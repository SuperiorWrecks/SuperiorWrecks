# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = True` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Wrecks(models.Model):
    ship_name = models.CharField(primary_key=True, max_length=255)
    ship_num = models.CharField(max_length=255)
    year_sunk = models.IntegerField(blank=True, null=True)
    date_sunk = models.DateField(blank=True, null=True)
    year_built = models.IntegerField(blank=True, null=True)
    date_built = models.DateField(blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    type = models.TextField(blank=True, null=True)
    length = models.IntegerField(blank=True, null=True)
    width = models.IntegerField(blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)
    deaths = models.IntegerField(blank=True, null=True)
    crew = models.IntegerField(blank=True, null=True)
    built_by = models.TextField(blank=True, null=True)
    can_you_visit = models.BooleanField(default=False)

    class Meta:
        managed = True
        db_table = 'wrecks'
        unique_together = (('ship_name', 'ship_num'),)


class Cargo(models.Model):
    ship_name = models.ForeignKey('Wrecks', models.DO_NOTHING, db_column='ship_name', blank=True, null=True)
    ship_num = models.ForeignKey('Wrecks', models.DO_NOTHING, db_column='ship_num', blank=True, null=True,
                                 related_name="+")
    cargo_type = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'cargo'


class Path(models.Model):
    ship_name = models.ForeignKey('Wrecks', models.DO_NOTHING, db_column='ship_name')
    ship_num = models.OneToOneField('Wrecks', models.DO_NOTHING, db_column='ship_num', primary_key=True,
                                    related_name="+")
    num = models.IntegerField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'path'
        unique_together = (('ship_num', 'ship_name', 'num'),)


class Photos(models.Model):
    ship_name = models.OneToOneField('Wrecks', models.DO_NOTHING, db_column='ship_name', primary_key=True)
    ship_num = models.ForeignKey('Wrecks', models.DO_NOTHING, db_column='ship_num', related_name="+")
    num = models.IntegerField(blank=True, null=True)
    title = models.TextField(blank=True, null=True)
    photo = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'photos'
        unique_together = (('ship_name', 'ship_num'),)


class References(models.Model):
    ship_name = models.OneToOneField('Wrecks', models.DO_NOTHING, db_column='ship_name', primary_key=True)
    ship_num = models.ForeignKey('Wrecks', models.DO_NOTHING, db_column='ship_num', related_name="+")
    num = models.IntegerField()
    url = models.TextField(blank=True, null=True)
    text = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'references'
        unique_together = (('ship_name', 'ship_num', 'num'),)


class Visit(models.Model):
    ship_name = models.OneToOneField('Wrecks', models.DO_NOTHING, db_column='ship_name', primary_key=True)
    ship_num = models.ForeignKey('Wrecks', models.DO_NOTHING, db_column='ship_num', related_name="+")
    num = models.IntegerField()
    url = models.TextField(blank=True, null=True)
    how_to_visit = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'visit_wreck'
        unique_together = (('ship_name', 'ship_num', 'num'),)


class Stories(models.Model):
    ship_name = models.OneToOneField('Wrecks', models.DO_NOTHING, db_column='ship_name', primary_key=True)
    ship_num = models.ForeignKey('Wrecks', models.DO_NOTHING, db_column='ship_num', related_name="+")
    num = models.IntegerField()
    content = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'stories'
        unique_together = (('ship_name', 'ship_num', 'num'),)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favorite_ships = models.ManyToManyField(Wrecks)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
