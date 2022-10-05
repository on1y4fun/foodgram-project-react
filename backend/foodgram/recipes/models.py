from email.policy import default
from django.db import models

from users.models import User


class Tag(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название тега',
        help_text='Введите название тега',
    )
    color = models.CharField(
        max_length=7, verbose_name='Цвет тега', help_text='Выберите цвет тега'
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name='Слаг-название тега',
        help_text='Введите слаг-название',
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название ингредиента',
        help_text='Введите название ингредиента',
    )
    unit = models.CharField(
        max_length=200,
        verbose_name='Единица измерения',
        help_text='Введите единицу измерения',
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    tags = models.ManyToManyField(
        Tag,
        through='RecipeTag',
        blank=True,
        verbose_name='Список тегов',
        help_text='Выберите теги',
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Автор рецепта'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        related_name='recipe',
        verbose_name='Список ингредиентов',
        help_text='Выберите ингредиенты',
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Название рецепта',
        help_text='Введите название рецепта',
    )
    image = models.ImageField(
        upload_to='recipes/images/', 
        default=None,
        null=True,
        verbose_name='Фото блюда',
        help_text='Приложите фото блюда',
    )
    text = models.TextField(
        blank=True,
        null=True,
        verbose_name='Описание рецепта',
        help_text='Опишите рецепт',
    )
    cooking_time = models.IntegerField(
        verbose_name='Время приготовления, мин',
        help_text='Введите время в минутах',
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('name',)

    def __str__(self):
        return self.name




class ShoppingList(models.Model):
    user = models.ForeignKey(
        User, verbose_name='Пользователь', on_delete=models.CASCADE
    )
    recipe = models.ManyToManyField(
        Recipe, verbose_name='Рецепт', through='RecipeShopping'
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        ordering = ('user',)

    def __str__(self):
        return f'{self.user} {self.recipe}'


# class Favorite(models.Model):
#     user = models.ForeignKey(
#         User, verbose_name='Пользователь', on_delete=models.CASCADE
#     )
#     recipe = models.ForeignKey(
#         Recipe, verbose_name='Рецепт', on_delete=models.CASCADE
#     )

#     class Meta:
#         verbose_name = 'Список избранного'
#         verbose_name_plural = 'Списки избранного'
#         ordering = ('user',)

#     def __str__(self):
#         return f'{self.user} {self.recipe}'


class RecipeShopping(models.Model):
    shopping_list = models.ForeignKey(
        ShoppingList,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Список покупок',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Рецепт',
    )

    def __str__(self):
        return f'{self.shopping_list} {self.recipe}'


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.SET_NULL,
        related_name='recipeingredient',
        null=True,
        verbose_name='Рецепт блюда',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        related_name='recipeingredient',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Ингредиенты',
    )
    amount = models.IntegerField(null=True, verbose_name='Количество')

    def __str__(self):
        return f'{self.recipe} {self.ingredient}'


class RecipeTag(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Рецепт блюда',
    )
    tag = models.ForeignKey(
        Tag, on_delete=models.SET_NULL, null=True, verbose_name='Теги'
    )

    def __str__(self):
        return f'{self.recipe} {self.tag}'
