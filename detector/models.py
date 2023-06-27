from django.db import models

# Create your models here.

class Team(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField()
    linkedin = models.URLField(default="https://www.linkedin.com/feed/")

    def __str__(self):
        return self.name


