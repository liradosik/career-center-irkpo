from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.courses.models import Course


class Command(BaseCommand):
    help = (
        'Архивирует прошедшие курсы (active/hidden -> archive). '
        'По умолчанию запускается в dry-run режиме.'
    )

    def add_arguments(self, parser):
        parser.add_argument('--apply', action='store_true', help='Применить изменения (без флага работает dry-run).')

    def handle(self, *args, **options):
        apply_changes = options['apply']
        today = timezone.localdate()

        queryset = Course.objects.filter(
            status__in=[Course.Status.ACTIVE, Course.Status.HIDDEN],
            date__lt=today,
        ).order_by('date', 'id')

        courses = list(queryset)
        total = len(courses)
        mode = 'APPLY' if apply_changes else 'DRY-RUN'

        self.stdout.write(self.style.WARNING(f'Режим: {mode}'))
        self.stdout.write(f'Дата проверки: {today:%Y-%m-%d}')
        self.stdout.write(f'Найдено прошедших курсов к архивации: {total}')

        if courses:
            self.stdout.write('Список курсов:')
            for course in courses:
                self.stdout.write(
                    f'- id={course.id}, title="{course.title}", date={course.date:%Y-%m-%d}, status={course.status}'
                )

        if not apply_changes:
            self.stdout.write(self.style.SUCCESS('Dry-run завершён. Изменения не применялись.'))
            return

        archived_count = queryset.update(status=Course.Status.ARCHIVE)
        self.stdout.write(self.style.SUCCESS(f'Реально архивировано курсов: {archived_count}'))
