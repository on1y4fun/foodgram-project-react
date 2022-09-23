from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Recipe(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Автор рецепта'
    )
    name = models.CharField(
        max_length=64,
        verbose_name='Название рецепта',
        help_text='Введите название рецепта',
    )
    image = models.ImageField(
        null=True, verbose_name='Фото блюда', help_text='Приложите фото блюда'
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Описание рецепта',
        help_text='Опишите рецепт',
    )
    ingredient = models.ManyToManyField(
        through='RecipeIngredient',
        verbose_name='Список ингредиентов',
        help_text='Выберите ингредиенты',
    )
    tag = models.ManyToManyField(
        through='RecipeTag',
        blank=True,
        null=True,
        verbose_name='Список тегов',
        help_text='Выберите теги',
    )
    cooking_time = models.IntegerField(
        verbose_name='Время приготовления', help_text='Введите время'
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(
        verbose_name='Название тега', help_text='Введите название тега'
    )
    color = models.CharField(
        max_length=64, verbose_name='Цвет тега', help_text='Выберите цвет тега'
    )
    slug = models.SlugField(
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
        verbose_name='Название ингредиента',
        help_text='Введите название ингредиента',
    )
    quantity = models.FloatField(
        verbose_name='Количество ингредиентов',
        help_text='Введите количество ингредиентов',
    )
    unit = models.CharField(
        verbose_name='Единица измерения', help_text='Введите единицу измерения'
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ('name',)

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.SET_NULL, verbose_name='Рецепт блюда'
    )
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.SET_NULL, verbose_name='Ингредиенты'
    )

    def __str__(self):
        return f'{self.recipe} {self.ingredient}'


class RecipeTag(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.SET_NULL, verbose_name='Рецепт блюда'
    )
    tag = models.ForeignKey(
        Tag, on_delete=models.SET_NULL, verbose_name='Теги'
    )

    def __str__(self):
        return f'{self.recipe} {self.tag}'
