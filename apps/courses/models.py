from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class Course(models.Model):
    class Kind(models.TextChoices):
        COURSE = 'course', 'Курс'
        SEMINAR = 'seminar', 'Семинар'
        PRACTICE = 'practice', 'Учебная практика'

    class Format(models.TextChoices):
        ONLINE = 'online', 'Онлайн'
        OFFLINE = 'offline', 'Очно'

    class Status(models.TextChoices):
        ACTIVE = 'active', 'Active'
        HIDDEN = 'hidden', 'Hidden'
        ARCHIVE = 'archive', 'Archive'

    title = models.CharField(max_length=255)
    kind = models.CharField(max_length=16, choices=Kind.choices)
    format_type = models.CharField(max_length=16, choices=Format.choices)
    description = models.TextField()
    organization = models.CharField(max_length=255)
    contacts = models.CharField(max_length=255)
    address = models.CharField(max_length=255, blank=True)
    map_url = models.URLField(blank=True)
    online_url = models.URLField(blank=True)
    date = models.DateField()
    places = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['status', 'date'], name='course_status_date_idx'),
            models.Index(fields=['kind', 'status'], name='course_kind_status_idx'),
            models.Index(fields=['format_type', 'status'], name='course_format_status_idx'),
        ]

    @property
    def occupied_places(self):
        return self.registrations.filter(status=CourseRegistration.Status.REGISTERED).count()

    @property
    def occupied_places_count(self):
        return self.occupied_places

    @property
    def has_unlimited_places(self):
        return not self.places

    @property
    def available_places_count(self):
        if self.has_unlimited_places:
            return None
        return max(self.places - self.occupied_places_count, 0)

    @property
    def is_full(self):
        if self.has_unlimited_places:
            return False
        return self.occupied_places_count >= self.places

    @property
    def is_past(self):
        return bool(self.date and self.date < timezone.localdate())

    @property
    def has_available_places(self):
        return not self.is_full

    def __str__(self):
        return self.title


class CourseRegistration(models.Model):
    class Status(models.TextChoices):
        REGISTERED = 'registered', 'Записан'
        CANCELLED = 'cancelled', 'Отменена'

    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='course_registrations')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='registrations')
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.REGISTERED)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=('student', 'course'), condition=models.Q(status='registered'), name='uniq_active_course_registration'),
        ]

    def clean(self):
        if (
            self.status == self.Status.REGISTERED
            and not self.course.has_available_places
        ):
            raise ValidationError('На это мероприятие больше нет мест.')

    def save(self, *args, **kwargs):
        self.clean()
        return super().save(*args, **kwargs)


class StudentFavoriteCourse(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favorite_courses')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='favorited_by_students')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=('student', 'course'), name='uniq_student_favorite_course'),
        ]

    def __str__(self):
        return f'{self.student} ♥ {self.course}'
