from dropbox.exceptions import AuthError
import dropbox
import feedparser


class MyDropBox(object):

    def __init__(self, db_token):
        self.db = self.create_dropbox_object(db_token)

    @staticmethod
    def create_dropbox_object(token):
        # Check for an access token
        if not token:
            raise ValueError("ERROR: Your token is invalid. "
                             "You will need to get a token from dropbox.com.")
        else:
            print "Creating a Dropbox object..."
            return dropbox.Dropbox(token)

    def validate(self):
        try:
            return self.db.users_get_current_account()
        except AuthError as error:
            print error
            return 1


class MP3Feed(object):
    def __init__(self, url):
        self.url = url

    @staticmethod
    def iter_mp3_links(feed, last_updated):
        for e in feed.entries:
            if last_updated or e.updated_parsed > last_updated:
                for l in e.links:
                    if l.type == 'audio/mpeg':
                        yield l.href

    def iter_mp3_download_links(self, since=None):
        feed = feedparser.parse(self.url)

        if since and feed.updated_parsed >= since:
            print "no updated podcasts to download"
            return

        for link in iter_mp3_links(feed, last_updated):
            mp3_name = link.split('/')[-1]
            yield mp3_name, link, timestamp



with open(last_update_path) as file_:
    last_update = pickle.load(file_)

mp3feed = MP3Feed(url)
for name, link in mp3feed.iter_mp3_download_links(last_update):
    download(name, link)

with open(last_update_path, 'wb') as file_:
    pickle.dump(feed.updated_parsed, file_)


