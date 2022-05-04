from django.db import models


class Battle(models.Model):
    name = models.CharField(max_length=250)
    wiki_link = models.URLField(max_length=250)
    date = models.CharField(max_length=250)
    latitude = models.CharField(max_length=100)
    longitude = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}: {self.date}"

    def is_valid_coordinates(self):
        lat = float(self.latitude)
        lng = float(self.longitude)
        return -90 < lat < 90 and -180 < lng < 180
