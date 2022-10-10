from rest_framework import exceptions, viewsets, status, permissions, filters
from rest_framework.decorators import api_view, action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.db.models import Sum


from recipes.models import Favorite, Ingredient, Recipe, Tag, ShoppingList
from api.filters import FavoriteShoppingFilter
from api.permissions import AuthorOrAuthenticated
from api.serializers import (
    IngredientSerializer,
    RecipeSerializer,
    TagSerializer,
    FavoriteOrShoppingSerializer,
)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = PageNumberPagination
    permission_classes = (AuthorOrAuthenticated,)
    filterset_class = FavoriteShoppingFilter
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = (
        'author',
        'tags',
        'is_favorited',
        'is_in_shopping_cart',
    )

    def _process(self, request, model, recipe, query):
        user = request.user
        if request.method == 'DELETE':
            query.get(recipe=recipe).delete()
            return Response('Объект удален', status=status.HTTP_200_OK)
        if query.filter(recipe=recipe).exists():
            return Response(
                'Уже есть в списке', status=status.HTTP_400_BAD_REQUEST
            )
        instance = model.objects.create(user=user, recipe=recipe)
        serializer = FavoriteOrShoppingSerializer(recipe)
        return Response(serializer.data)

    @action(
        detail=True,
        methods=(
            'post',
            'delete',
        ),
        permission_classes=(permissions.IsAuthenticated,),
    )
    def favorite(self, request, pk):
        recipe = get_object_or_404(Recipe, id=pk)
        return self._process(request, Favorite, recipe, request.user.favorite)

    @action(
        detail=True,
        methods=(
            'post',
            'delete',
        ),
        permission_classes=(permissions.IsAuthenticated,),
    )
    def shopping_cart(self, request, pk):
        recipe = get_object_or_404(Recipe, id=pk)
        return self._process(
            request, ShoppingList, recipe, request.user.shopping
        )

    @action(
        detail=False,
        methods=('get',),
        permission_classes=(permissions.IsAuthenticated,),
    )
    def download_shopping_cart(self, request):
        user = request.user
        content = 'Foodgram\n' + 'Shopping list\n'
        recipes = user.shopping.select_related('recipe').prefetch_related(
            'recipe__recipeingredient'
        )
        shopping_list = {}
        for instance in recipes:
            objects = instance.recipe.recipeingredient.values(
                'ingredient_id', 'amount'
            )
            for object in objects:
                ingredient = Ingredient.objects.get(
                    id=object['ingredient_id']
                )
                if ingredient.name not in shopping_list:
                    shopping_list[ingredient.name] = [object['amount'], ingredient.unit]
                else:
                    shopping_list[ingredient.name][0] += object['amount']
        for name, amount in shopping_list.items():
            content += f'{name} - {amount[0]} {amount[1]}\n'
        response = HttpResponse(content, content_type='text/plain')
        return response


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    # permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, )
    filterset_fields = ('name',)
    search_fields = ('^name',)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)