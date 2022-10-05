import base64
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError
from rest_framework.fields import SkipField
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
from users.models import User, Follow


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
        )


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
    # is_favorite = serializers.BooleanField(required=False, default=False)

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
        )
        validators = [
            UniqueTogetherValidator(
                queryset=Recipe.objects.all(), fields=('author', 'name')
            )
        ]

    def to_internal_value(self, data):
        fields = self._writable_fields
        tags = []
        ret = {}
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
                pass
            except DjangoValidationError as exc:
                pass
            except SkipField:
                pass
            else:
                ret[field.source_attrs[0]] = validated_value
        for tag in data['tags']:
            tags.append(
                TagSerializer(Tag.objects.filter(id=tag), many=True).data[0]
            )
        ret['tags'] = tags
        ret['ingredients'] = data['ingredients']
        return ret

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
        recipe = Recipe.objects.create(**validated_data, image=self.image)
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


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field='username',
        default=serializers.CurrentUserDefault(),
        queryset=User.objects.all(),
    )
    following = serializers.SlugRelatedField(
        slug_field='username', queryset=User.objects.all()
    )

    class Meta:
        model = User
        fields = ('user', 'following',)
        model = Follow
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(), fields=('user', 'following')
            )
        ]
