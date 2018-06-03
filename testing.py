import feedparser
import time


briefing_rss_url = "https://www.albertmohler.com/category/the-briefing/feed/"


def get_mp3_rss_info(rss_url):
    feed = feedparser.parse(rss_url)
    #download_links = []
    #older_time = feed.updated_parsed
    #newer_time = time.localtime()

    #if newer_time > older_time:
    #    for item in feed.entries:
    #        if item["links"][1]["type"] == "audio/mpeg":
    #            download_links.append(item["links"][1]["href"])
    #else:
    #    print "no updated podcasts to download"

    #mp3_name = download_links[0].split('/')[-1]
    #print "\nmp3 name = {}".format(mp3_name)
    print feed
    #return download_links[0], mp3_name

get_mp3_rss_info(briefing_rss_url)
#TODO
#use the last build date header to get the version
# <lastBuildDate>Thu, 25 Jan 2018 18:02:26 +0000</lastBuildDate>

#encode("utf-8")

#'type': u'audio/mpeg',
#'href': u'https://mohler-media-5ox2mshyj.stackpathdns.com/Podcast/20180124_TheBriefing.mp3',
#for k, v in feed[0]:
#    print '{} : {}'.format(k, v)

'''
location = 'f:\\temp\\test\\'





remove_month_old_os_mp3(location)
'''
