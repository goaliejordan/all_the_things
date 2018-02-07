import dropbox

class MyDropBox(object):
    def __init__(self, db_token):
		self.db = self.create_dropbox_object(db_token)

	@staticmethod
    def create_dropbox_object(token):
		'''Returns a dropbox object'''
        # Check for an access token
        if not token:
            raise ValueError("ERROR: Your token is invalid. "
                             "You will need to get a token from dropbox.com.")
        else:
            print "Creating a Dropbox object..."
            return dropbox.Dropbox(token)

    def validate(self):
		'''Returns result from dropbox method users_get_current_account'''
        return self.db.users_get_current_account()


class RSSChecker(object):
    def __init__(self, url):
		self.feed = Feed(url)
		print self.feed.rss


class Feed(object):
    def __init__(self, url):
		self.url = url
		self.rss = self.get_rss(url)

	def get_rss(self):
		response = requests.get(url)
		return response
