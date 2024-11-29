# models.py

from django.db import models

class Gear(models.Model):
    name = models.CharField(max_length=255)
    min_trip_duration = models.IntegerField()
    max_trip_duration = models.IntegerField()
    weather_condition = models.CharField(max_length=255)
    terrain_type = models.CharField(max_length=255)
    weight = models.IntegerField()
    image_url = models.URLField(blank=True)  # Optional field for image URL

    def __str__(self):
        return self.name
