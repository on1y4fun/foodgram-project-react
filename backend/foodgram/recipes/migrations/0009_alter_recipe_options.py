# Generated by Django 4.1.1 on 2022-10-07 16:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("recipes", "0008_alter_recipe_options"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="recipe",
            options={
                "ordering": ("-pub_date",),
                "verbose_name": "Рецепт",
                "verbose_name_plural": "Рецепты",
            },
        ),
    ]
