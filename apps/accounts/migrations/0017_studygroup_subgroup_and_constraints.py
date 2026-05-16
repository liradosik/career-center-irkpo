from django.db import migrations, models
import django.db.models.functions.comparison


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0016_studentprofile_contact_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='studygroup',
            name='subgroup_number',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AddConstraint(
            model_name='studygroup',
            constraint=models.UniqueConstraint(
                'specialty_ref',
                'admission_year',
                'course_number',
                django.db.models.functions.comparison.Coalesce('subgroup_number', 0),
                name='accounts_group_specialty_year_course_subgroup_uniq',
            ),
        ),
    ]
