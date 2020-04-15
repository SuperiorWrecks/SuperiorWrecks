# Generated by Django 3.0.3 on 2020-04-13 16:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Wrecks',
            fields=[
                ('ship_name', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('ship_num', models.CharField(max_length=255)),
                ('year_sunk', models.IntegerField(blank=True, null=True)),
                ('date_sunk', models.DateField(blank=True, null=True)),
                ('year_built', models.IntegerField(blank=True, null=True)),
                ('date_built', models.DateField(blank=True, null=True)),
                ('latitude', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
                ('longitude', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
                ('type', models.TextField(blank=True, null=True)),
                ('length', models.IntegerField(blank=True, null=True)),
                ('width', models.IntegerField(blank=True, null=True)),
                ('height', models.IntegerField(blank=True, null=True)),
                ('deaths', models.IntegerField(blank=True, null=True)),
                ('crew', models.IntegerField(blank=True, null=True)),
                ('built_by', models.TextField(blank=True, null=True)),
                ('can_you_visit', models.BooleanField()),
            ],
            options={
                'db_table': 'wrecks',
                'managed': True,
                'unique_together': {('ship_name', 'ship_num')},
            },
        ),
        migrations.CreateModel(
            name='Cargo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cargo_type', models.TextField(blank=True, null=True)),
                ('ship_name', models.ForeignKey(blank=True, db_column='ship_name', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='wrecks.Wrecks')),
                ('ship_num', models.ForeignKey(blank=True, db_column='ship_num', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='wrecks.Wrecks')),
            ],
            options={
                'db_table': 'cargo',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Visit',
            fields=[
                ('ship_name', models.OneToOneField(db_column='ship_name', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='wrecks.Wrecks')),
                ('num', models.IntegerField()),
                ('url', models.TextField(blank=True, null=True)),
                ('how_to_visit', models.TextField(blank=True, null=True)),
                ('ship_num', models.ForeignKey(db_column='ship_num', on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='wrecks.Wrecks')),
            ],
            options={
                'db_table': 'visit_wreck',
                'managed': True,
                'unique_together': {('ship_name', 'ship_num', 'num')},
            },
        ),
        migrations.CreateModel(
            name='Stories',
            fields=[
                ('ship_name', models.OneToOneField(db_column='ship_name', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='wrecks.Wrecks')),
                ('num', models.IntegerField()),
                ('content', models.TextField(blank=True, null=True)),
                ('ship_num', models.ForeignKey(db_column='ship_num', on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='wrecks.Wrecks')),
            ],
            options={
                'db_table': 'stories',
                'managed': True,
                'unique_together': {('ship_name', 'ship_num', 'num')},
            },
        ),
        migrations.CreateModel(
            name='References',
            fields=[
                ('ship_name', models.OneToOneField(db_column='ship_name', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='wrecks.Wrecks')),
                ('num', models.IntegerField()),
                ('url', models.TextField(blank=True, null=True)),
                ('text', models.TextField(blank=True, null=True)),
                ('ship_num', models.ForeignKey(db_column='ship_num', on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='wrecks.Wrecks')),
            ],
            options={
                'db_table': 'references',
                'managed': True,
                'unique_together': {('ship_name', 'ship_num', 'num')},
            },
        ),
        migrations.CreateModel(
            name='Photos',
            fields=[
                ('ship_name', models.OneToOneField(db_column='ship_name', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='wrecks.Wrecks')),
                ('num', models.IntegerField(blank=True, null=True)),
                ('title', models.TextField(blank=True, null=True)),
                ('photo', models.TextField(blank=True, null=True)),
                ('ship_num', models.ForeignKey(db_column='ship_num', on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='wrecks.Wrecks')),
            ],
            options={
                'db_table': 'photos',
                'managed': True,
                'unique_together': {('ship_name', 'ship_num')},
            },
        ),
        migrations.CreateModel(
            name='Path',
            fields=[
                ('ship_num', models.OneToOneField(db_column='ship_num', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, related_name='+', serialize=False, to='wrecks.Wrecks')),
                ('num', models.IntegerField()),
                ('latitude', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
                ('longitude', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
                ('ship_name', models.ForeignKey(db_column='ship_name', on_delete=django.db.models.deletion.DO_NOTHING, to='wrecks.Wrecks')),
            ],
            options={
                'db_table': 'path',
                'managed': True,
                'unique_together': {('ship_num', 'ship_name', 'num')},
            },
        ),
    ]
