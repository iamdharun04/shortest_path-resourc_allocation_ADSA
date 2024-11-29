# Example models in tourplan/models.py

from django.db import models

class City(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.name

class TouristAttraction(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.name

class Trip(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    attractions = models.ManyToManyField(TouristAttraction)

    def __str__(self):
        return self.name
# models.py

from django.db import models

class TouringPlace(models.Model):
    name = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    city = models.CharField(max_length=100)

    def __str__(self):
        return self.name
