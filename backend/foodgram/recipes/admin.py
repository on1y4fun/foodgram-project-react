from django.contrib import admin

from recipes.models import (
    Ingredient,
    Recipe,
    Tag,
    ShoppingList,
    RecipeShopping,
    RecipeIngredient,
    RecipeTag,
    Follow,
)


class IngredientInline(admin.TabularInline):
    model = RecipeIngredient


class TagInline(admin.TabularInline):
    model = RecipeTag


class ShoppingInline(admin.TabularInline):
    model = RecipeShopping


class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'author',
        'name',
        'image',
        'description',
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
    )
    search_fields = ('user',)
    list_filter = ('user',)
    empty_value_display = '-пусто-'
    inlines = (ShoppingInline,)


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient)
admin.site.register(Tag)
admin.site.register(ShoppingList, ShoppingAdmin)
admin.site.register(Follow)
