from django.urls import include, path
from rest_framework.routers import SimpleRouter

from recipes.views import (
    IngredientViewSet,
    RecipeViewSet,
    TagViewSet,
)
from users.views import FollowViewSet, UserViewSet

router_v1 = SimpleRouter()
router_v1.register(r'recipes', RecipeViewSet, basename='recipes')
router_v1.register(r'tags', TagViewSet, basename='tags')
router_v1.register(r'ingredients', IngredientViewSet, basename='ingredients')
router_v1.register(r'users/subscribtions', FollowViewSet, basename='following')
router_v1.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('', include(router_v1.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
