import dropbox
import urllib
import urllib2
from datetime import date
from dropbox.files import WriteMode
from dropbox.exceptions import ApiError, AuthError
import sys

# dropbox variables
ap_key = ""
ap_secret = ""
db_token = ""

# mp3 variables
today = str(date.today()).replace("-", "")
file_location = "c:\\temp\\"
file_name = "TheBriefing%s.mp3" % today
local_copy_mp3 = file_location + file_name
dropbox_folder = "/TheBriefing"
upload_path = (dropbox_folder + "/" + file_name)

# get the url with the date.
mp3_url = "https://mohler-media-5ox2mshyj.stackpathdns.com/Podcast/%s_TheBriefing.mp3" % today


def ensure_url_exists(url):
    try:
        urllib2.urlopen(url)
    except urllib2.HTTPError, e:
        return e.code, "The Briefing does not exist for that date."
    except urllib2.URLError, e:
        return e.args, "Unable to retrieve The Briefing MP3."


def download_mp3():
    urllib.urlretrieve(mp3_url, local_copy_mp3)

# Uploads The Briefing MP3 to Dropbox


def mp3_upload():
    with open(local_copy_mp3, 'rb') as f:
        # We use WriteMode=overwrite to make sure that the settings in the file
        # are changed on upload
        print("Uploading " + file_name + " to Dropbox as " + upload_path + "...")
        try:
            dbx.files_upload(f.read(), upload_path, mode=WriteMode('overwrite'))
        except ApiError as err:
            # This checks for the specific error where a user doesn't have
            # enough Dropbox space quota to upload this file
            if (err.error.is_path() and
                    err.error.get_path().reason.is_insufficient_space()):
                sys.exit("ERROR: Cannot back up; insufficient space.")
            elif err.user_message_text:
                print(err.user_message_text)
                sys.exit()
            else:
                print(err)
                sys.exit()

# connect to dropbox account


if __name__ == '__main__':
    # Check for an access token
    if len(db_token) == 0:
        sys.exit("ERROR: Looks like you didn't add your access token. "
            "You will need to get this token from dropbox.com.")

    # Create an instance of a Dropbox class, which can make requests to the API.
    print("Creating a Dropbox object...")
    dbx = dropbox.Dropbox(db_token)

    # Check that the access token is valid
    try:
        dbx.users_get_current_account()
    except AuthError as err:
        sys.exit("ERROR: Invalid access token; try re-generating an "
                 "access token from the app console on the web.")

    # Verify that the mp3 url is valid.
    ensure_url_exists(mp3_url)

    # Download local copy of mp3
    download_mp3()

    # Upload mp3 to dropbox
    mp3_upload()

    # Remove 30 day old files from dropbox

    print("Done!")
