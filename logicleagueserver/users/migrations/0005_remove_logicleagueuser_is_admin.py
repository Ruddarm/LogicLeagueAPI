# Generated by Django 5.1.3 on 2024-11-21 07:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_logicleagueuser_username'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='logicleagueuser',
            name='is_admin',
        ),
    ]