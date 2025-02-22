from django.db import models
from taggit.managers import TaggableManager


class Goods(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    tags = TaggableManager()

    def __str__(self):
        return self.name
