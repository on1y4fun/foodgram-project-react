import base64
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError
from rest_framework.fields import get_error_detail, SkipField
from rest_framework.validators import UniqueTogetherValidator

from django.core.files.base import ContentFile
from rest_framework import serializers

from recipes.models import (
    Ingredient,
    Recipe,
    RecipeTag,
    RecipeIngredient,
    Tag,
)
from users.models import Follow, User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password'
        )

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super(UserSerializer, self).create(validated_data)


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = (
            'id',
            'name',
            'unit',
        )

    def serialize_ingredient(self, ingredient):
        try:
            recipe = self.context['recipe_instance']
        except KeyError:
            return {}
        recipe_ingredient = ingredient.recipeingredient.filter(
            recipe=recipe
        ).first()
        return RecipeIngredientSerializer(recipe_ingredient).data

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        return {**rep, **self.serialize_ingredient(instance)}


class RecipeIngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeIngredient
        fields = ('amount',)

    def validate(self, attrs):
        return super().validate(attrs)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, required=True)
    author = UserSerializer(required=False, read_only=True)
    ingredients = serializers.SerializerMethodField(source='get_ingredients')
    image = Base64ImageField(required=True)
    is_favorited = serializers.SerializerMethodField(
        source='get_is_favorite', default=False
    )
    is_in_shopping_cart = serializers.SerializerMethodField(
        source='get_is_in_shopping_cart', default=False
    )

    def to_internal_value(self, data):
        fields = self._writable_fields
        tags = []
        out_data = {}
        errors = {}
        for tag in data['tags']:
            tags.append(
                TagSerializer(Tag.objects.filter(id=tag), many=True).data[0]
            )
        data['tags'] = tags
        for field in fields:
            validate_method = getattr(
                self, 'validate_' + field.field_name, None
            )
            primitive_value = field.get_value(data)
            try:
                validated_value = field.run_validation(primitive_value)
                if validate_method is not None:
                    validated_value = validate_method(validated_value)
            except ValidationError as exc:
                if not field.field_name == 'tags':
                    errors[field.field_name] = exc
                pass
            except DjangoValidationError as exc:
                errors[field.field_name] = get_error_detail(exc)
            except SkipField:
                pass   
            else:
                out_data[field.source_attrs[0]] = validated_value
        if errors:
            raise ValidationError(errors)
        out_data['tags'] = tags
        out_data['ingredients'] = data['ingredients']
        return out_data

    def get_ingredients(self, recipe):
        return IngredientSerializer(
            recipe.ingredients.all(),
            context={'recipe_instance': recipe},
            many=True,
        ).data

    def create(self, validated_data):
        request = self.context.get('request', None)
        validated_data['author'] = request.user
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        for ingredient in ingredients:
            amount = ingredient['amount']
            current_ingredient = Ingredient.objects.get(id=ingredient['id'])
            RecipeIngredient.objects.create(
                ingredient=current_ingredient, recipe=recipe, amount=amount
            )
        for tag in tags:
            current_tag = Tag.objects.get(id=tag['id'])
            RecipeTag.objects.create(tag=current_tag, recipe=recipe)
        return recipe

    def update(self, instance, validated_data):
        data = validated_data.copy()
        tags = data.pop('tags')
        ingredients = data.pop('ingredients')
        for field, value in data.items():
            setattr(instance, field, value)
        instance.save()
        update_tags = [tag['id'] for tag in tags]
        instance.tags.set(update_tags)
        update_ingredients = [ingredient['id'] for ingredient in ingredients]
        instance.ingredients.set(update_ingredients)
        for ingredient in ingredients:
            current_ingredient = instance.recipeingredient.filter(
                recipe=instance, ingredient=ingredient['id']
            ).first()
            current_ingredient.amount = ingredient.get('amount')
            current_ingredient.save()
        return instance

    def get_is_favorited(self, recipe):
        try:
            user = self.context['request'].user
            if user.is_anonymous:
                return None
        except KeyError:
            return None
        return recipe.favorite.filter(user=user, recipe=recipe).exists()

    def get_is_in_shopping_cart(self, recipe):
        try:
            user = self.context['request'].user
            if user.is_anonymous:
                return False
        except KeyError:
            return False
        return recipe.shopping.filter(user=user, recipe=recipe).exists()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'name',
            'image',
            'text',
            'cooking_time',
            'is_favorited',
            'is_in_shopping_cart',
        )


class FollowSerializer(serializers.ModelSerializer):
    author = UserSerializer(required=False)
    recipes = serializers.SerializerMethodField(source='get_recipes')
    recipes_count = serializers.SerializerMethodField(
        source='get_recipes_count'
    )

    class Meta:
        fields = ('author', 'recipes', 'recipes_count')
        model = Follow

    def get_recipes(self, user):
        recipes = RecipeSerializer(
            user.author.recipe.filter(author=user.author),
            context={'request': self.context['request']},
            many=True,
        ).data
        for recipe in recipes:
            for field in ['tags', 'author', 'ingredients', 'text']:
                recipe.pop(field)
        return recipes

    def get_recipes_count(self, user):
        return user.author.recipe.filter(author=user.author).count()

    def to_representation(self, instance):
        data = super().to_representation(instance)
        recipes = data.pop('recipes')
        recipes_count = data.pop('recipes_count')
        data['author']['recipes'] = recipes
        data['author']['recipes_count'] = recipes_count
        return data['author']


class FavoriteOrShoppingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class UserPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(max_length=150)
    current_password = serializers.CharField(max_length=150)

    def validate(self, data):
        errors = {}
        if data.get('new_password') == data.get('current_password'):
            errors['new_password'] = 'Пароль должен отличаться'
            raise serializers.ValidationError(errors)
        return data

    class Meta:
        fields = ('new_password', 'current_password',)
