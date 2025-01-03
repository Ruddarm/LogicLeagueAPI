# Generated by Django 5.1.3 on 2025-01-03 09:01

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('challenges', '0004_rename_values_testcase_output_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Contest',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('start_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('end_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('prizes', models.CharField(blank=True, max_length=300, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_public', models.BooleanField(default=False)),
                ('challenge', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contests', to='challenges.challenges')),
                ('participants', models.ManyToManyField(blank=True, related_name='contests', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Problem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('constraints', models.TextField()),
                ('test_cases', models.JSONField()),
                ('contest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='problems', to='contests.contest')),
            ],
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.TextField()),
                ('language', models.CharField(max_length=50)),
                ('status', models.CharField(max_length=50)),
                ('execution_time', models.FloatField()),
                ('score', models.IntegerField()),
                ('problem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='submissions', to='contests.problem')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='submissions', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
