# Generated by Django 3.0.7 on 2020-11-06 09:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('payment_system', '0005_auto_20201029_1328'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('deleted_at', models.DateTimeField(blank=True, default=None, null=True)),
                ('role', models.CharField(blank=True, choices=[('initiator', 'Initiator'),
                                                               ('participant', 'Participant')],
                                          default='participant', max_length=20)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                              related_name='user_projects', to='payment_system.Project')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                           related_name='user_projects', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['id'],
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='project',
            name='users',
        ),
        migrations.AddField(
            model_name='project',
            name='users',
            field=models.ManyToManyField(related_name='projects', through='payment_system.UserProject',
                                         to=settings.AUTH_USER_MODEL),
        ),
    ]