from django.core.management.base import BaseCommand

from property.services import dispatch_recent_saved_search_alerts


class Command(BaseCommand):
    help = 'Send saved-search alerts for recently published property listings.'

    def add_arguments(self, parser):
        parser.add_argument('--days', type=int, default=1, help='Look back this many days for active properties.')

    def handle(self, *args, **options):
        delivered = dispatch_recent_saved_search_alerts(days=options['days'])
        self.stdout.write(self.style.SUCCESS(f'Property saved-search alerts delivered: {delivered}'))
