from django.contrib.gis.db import models


class Battle(models.Model):
    name = models.CharField(max_length=255)
    wiki_link = models.URLField(max_length=255)
    date = models.CharField(max_length=100)
    point = models.PointField()

    def __str__(self):
        return self.name
