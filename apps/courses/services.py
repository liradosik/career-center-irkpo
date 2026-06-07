from django.utils import timezone

from .models import Course


def archive_past_courses_if_needed():
    """Archive active/hidden courses with a date earlier than today.

    The function intentionally performs a single UPDATE query and does not
    delete records, so it is safe to call before pages that depend on fresh
    course statuses.
    """
    today = timezone.localdate()
    return Course.objects.filter(
        status__in=[Course.Status.ACTIVE, Course.Status.HIDDEN],
        date__lt=today,
    ).update(status=Course.Status.ARCHIVE)
