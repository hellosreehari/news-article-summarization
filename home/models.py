from django.db import models

# Create your models here.
class News(models.Model):
    title = models.CharField(max_length=1000, null=True)
    summary = models.TextField(null=True)
    article_url = models.CharField(max_length=1000, null=True)
    image_url = models.CharField(max_length=1000, null=True)
    date_published = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
       return self.title
