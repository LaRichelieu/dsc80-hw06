import os
import pandas as pd
import numpy as np
import requests
import bs4
import time

# ---------------------------------------------------------------------
# Question # 1
# ---------------------------------------------------------------------

# None

# ---------------------------------------------------------------------
# Question # 2
# ---------------------------------------------------------------------

def answers():
    """
    Returns two lists with your answers
    :return: Two lists: one with your answers to multiple choice questions
    and the second list has 6 websites that satisfy given requirements.
    >>> list1, list2 = answers()
    >>> len(list1)
    4
    >>> len(list2)
    6
    """
    r1 = [1,2,1,1]
    r2 = ["http://dsc.ucsd.edu","https://www.google.ca","https://slate.com","https://www.instagram.com/","https://www.gradescope.com/","https://facebook.com/"]
    return r1,r2

# ---------------------------------------------------------------------
# Question # 3
# ---------------------------------------------------------------------


def find_countries(url):
    """
    Scrapes the site to extract the name of the countries.
    :param url:
    :return: dataframe with all countries listed in a column
    >>> url = "http://example.webscraping.com/"
    >>> df = find_countries(url)
    >>> df.shape
    (252, 1)
    """
    countries = []
    r = requests.get(url)
    urlText = r.text
    while True:
        soup = bs4.BeautifulSoup(urlText, 'html.parser')
    
        for i in soup.find('table').find_all('a'):
            countries.append(i.get_text().strip())
        
        nexturl = soup.find('div', attrs={'id': 'pagination'}).find('a',text='Next >')

        if nexturl == None:
            break
        else:
            r = requests.get(url + nexturl.attrs.get('href'))
            urlText = r.text
            time.sleep(5)

    df = pd.DataFrame(countries, columns = ['Countries'])
    return df


def first_letters_count(df):
    """
    Counts number of countries that begin with the same letter
    :param df:
    :return: dataframe, indexed by a capital letter and the column
             containing the number of countries starting from this letter

    :Example:
    >>> fp = os.path.join('data', 'countries-sample.csv')
    >>> df = pd.read_csv(fp)
    >>> counts = first_letters_count(df)
    >>> counts.shape
    (7, 1)
    """
    df.loc[:,'Start Letter'] = df.iloc[:,0].apply(lambda x: x[0:1])
    unsorted = df.groupby('Start Letter').count()
    return unsorted.iloc[:,[0]].sort_values(unsorted.columns[0], ascending = False)


# ---------------------------------------------------------------------
# Question # 4
# ---------------------------------------------------------------------


def extract_book_links(text):
    """
    :Example:
    >>> fp = os.path.join('data', 'products.html')
    >>> out = extract_book_links(open(fp).read())
    >>> url = 'scarlet-the-lunar-chronicles-2_218/index.html'
    >>> out[0] == url
    True
    """
    result = []
    soup = bs4.BeautifulSoup(text, 'html.parser')
    books = soup.find('section').find_all('div')[1:][0].find_all('article')
    for i in books:
        attributes = i.find_all('p')
        if attributes[0].attrs.get('class')[1] == 'Four' or attributes[0].attrs.get('class')[1] == 'Five':
            if float(attributes[1].text[-5:])<=20:
                result.append(i.find('h3').find('a').attrs.get('href'))
    return result


def get_product_info(text):
    """
    :Example:
    >>> fp = os.path.join('data', 'Frankenstein.html')
    >>> out = get_product_info(open(fp).read())
    >>> isinstance(out, dict)
    True
    >>> 'UPC' in out.keys()
    True
    >>> out['Rating']
    'Two'
    """
    result = {}
    soup = bs4.BeautifulSoup(text, 'html.parser')
    main_info = soup.find('div', attrs={'class':'product_main'})
    result['Title'] = main_info.find('h1').text
    result['Rating'] = main_info.find('p', attrs={'class':'star-rating'}).attrs.get('class')[1]

    product_info = soup.find('table', attrs={'class':'table table-striped'}).find_all('tr')
    result['UPC'] = product_info[0].find('td').text
    result['Product Type'] = product_info[1].find('td').text
    result['Price (excl. tax)'] = product_info[2].find('td').text
    result['Price (incl. tax)'] = product_info[3].find('td').text
    result['Tax'] = product_info[4].find('td').text
    result['Availability'] = product_info[5].find('td').text
    result['Number of reviews'] = product_info[6].find('td').text
    result['Description'] = soup.find_all('p')[3].text
    return result


def scrape_books(k):
    """
    :param k: number of book-listing pages to scrape.
    :returns: a dataframe of information on (certain) books
    on the k pages (as described in the question).

    :Example:
    >>> out = scrape_books(1)
    >>> out.shape
    (1, 10)
    >>> out['Rating'][0] == 'Five'
    True
    >>> out['UPC'][0] == 'ce6396b0f23f6ecc'
    True
    """
    base = 'http://books.toscrape.com/catalogue/'
    url = 'http://books.toscrape.com/catalogue/page-1.html'
    r = requests.get(url)
    urlText = r.text
    
    pages_read = 0
    bookurls = []

    while k > pages_read:
        soup = bs4.BeautifulSoup(urlText, 'html.parser')

        bookurls += extract_book_links(urlText)
        pages_read += 1
        
        if pages_read < 50:
            r = requests.get(base + soup.find('li', attrs = {'class':'next'}).find('a').attrs.get('href'))
            urlText = r.text

    results = []
    for i in bookurls:
        book = requests.get(base + i)
        bookText = book.text
        results.append(get_product_info(bookText))
    
    return pd.DataFrame(results, columns = ['Availability', 'Number of reviews', 'Price (excl. tax)', 'Price (incl. tax)',
        'Product Type', 'Tax', 'UPC', 'Description', 'Rating', 'Title'])

# ---------------------------------------------------------------------
# Question # 5
# ---------------------------------------------------------------------


def depth(comments):
    """
    
    :Example:
    >>> fp = os.path.join('data', 'comments.csv')
    >>> comments = pd.read_csv(fp, sep='|')
    >>> (depth(comments) == [1, 2, 2, 3, 4, 1, 2, 1]).all()
    True
    """

    return ...


def descendants(comments):
    """
    
    :Example:
    >>> fp = os.path.join('data', 'comments.csv')
    >>> comments = pd.read_csv(fp, sep='|')
    >>> (descendants(comments) == [4, 0, 2, 1, 0, 1, 0, 0]).all()
    True
    """

    return ...


def distinct_descendants(comments):
    """
    
    :Example:
    >>> fp = os.path.join('data', 'comments.csv')
    >>> comments = pd.read_csv(fp, sep='|')
    >>> (distinct_descendants(comments) == [3, 0, 2, 1, 0, 1, 0, 0]).all()
    True
    """

    return ...

# ---------------------------------------------------------------------
# DO NOT TOUCH BELOW THIS LINE
# IT'S FOR YOUR OWN BENEFIT!
# ---------------------------------------------------------------------


# Graded functions names! DO NOT CHANGE!
# This dictionary provides your doctests with
# a check that all of the questions being graded
# exist in your code!

GRADED_FUNCTIONS = {
    'q01': [],
    'q02': ['answers'],
    'q03': ['find_countries', 'first_letters_count'],
    'q04': ['extract_book_links', 'get_product_info', 'scrape_books'],
    'q05': ['depth', 'descendants', 'distinct_descendants']
}


def check_for_graded_elements():
    """
    >>> check_for_graded_elements()
    True
    """
    
    for q, elts in GRADED_FUNCTIONS.items():
        for elt in elts:
            if elt not in globals():
                stmt = "YOU CHANGED A QUESTION THAT SHOULDN'T CHANGE! \
                In %s, part %s is missing" %(q, elt)
                raise Exception(stmt)

    return True
