from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0018_user_must_change_password'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdminActivityLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(choices=[('create', 'Создание'), ('update', 'Обновление'), ('delete', 'Удаление'), ('status_change', 'Смена статуса'), ('reset_password', 'Сброс пароля')], max_length=32)),
                ('object_type', models.CharField(choices=[('student', 'Студент'), ('curator', 'Куратор'), ('group', 'Группа'), ('specialty', 'Специальность'), ('vacancy', 'Вакансия'), ('course', 'Курс'), ('support_ticket', 'Обращение')], max_length=32)),
                ('object_id', models.PositiveIntegerField(blank=True, null=True)),
                ('object_repr', models.CharField(blank=True, max_length=255)),
                ('description', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('actor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='admin_actions', to='accounts.user')),
            ],
            options={
                'ordering': ('-created_at',),
                'indexes': [models.Index(fields=['-created_at'], name='accounts_admlog_created_idx'), models.Index(fields=['object_type', 'action'], name='accounts_admlog_oa_idx'), models.Index(fields=['actor', '-created_at'], name='accounts_admlog_ac_idx')],
            },
        ),
    ]
