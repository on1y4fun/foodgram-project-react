from django.core.validators import MinValueValidator
from django.db import models

from users.models import User

NAMING_LENGTH = 200


class Tag(models.Model):
    name = models.CharField(
        max_length=NAMING_LENGTH,
        verbose_name='Название тега',
        help_text='Введите название тега',
        unique=True,
    )
    color = models.CharField(
        max_length=7, verbose_name='Цвет тега', help_text='Выберите цвет тега'
    )
    slug = models.SlugField(
        max_length=NAMING_LENGTH,
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
        max_length=NAMING_LENGTH,
        verbose_name='Название ингредиента',
        help_text='Введите название ингредиента',
        unique=True,
    )
    measurement_unit = models.CharField(
        max_length=NAMING_LENGTH,
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
        related_name='recipe',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор рецепта',
        related_name='recipe',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        related_name='recipe',
        verbose_name='Список ингредиентов',
        help_text='Выберите ингредиенты',
    )
    name = models.CharField(
        max_length=NAMING_LENGTH,
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
    cooking_time = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1),
        ],
        verbose_name='Время приготовления, мин',
        help_text='Введите время в минутах',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата публикации', db_index=True
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-pub_date',)
        constraints = (
            models.UniqueConstraint(
                fields=(
                    'author',
                    'name',
                ),
                name='unique_name',
            ),
        )

    def __str__(self):
        return self.name


class ShoppingList(models.Model):
    user = models.ForeignKey(
        User,
        related_name='shopping',
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping',
        verbose_name='Рецепт',
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        ordering = ('user',)
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe'), name='shopping_model'
            )
        ]

    def __str__(self):
        return f'{self.user} {self.recipe}'


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='favorite',
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
        related_name='favorite',
    )

    class Meta:
        verbose_name = 'Список избранного'
        verbose_name_plural = 'Списки избранного'
        ordering = ('user',)
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe'), name='favorite_model'
            )
        ]

    def __str__(self):
        return f'{self.user} {self.recipe}'


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
    amount = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1),
        ],
        verbose_name='Количество',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('recipe', 'ingredient'), name='recipe_ingredient_model'
            )
        ]

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

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('recipe', 'tag'), name='recipe_tag_model'
            )
        ]

    def __str__(self):
        return f'{self.recipe} {self.tag}'
