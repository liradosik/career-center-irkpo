from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.accounts.models import SupportTicket


class Command(BaseCommand):
    help = (
        'Архивирует решённые обращения техподдержки старше 30 дней: '
        'status=resolved -> status=closed. По умолчанию dry-run.'
    )

    def add_arguments(self, parser):
        parser.add_argument('--apply', action='store_true', help='Применить изменения. Без флага работает dry-run.')

    def handle(self, *args, **options):
        apply_changes = options['apply']
        cutoff = timezone.now() - timedelta(days=30)

        queryset = SupportTicket.objects.filter(
            status=SupportTicket.Status.RESOLVED,
            resolved_at__isnull=False,
            resolved_at__lt=cutoff,
        )

        total = queryset.count()
        mode = 'APPLY' if apply_changes else 'DRY-RUN'

        self.stdout.write(self.style.WARNING(f'Режим: {mode}'))
        self.stdout.write(f'Порог даты решения: {cutoff:%Y-%m-%d %H:%M:%S %Z}')
        self.stdout.write(f'Найдено resolved-обращений старше 30 дней: {total}')

        if not apply_changes:
            self.stdout.write(self.style.SUCCESS('Dry-run завершён. Изменения не применялись.'))
            return

        archived_count = queryset.update(status=SupportTicket.Status.CLOSED)
        self.stdout.write(self.style.SUCCESS(f'Архивировано обращений (resolved -> closed): {archived_count}'))
