from django.db import models


class Article(models.Model):
    url_name = models.URLField(max_length=300)
    article_headline = models.CharField(max_length=200)
    aricle_body = models.TextField()