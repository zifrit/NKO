from django.core.management import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        if User.objects.filter(username='admin', is_superuser=True).exists():
            self.stdout.write(self.style.SUCCESS('Success create superuser'))
        else:
            User.objects.create_superuser(username="admin", password="admin")
            self.stdout.write(self.style.SUCCESS('Success create superuser'))
