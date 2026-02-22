from django.db import models


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class City(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True)
    country = models.CharField(max_length=120, default='Kazakhstan')

    class Meta:
        ordering = ['name']

    def __str__(self) -> str:
        return f"{self.name}" 
