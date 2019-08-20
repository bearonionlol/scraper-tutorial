from django.db import models


class Article(models.Model):
    url_name = models.URLField(max_length=1000)
    article_headline = models.CharField(max_length=1000)
    article_text = models.TextField()

    def __str__(self):
        # return 'asdf'
        return "{} {}".format(self.article_headline, self.url_name)
