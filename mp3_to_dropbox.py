import os
import sys
import requests
import urllib
import time
from datetime import date, datetime, timedelta

import myconfig
import dropbox
from dropbox.files import WriteMode
from dropbox.exceptions import ApiError, AuthError


def ensure_url_exists(url):
    try:
        request = requests.get(url)
        request.raise_for_status()
    except requests.exceptions.HTTPError as _err:
        print _err, "The Briefing does not exist for this date."
        sys.exit(1)


def download_mp3(url, path):
    urllib.urlretrieve(url, path)


def remove_month_old_db_mp3(drop_box_object, dropbox_path_to_remove):
    # Remove mp3s that are older than 30 days from dropbox.
    present = datetime.now()
    thirty_days_ago = present - timedelta(days=30)
    entries = drop_box_object.files_list_folder(dropbox_path_to_remove)
    for entry in entries.entries:
        file_creation_time = entry.server_modified
        # delete the file
        if file_creation_time < thirty_days_ago:
            print "Deleting dropbox file {}".format(entry.name)
            drop_box_object.files_delete_v2((dropbox_path_to_remove + "/" + entry.name))


#def remove_month_old_os_mp3():
    # Remove mp3s that are older than 30 days from dropbox.
    # get files in OS and check thier time:
    #    for files in os location:
    # filecreated = os.path.getmtime("c:\\temp\\TheBriefing20180103.mp3")
    #       time.ctime(filecreated)
    #    #       if filecreated < 30_days_ago
    #       delete file
    #
    # filetime = datetime.datetime.fromtimestamp(filecreated)


def mp3_upload(drop_box_object, file_name, drop_box_path, local_mp3_file):
    # Uploads The Briefing MP3 to Dropbox
    dropbox_upload_path = str(drop_box_path).replace('\\', '/')
    with open(local_mp3_file, 'rb') as f:
        # We use WriteMode=overwrite to make sure that the settings in the file
        # are changed on upload
        print("Uploading " + file_name + " to Dropbox as " + dropbox_upload_path + "...")
        try:
            drop_box_object.files_upload(f.read(), dropbox_upload_path, mode= WriteMode('overwrite'))
        except ApiError as err:
            # This checks for the specific error where a user doesn't have
            # enough Dropbox space quota to upload this file
            if (err.error.is_path() and
                    err.error.get_path().reason.is_insufficient_space()):
                sys.exit("ERROR: Cannot back up; insufficient space.")
            elif err.user_message_text:
                print err.user_message_text
                sys.exit()
            else:
                print err
                sys.exit()


def main():
    # dropbox variables
    db_token = myconfig.db_token
    # mp3 variables
    today = str(date.today()).replace("-", "")
    file_location = "c:\\temp\\"
    file_name = "TheBriefing{}.mp3".format(today)
    local_copy_mp3 = os.path.join(file_location, file_name)
    dropbox_folder = "/TheBriefing"
    upload_path = os.path.join(dropbox_folder, file_name)

    # get the url with the date.
    mp3_url = "https://mohler-media-5ox2mshyj.stackpathdns.com/Podcast/{}_TheBriefing.mp3".format(today)
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
    download_mp3(mp3_url, local_copy_mp3)

    # Upload mp3 to dropbox
    mp3_upload(dbx, file_name, upload_path, local_copy_mp3)

    # Remove 30 day old files from dropbox
    remove_month_old_db_mp3(dbx, dropbox_folder)

    print "Done!"


if __name__ == '__main__':
    main()


# help = 'https://discourse.mcneel.com/t/python-variables-and-arguments-best-practices/31440/3'

