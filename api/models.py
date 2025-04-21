from django.db import models


class Address(models.Model):
    label = models.CharField(max_length=200)
    housenumber = models.IntegerField()
    street = models.CharField(max_length=200)
    postcode = models.CharField(max_length=5)
    citycode = models.CharField(max_length=5)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    def __str__(self):
        return self.label
