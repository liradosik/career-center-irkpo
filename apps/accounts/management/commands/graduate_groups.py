from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from apps.accounts.models import StudyGroup, User


class Command(BaseCommand):
    help = (
        'Выпускает учебные группы: делает группу неактивной и переводит студентов в статус "выпускник". '
        'По умолчанию запускается в dry-run режиме (без изменений).'
    )

    def add_arguments(self, parser):
        parser.add_argument('--apply', action='store_true', help='Применить изменения (без флага работает dry-run).')
        parser.add_argument('--group-id', type=int, help='Выпустить конкретную группу по ID.')
        parser.add_argument('--group-code', type=str, help='Выпустить конкретную группу по коду/названию, например И-422/1.')

    def handle(self, *args, **options):
        apply_changes = options['apply']
        group_id = options.get('group_id')
        group_code = (options.get('group_code') or '').strip()

        if group_id and group_code:
            raise CommandError('Используйте только один параметр: --group-id или --group-code.')

        groups_qs = StudyGroup.objects.all().order_by('name')

        if group_id:
            groups_qs = groups_qs.filter(id=group_id)
            scope_label = f'group-id={group_id}'
        elif group_code:
            groups_qs = groups_qs.filter(name=group_code)
            scope_label = f'group-code="{group_code}"'
        else:
            groups_qs = groups_qs.filter(is_active=True, course_number__gte=4)
            scope_label = 'all active groups with course_number >= 4'

        groups = list(groups_qs)
        if not groups:
            self.stdout.write(self.style.WARNING(f'Группы не найдены для выборки: {scope_label}'))
            return

        mode_label = 'APPLY' if apply_changes else 'DRY-RUN'
        self.stdout.write(self.style.WARNING(f'Режим: {mode_label}'))
        self.stdout.write(f'Выборка: {scope_label}')

        updated_groups = 0
        updated_students = 0

        for group in groups:
            students_qs = User.objects.filter(role=User.Role.STUDENT, study_group=group)
            total_students = students_qs.count()
            already_graduated = students_qs.filter(academic_status=User.AcademicStatus.GRADUATED).count()
            to_graduate = total_students - already_graduated

            if not group.is_active:
                self.stdout.write(
                    self.style.WARNING(
                        f'Пропуск {group.name} (id={group.id}): группа уже неактивна. '
                        f'Студентов: {total_students}, уже выпускники: {already_graduated}, к переводу: 0.'
                    )
                )
                continue

            self.stdout.write(
                f'- {group.name} (id={group.id}): студентов={total_students}, '
                f'уже выпускники={already_graduated}, к переводу в graduated={to_graduate}'
            )

            if apply_changes:
                with transaction.atomic():
                    group.is_active = False
                    group.save(update_fields=['is_active'])
                    changed = students_qs.exclude(academic_status=User.AcademicStatus.GRADUATED).update(
                        academic_status=User.AcademicStatus.GRADUATED
                    )
                updated_groups += 1
                updated_students += changed

        if apply_changes:
            self.stdout.write(
                self.style.SUCCESS(
                    f'Изменения применены. Обновлено групп: {updated_groups}. '
                    f'Обновлено студентов (academic_status -> graduated): {updated_students}.'
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    'Dry-run завершён. Изменения не применялись. '
                    f'Будет обновлено групп: {sum(1 for g in groups if g.is_active)}. '
                    f'Будет обновлено студентов: '
                    f'{sum(User.objects.filter(role=User.Role.STUDENT, study_group=g).exclude(academic_status=User.AcademicStatus.GRADUATED).count() for g in groups if g.is_active)}.'
                )
            )
