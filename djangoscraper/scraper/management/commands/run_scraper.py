from django.core.management.base import BaseCommand
from scraper.models import Article
from requests_html import HTMLSession

def get_session(url, selector):
    session = HTMLSession()
    r = session.get(url)
    r.html.render()
    return r.html.find(selector)

def run_scraper():

    articles = get_session('https://www.cnbc.com', '.Card-titleContainer a')

    article_links = []

    for article in articles:
        headline = article.text

        article_link = article.find('a', first=True).attrs['href']

        if article_link.startswith('http'):
            url = article_link
        # print(headline, url)

        article_links.append((headline, url,))


    all_articles = []

    counter = 0

    for headline, url in article_links:

        articletext = get_session(url, 'div.ArticleBody-articleBody')

        article_body = None

        for article in articletext:
            article_body = article.text

        out = {
            'headline': headline,
            'url': url,
            'article_body': article_body
        }

        all_articles.append(out)

        counter += 1

        if counter > 5:
            break

    for a in all_articles:
        headline = a['headline']
        url = a['url']
        article_body = a['article_body']

        print('Headline: {} URL: {}'.format(headline, a['url']))

        print("Article Body: \n\n\n\n\n\n\n{}".format(article_body))


def run_scraper2():

    articles = get_session('https://www.marketwatch.com', '.article__headline a')[1:]

    article_links = []

    for article in articles:
        headline = article.text

        article_link = article.find('a', first=True).attrs['href']

        if article_link.startswith('http'):
            url = article_link
        # print(headline, url)

        article_links.append((headline, url,))


    all_articles = []

    counter = 0

    for headline, url in article_links:

        articletext = get_session(url, '#article-body')

        article_body = None

        for article in articletext:
            article_body = article.text

        out = {
            'headline': headline,
            'url': url,
            'article_body': article_body
        }

        all_articles.append(out)

        counter += 1

        if counter > 5:
            break

    for a in all_articles:
        headline = a['headline']
        url = a['url']
        article_body = a['article_body']

        print('Headline: {} URL: {}'.format(headline, a['url']))

        print("Article Body: \n{}\n\n".format(article_body))

        scraper_data = Article.objects.all()
        for data in scraper_data:
            data.url_name = url
            data.article_headline = headline
            data.article_text = article_body
            data.save()


class Command(BaseCommand):
    def handle(self, **options):
        run_scraper()
        run_scraper2()



