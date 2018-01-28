import feedparser
from datetime import datetime
import time


briefing_rss_url = "https://www.albertmohler.com/category/the-briefing/feed/"

feed = feedparser.parse(briefing_rss_url)
download_link = []

#print feed.headers
#rss_date = feed.headers['last-modified']
#print feed.headers['last-modified'].strip(" GMT")

#compare_date = datetime.strptime(rss_date.strip(" GMT"), '%a, %d %b %Y %H:%M:%S')
#print compare_date
older_time = feed.updated_parsed
newer_time = time.localtime()
print "testing area"
print feed.updated_parsed
print newer_time
if newer_time < older_time:
    print "The future is here"
if newer_time > older_time:
    print "Things make sense"
else:
    print "time is relative"
print type(feed.updated_parsed)

print "end testing area"

for item in feed.entries:
    if item["links"][1]["type"] == "audio/mpeg":
        download_link.append(item["links"][1]["href"])

for link in download_link:
    print type(link)

#TODO
#use the last build date header to get the version
# <lastBuildDate>Thu, 25 Jan 2018 18:02:26 +0000</lastBuildDate>

#encode("utf-8")

#'type': u'audio/mpeg',
#'href': u'https://mohler-media-5ox2mshyj.stackpathdns.com/Podcast/20180124_TheBriefing.mp3',
#for k, v in feed[0]:
#    print '{} : {}'.format(k, v)


