from django.core.management.base import BaseCommand, CommandError
from scraper.models import Article


class Command(BaseCommand):
    def handle(self, **options):
        exec(open('/home/shiva/code/scraper/comb_scrape.py').read())
        article = Article.objects.get()
        article.opened = True
        article.save()