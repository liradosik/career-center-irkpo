from apps.accounts.models import User


def _is_student(user):
    return getattr(user, 'role', None) == User.Role.STUDENT


def can_register_courses(user):
    return _is_student(user) and user.academic_status == User.AcademicStatus.STUDYING


def can_apply_vacancies(user):
    return _is_student(user) and user.academic_status in {
        User.AcademicStatus.STUDYING,
        User.AcademicStatus.GRADUATED,
    }


def can_create_portfolio_entries(user):
    return _is_student(user) and user.academic_status == User.AcademicStatus.STUDYING


def can_edit_portfolio_entries(user):
    return can_create_portfolio_entries(user)


def can_edit_resume(user):
    return _is_student(user) and user.academic_status in {
        User.AcademicStatus.STUDYING,
        User.AcademicStatus.ACADEMIC_LEAVE,
        User.AcademicStatus.GRADUATED,
    }


def can_manage_favorites(user, target='any'):
    if not _is_student(user):
        return False

    if user.academic_status == User.AcademicStatus.STUDYING:
        return True

    if user.academic_status == User.AcademicStatus.GRADUATED:
        return target == 'vacancies'

    return False