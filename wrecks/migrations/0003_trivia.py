# Generated by Django 3.0.3 on 2020-04-17 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wrecks', '0002_auto_20200415_0210'),
    ]

    operations = [
        migrations.CreateModel(
            name='Trivia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=255)),
                ('ans1', models.TextField(blank=True, null=True)),
                ('ans2', models.TextField(blank=True, null=True)),
                ('ans3', models.TextField(blank=True, null=True)),
                ('ans4', models.TextField(blank=True, null=True)),
                ('correct', models.IntegerField(blank=True, null=True)),
            ],
        ),
    ]