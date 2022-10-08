from django.contrib import admin

from recipes.models import (
    Ingredient,
    Recipe,
    Tag,
    ShoppingList,
    RecipeIngredient,
    RecipeTag,
    Favorite
)

class IngredientInline(admin.TabularInline):
    model = RecipeIngredient


class TagInline(admin.TabularInline):
    model = RecipeTag


class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'author',
        'name',
        'image',
        'text',
        'cooking_time',
    )
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'
    inlines = (
        IngredientInline,
        TagInline,
    )


class ShoppingAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'user',
        'recipe',
    )
    search_fields = ('user',)
    list_filter = ('user',)
    empty_value_display = '-пусто-'


class FavoriteAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'user',
        'recipe',
    )
    search_fields = ('user',)
    list_filter = ('user',)
    empty_value_display = '-пусто-'


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient)
admin.site.register(Tag)
admin.site.register(ShoppingList, ShoppingAdmin)
admin.site.register(Favorite, FavoriteAdmin)

