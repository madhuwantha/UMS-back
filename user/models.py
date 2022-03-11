from django.db import models
from django.utils import timezone


# Create your models here.
class User(models.Model):
    user_name = models.CharField(max_length=20)
    email = models.EmailField(max_length=20)
    device_token = models.CharField(max_length=200)
    is_premium_user = models.BooleanField(default=False)
    did_accept_to_sand_privacy_policy = models.BooleanField(default=False)
    date_accepted_to_sand_privacy_policy = models.DateTimeField()
    fire_monitoring_is_on = models.BooleanField(default=False)
    weather_monitoring_is_on = models.BooleanField(default=False)

    created = models.DateTimeField(editable=False, auto_created=True)
    modified = models.DateTimeField()

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(User, self).save(*args, **kwargs)


class Property(models.Model):
    radius = models.FloatField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    property_name = models.CharField(max_length=255)
    property_address = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    created = models.DateTimeField(editable=False, auto_created=True)
    modified = models.DateTimeField()

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(Property, self).save(*args, **kwargs)


class Notification(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    type = models.CharField(max_length=10)  # fire | weather
    distance = models.FloatField(default=0)

    created = models.DateTimeField(editable=False, auto_created=True)
    modified = models.DateTimeField()

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(Notification, self).save(*args, **kwargs)
