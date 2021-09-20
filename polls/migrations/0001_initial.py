# Generated by Django 2.2.1 on 2019-05-21 01:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EventDay',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='PollUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(default='FIRST_NAME', max_length=100)),
                ('last_name', models.CharField(default='LAST_NAME', max_length=100)),
                ('phone_number', models.CharField(default='0917', max_length=20)),
                ('student_number', models.CharField(default='1234', max_length=20)),
                ('entry_year', models.IntegerField()),
                ('can_presure', models.BooleanField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index', models.IntegerField(default=1)),
                ('eventday', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.EventDay')),
            ],
        ),
        migrations.CreateModel(
            name='USR',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('polluser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.PollUser')),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.Section')),
            ],
        ),
    ]