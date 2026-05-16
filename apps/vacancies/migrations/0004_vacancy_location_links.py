from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vacancies', '0003_studentfavoritevacancy'),
    ]

    operations = [
        migrations.AddField(
            model_name='vacancy',
            name='address',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='vacancy',
            name='map_url',
            field=models.URLField(blank=True),
        ),
    ]
