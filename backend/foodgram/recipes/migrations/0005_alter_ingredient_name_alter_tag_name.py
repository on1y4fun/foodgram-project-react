# Generated by Django 4.1.1 on 2022-10-06 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("recipes", "0004_alter_recipe_cooking_time"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ingredient",
            name="name",
            field=models.CharField(
                help_text="Введите название ингредиента",
                max_length=200,
                unique=True,
                verbose_name="Название ингредиента",
            ),
        ),
        migrations.AlterField(
            model_name="tag",
            name="name",
            field=models.CharField(
                help_text="Введите название тега",
                max_length=200,
                unique=True,
                verbose_name="Название тега",
            ),
        ),
    ]