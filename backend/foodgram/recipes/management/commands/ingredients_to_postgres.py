import csv
from django.core.management.base import BaseCommand
import psycopg2

from foodgram.settings import DATABASES


class Command(BaseCommand):

    def handle(self, *args, **options):
        data_path = f'fixtures_ingredients.csv'
        with open(data_path, 'r', encoding='utf8') as csv_file:
            database = csv.DictReader(csv_file)
            database.fieldnames = ['name', 'measurement_unit']
            connection = psycopg2.connect(
                dbname=DATABASES['default']['NAME'],
                user=DATABASES['default']['USER'],
                password=DATABASES['default']['PASSWORD'],
                host=DATABASES['default']['HOST'],
                port=DATABASES['default']['PORT'],
            )
            cursor = connection.cursor()
            columns = ','.join(database.fieldnames)
            sql_request = f"""copy recipes_ingredient({columns})
                        from stdout with (format csv)"""
            cursor.copy_expert(sql_request, csv_file)
            connection.commit()
