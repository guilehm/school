import time

from django.core.management.base import BaseCommand
from django.db import connections


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write('Waiting for database...')
        connected = False
        while not connected:
            try:
                db_conn = connections['default']
                db_conn.ensure_connection()
                connected = True
            except Exception as e:
                self.stdout.write(e)
                self.stdout.write('Database is not available, waiting...')
                time.sleep(2)
        self.stdout.write(self.style.SUCCESS('Database available!'))
