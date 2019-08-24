from django.db import models


class Article(models.Model):
    url_name = models.URLField(max_length=1000)
    article_headline = models.CharField(max_length=1000)
    article_text = models.TextField()
    website_name = models.CharField(max_length=1000, null=True)

    def __str__(self):
        # return 'asdf'
        return "{} {}".format(self.article_headline, self.url_name, self.website_name)



