import pandas as pd
import re
import os

from requests import get
from bs4 import BeautifulSoup


def get_blog_links():
    
    url = 'https://codeup.edu/blog/'

    #user with access to webpage
    headers = {'User-Agent': 'Codeup Data Science'}

    response = get(url, headers=headers)
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    links = soup.find_all("h2")
        
    new_links = []

    for article in links:
        
        if article.find("a"):

            new_links.append(article.find("a").get("href")) 
        
    return links, new_links


def blog_titles():
    
    links, new_links = get_blog_links()
    
    titles = []
    
    for article in links:
        
        titles.append(article.get_text())
        
    titles.remove('Git Codeupdates')
        
    return titles


def blog_content():
    
    links, new_links = get_blog_links()
    
    headers = {'User-Agent': 'Codeup Data Science'}
    
    all_content = []

    for url in new_links:
        
        response = get(url, headers=headers)
    
        soup = BeautifulSoup(response.content, 'html.parser')

        content = soup.select(".entry-content")[0].find_all("p")
        
        all_content.append(content)

    clean_content = []

    for c in all_content:
        
        paragraphs = []

        for p in c:

            paragraphs.append(p.get_text())        
    
        clean_content.append(paragraphs)
    
    return clean_content


#-----------------------------------------------------

def get_blog_articles_data(refresh=False):
    
    if not os.path.isfile('blog_articles.csv') or refresh:
        
        url = 'https://codeup.com/blog/'
        headers = {'User-Agent': 'Codeup Data Science'}
        response = get(url, headers=headers)

        soup = BeautifulSoup(response.content, 'html.parser')

        links = [link['href'] for link in soup.select('h2 a[href]')]

        articles = []

        for url in links:

            url_response = get(url, headers=headers)
            soup = BeautifulSoup(url_response.text, 'html.parser')

            title = soup.find('h1', class_='entry-title').text
            content = soup.find('div', class_='entry-content').text.strip()

            article_dict = {
                'title': title,
                'content': content
            }

            articles.append(article_dict)
        
        blog_article_df = pd.DataFrame(articles)
        
        blog_article_df.to_csv('blog_articles.csv', index=False)
        
    return pd.read_csv('blog_articles.csv')


def get_news_articles_data(refresh=False):
    
    if not os.path.isfile('news_articles.csv') or refresh:
        
        url = 'https://inshorts.com/en/read'
        response = get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        categories = [li.text.lower() for li in soup.select('li')][1:]
        categories[0] = 'national'

        inshorts = []

        for category in categories:

            cat_url = url + '/' + category
            response = get(url)
            soup = BeautifulSoup(response.content, 'html.parser')

            titles = [span.text for span in soup.find_all('span', itemprop='headline')]
            contents = [div.text for div in soup.find_all('div', itemprop='articleBody')]

            for i in range(len(titles)):

                article = {
                    'title': titles[i],
                    'content': contents[i],
                    'category': category,
                }

                inshorts.append(article)
                
        inshorts_article_df = pd.DataFrame(inshorts)
        
        inshorts_article_df.to_csv('news_articles.csv', index=False)
                
    return pd.read_csv('news_articles.csv')