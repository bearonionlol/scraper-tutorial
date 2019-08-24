from django.core.management.base import BaseCommand
from scraper.models import Article
from requests_html import HTMLSession
import sqlite3
from sqlite3 import Error

def get_session(url, selector):
    session = HTMLSession()
    r = session.get(url)
    #r.html.render()
    return r.html.find(selector)


def create_connection(scraper_article):
    
    try:
        conn = sqlite3.connect(scraper_article)
        return conn
    except Error as e:
        print(e)

    return None


def prevent_duplicates(conn):
    headline = ['headline']
    url = ['url']

    # Create cursor object
    cur = conn.db.cursor()

    # run a select query against the table to see if any record exists
    # that has the email or username
    cur.execute("""SELECT headline
                          ,url
                   FROM scraper_article
                   WHERE headline=?
                       OR url=?""",
                (headline, url))

    result = cur.fetchall()

    if result:
        pass
    else:
        cur.execute("INSERT INTO scraper_article VALUES (?, ?)", (headline, url))
        conn.db.commit()


def save_article(article):
    headline = article['headline']
    url = article['url']
    article_body = article['article_body']
    website_name = article['website_name']
    art = Article()

    database = "C:\\sqlite\db\pythonsqlite.db"

    # create a database connection
    conn = create_connection(database)
    with conn:
        prevent_duplicates(conn)

    print("Saving article {} {}".format(headline, url))

    """
        url_name = models.URLField(max_length=1000)
        article_headline = models.CharField(max_length=1000)
        article_text = models.TextField()

    """

    print("Saving article {} {}".format(headline, url))

    art.article_headline = headline
    art.url_name = url
    art.article_text = article_body
    art.website_name = website_name
    art.save()
    prevent_duplicates(conn)


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
            'article_body': article_body,
            'website_name': 'CNBC'
        }

        print("fetched {}".format(url))

        all_articles.append(out)

        counter += 1

            # if counter > 5:
            #     break

    for a in all_articles:
        # headline = a['headline']
        # url = a['url']
        # article_body = a['article_body']
        # art = Article()
        #
        # """
        #     url_name = models.URLField(max_length=1000)
        #     article_headline = models.CharField(max_length=1000)
        #     article_text = models.TextField()
        #
        # """



        save_article(a)


        # art.article_headline = headline
        # art.url_name = url
        # art.article_text = article_body
        # art.save()

        # print('Headline: {} URL: {}'.format(headline, a['url']))
        #
        # print("Article Body: \n\n\n\n\n\n\n{}".format(article_body))


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
            'article_body': article_body,
            'website_name': 'Market Watch'
        }

        all_articles.append(out)

        counter += 1

        if counter > 5:
            break

    for a in all_articles:
        save_article(a)


        # headline = a['headline']
        # url = a['url']
        # article_body = a['article_body']
        # art = Article()
        #
        # art.headline = headline
        # art.url = url
        # art.body = article_body
        # art.save()

        # # print('Headline: {} URL: {}'.format(headline, a['url']))
        #
        # print("Article Body: \n{}\n\n".format(article_body))
        #
        # scraper_data = Article.objects.all()
        # for data in scraper_data:
        #     data.url_name = url
        #     data.article_headline = headline
        #     data.article_text = article_body
        #     data.save()


class Command(BaseCommand):
    def handle(self, **options):
        run_scraper()
        run_scraper2()



