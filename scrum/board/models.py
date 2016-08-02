from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

class Product(models.Model):
	category = models.CharField(max_length=100)
	name = models.CharField(max_length=100)
	image = models.CharField(max_length=100)
	price = models.IntegerField(null=True)
	