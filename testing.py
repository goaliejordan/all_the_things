import feedparser
from datetime import datetime



briefing_rss_url = "https://www.albertmohler.com/category/the-briefing/feed/"

feed = feedparser.parse(briefing_rss_url)
download_link = []

print feed.headers
rss_date = feed.headers['last-modified']
print feed.headers['last-modified'].strip(" GMT")

compare_date = datetime.strptime(rss_date.strip(" GMT"), '%a, %d %b %Y %H:%M:%S')
print compare_date


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


