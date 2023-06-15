# Generated by Django 4.2.1 on 2023-06-13 12:06

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
            name='AcademicYear',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=12)),
                ('started_at', models.DateField()),
                ('finished_at', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Level',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level_number', models.IntegerField(choices=[(1, 'First'), (2, 'Second'), (3, 'Last')], default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=24)),
                ('birth_date', models.DateField()),
                ('confession', models.IntegerField(choices=[(-1, 'Not Defined'), (0, 'Roman Catholic'), (1, 'Greek Catholic'), (2, 'Orthodox'), (3, 'Other')], default=-1)),
                ('education', models.IntegerField(choices=[(-1, 'Higher'), (0, 'Secondary'), (1, 'Vocational'), (2, 'Primary'), (3, 'Other')], default=-1)),
                ('address', models.TextField(blank=True)),
                ('workplace', models.TextField(blank=True)),
                ('comments', models.TextField(blank=True)),
                ('index', models.CharField(blank=True, max_length=24, unique=True)),
                ('diploma', models.CharField(blank=True, max_length=24, unique=True)),
                ('academic_years', models.ManyToManyField(related_name='students', to='student.academicyear')),
                ('level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='students', to='student.level')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='StudentItemYear',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('academic_year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.academicyear')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.item')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.student')),
            ],
            options={
                'unique_together': {('student', 'item', 'academic_year')},
            },
        ),
        migrations.AddField(
            model_name='item',
            name='students',
            field=models.ManyToManyField(related_name='items', through='student.StudentItemYear', to='student.student'),
        ),
        migrations.AddField(
            model_name='academicyear',
            name='items',
            field=models.ManyToManyField(related_name='academicyears', through='student.StudentItemYear', to='student.item'),
        ),
    ]
