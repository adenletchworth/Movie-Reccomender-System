import re
from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
from nltk.tokenize import word_tokenize
import web_scraper

class MovieScraper:
    def __init__(self, url):
        self.url = url
        self.movie_attributes = {}

    def find_movie_attributes(self):

        # connect to the url
        movie_Scrape = requests.get(self.url)

        # get content of the page
        movie_html_Content = movie_Scrape.text

        # connect BeautifulSoup scraper
        soup = BeautifulSoup(movie_html_Content, 'lxml')

        # get the conent we are interested in
        movie_attributes_r = soup.find_all('span', class_='info-item-value')
        movie_labels_r = soup.find_all('b', class_='info-item-label')
        movie_name_r = soup.find('h1',class_='title')
        movie_description = soup.find('p',{'data-qa':'movie-info-synopsis'})

        self.movie_attributes['URL'] = self.url
        self.movie_attributes['Title'] = movie_name_r.text
        self.movie_attributes['Description'] = movie_description.text

        # forms text and adds to movie_attributes list
        for label, attribute in zip(movie_labels_r, movie_attributes_r):
            label_text = label.text.replace(':','').strip()
            attribute_text = re.sub(r'\s+', ' ', attribute.text.strip())
            self.movie_attributes[label_text] = attribute_text


    def print_movie_attributes(self):
        for label, attribute in self.movie_attributes.items():
            print(f"{label}: {attribute}")

class UrlFinder:
    def __init__(self,movie_url_page):
        self.movie_url_page = movie_url_page
        self.url_Ending = set()

    def __getitem__(self):

        url_Scrape = requests.get(self.movie_url_page)

        url_Text = url_Scrape.content


        soup = BeautifulSoup(url_Text,'lxml')

        url_List = soup.find_all('a',{'data-track':'scores'})

        for url in url_List:
            self.url_Ending.add(url['href'])
            time.sleep(1)

def UrlPredictor(title_input):
    title = word_tokenize(title_input)
    filter_ = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
    filtered_title = [word.lower() for word in title if word not in filter_]
    url = '_'.join(filtered_title)
    return 'https://www.rottentomatoes.com/m/' + url


""""
url1 = 'https://www.rottentomatoes.com/browse/movies_at_home/?page=100'
url2 = 'https://www.rottentomatoes.com/browse/movies_in_theaters/?page=100'
url3 = 'https://www.rottentomatoes.com/browse/movies_coming_soon/'

urls = UrlFinder(url1)

url_Set = urls.get()

df = pd.DataFrame()

for url_end in urls.url_Ending:
    url = 'https://www.rottentomatoes.com' + url_end
    scrape = MovieScraper(url)
    scrape.find_movie_attributes()
    movie_attributes = scrape.movie_attributes

    # Add the keys to the columns list if not already present
    for key in movie_attributes.keys():
        if key not in df.columns:
            df[key] = ""

    # Append the values to the corresponding columns
    df = df._append(movie_attributes, ignore_index=True)

df.to_csv('movies_in_home.csv', index=False)



url_guess = UrlPredictor('IT (2017)')

movie_guess = MovieScraper(url_guess)

movie_guess.find_movie_attributes()

print(movie_guess.movie_attributes)

"""






