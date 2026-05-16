from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0017_studygroup_subgroup_and_constraints'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='must_change_password',
            field=models.BooleanField(default=False),
        ),
    ]
