from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_studentfavoritecourse'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='address',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='course',
            name='map_url',
            field=models.URLField(blank=True),
        ),
        migrations.AddField(
            model_name='course',
            name='online_url',
            field=models.URLField(blank=True),
        ),
    ]
