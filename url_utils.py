import urllib2
from BeautifulSoup import BeautifulSoup
 
def get_rss(url):
    '''get_rss() takes a web page and returns the RSS feed url or NoneType'''
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page)
    link = soup.find('link', type='application/rss+xml')
    
    if link:
        return link['href']
    else:
        return False
