# Generated by Django 2.2 on 2020-04-03 02:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('my_poll_app', '0002_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='poll',
            name='submitted_by',
            field=models.ForeignKey(default=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_polls', to='my_poll_app.User'),
        ),
    ]
