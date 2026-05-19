from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0003_portfolioentry_indexes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='portfolioentry',
            name='type',
            field=models.CharField(
                choices=[
                    ('academic', 'Учебные достижения'),
                    ('project', 'Проекты и работы'),
                    ('skill', 'Навыки'),
                    ('certificates', 'Сертификаты и курсы'),
                    ('recommendation', 'Отзывы и рекомендации'),
                    ('creative', 'Творческая деятельность'),
                    ('sport', 'Спортивная деятельность'),
                    ('social', 'Общественная деятельность'),
                ],
                max_length=64,
            ),
        ),
    ]
