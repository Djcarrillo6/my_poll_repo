# Generated by Django 2.2 on 2020-04-04 00:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('my_poll_app', '0003_poll_submitted_by'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('poll_choice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='my_poll_app.Poll')),
                ('voter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='my_poll_app.User')),
            ],
        ),
    ]
