from django.urls import include, path
from rest_framework.routers import SimpleRouter

from recipes.views import IngredientViewSet, RecipeViewSet, TagViewSet

router_v1 = SimpleRouter()
router_v1.register(r'recipes', RecipeViewSet, basename='recipes')
router_v1.register(r'tags', TagViewSet, basename='tags')
router_v1.register(r'ingredients', IngredientViewSet, basename='ingredients')

urlpatterns = [
    path('v1/', include(router_v1.urls))
]