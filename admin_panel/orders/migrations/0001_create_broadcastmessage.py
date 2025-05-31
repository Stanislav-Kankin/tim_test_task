from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='BroadcastMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Текст сообщения')),
                ('image', models.ImageField(blank=True, null=True, upload_to='broadcast_images/', verbose_name='Картинка (опционально)')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_sent', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Рассылка',
                'verbose_name_plural': 'Рассылки',
            },
        ),
    ]
