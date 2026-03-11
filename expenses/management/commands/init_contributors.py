from django.core.management.base import BaseCommand
from expenses.models import Contributor


class Command(BaseCommand):
    help = 'Initialize default contributors (Fadhil and Shahid)'

    def handle(self, *args, **options):
        # Create default contributors
        contributors_data = [
            {'name': 'Fadhil', 'description': 'Default contributor'},
            {'name': 'Shahid', 'description': 'Default contributor'},
        ]
        
        created_count = 0
        for data in contributors_data:
            contributor, created = Contributor.objects.get_or_create(
                name=data['name'],
                defaults={'description': data['description']}
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created contributor: {contributor.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Contributor already exists: {contributor.name}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'\nTotal contributors created: {created_count}')
        )
