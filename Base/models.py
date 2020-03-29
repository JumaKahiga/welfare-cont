from django.db import models

from cloudinary.models import CloudinaryField


class Person(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    avatar = CloudinaryField("image", default="image/upload/v1551960935/books.png")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
        app_label = 'members'
