from django.contrib import admin

from .models import Article

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('article_headline', 'url_name', 'website_name')
    # fields = ('article_headline', 'url_name')
    list_filter = ('website_name',)

    pass


