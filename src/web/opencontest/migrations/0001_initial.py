# Generated by Django 2.1.7 on 2019-03-09 00:43

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
            name='Contest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('start', models.DateTimeField()),
                ('scoreboard_freeze', models.DateTimeField()),
                ('end', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=100)),
                ('is_admin', models.BooleanField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Problem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=255)),
                ('statement', models.CharField(max_length=1000)),
                ('input_format', models.CharField(max_length=1000)),
                ('output_format', models.CharField(max_length=1000)),
                ('constraints', models.CharField(max_length=1000)),
                ('sample_count', models.IntegerField(default=0)),
                ('contest', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='opencontest.Contest')),
            ],
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_full', models.BooleanField()),
                ('timestamp', models.DateTimeField()),
                ('code_path', models.CharField(max_length=255)),
                ('contest', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='opencontest.Contest')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='opencontest.Person')),
                ('problem', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='opencontest.Problem')),
                ('result', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='opencontest.Result')),
            ],
        ),
        migrations.CreateModel(
            name='SubmissionCase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stdout_path', models.CharField(max_length=255)),
                ('stderr_path', models.CharField(max_length=255)),
                ('submission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='opencontest.Submission')),
            ],
        ),
        migrations.CreateModel(
            name='TestCase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('input_path', models.CharField(max_length=255)),
                ('output_path', models.CharField(max_length=255)),
                ('problem', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='opencontest.Problem')),
            ],
        ),
        migrations.AddField(
            model_name='submissioncase',
            name='test_case',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='opencontest.TestCase'),
        ),
    ]
