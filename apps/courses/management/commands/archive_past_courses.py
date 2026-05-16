from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.courses.models import Course


class Command(BaseCommand):
    help = 'Архивирует активные прошедшие курсы. Запускайте вручную после завершения мероприятий.'

    def handle(self, *args, **options):
        today = timezone.localdate()
        archived_count = Course.objects.filter(
            status=Course.Status.ACTIVE,
            date__lt=today,
        ).update(status=Course.Status.ARCHIVE)
        self.stdout.write(self.style.SUCCESS(f'Архивировано курсов: {archived_count}'))
