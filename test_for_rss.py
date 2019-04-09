import urllib2
from BeautifulSoup import BeautifulSoup
 
page = urllib2.urlopen("http://www.ximenavengoechea.com/")
soup = BeautifulSoup(page)
 
link = soup.find('link', type='application/rss+xml')
print link['href']
