#!/usr/bin/env python2.7

'''
Downloads a mp3 from a URL and uploads it to DropBox
    also removes mp3 that are older to 30 days to save space.
'''

import os
import sys
from datetime import date, datetime, timedelta
import requests

import dropbox
from dropbox.files import WriteMode
from dropbox.exceptions import ApiError, AuthError
import myconfig


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


def download_mp3(url, path):
    '''Download the mp3 from the ULR pull and place in selected path.'''
    request = requests.get(url)
    with open(path, 'wb') as file_:
        file_.write(request.content)


def remove_month_old_db_mp3(drop_box_object, dropbox_path_to_remove):
    ''' Remove mp3s that are older than 30 days from dropbox.'''
    present = datetime.now()
    thirty_days_ago = present - timedelta(days=30)
    entries = drop_box_object.files_list_folder(dropbox_path_to_remove)
    for entry in entries.entries:
        file_creation_time = entry.server_modified
        # delete the file
        if file_creation_time < thirty_days_ago:
            print "Deleting dropbox file {}".format(entry.name)
            removal_path = '{}/{}'.format(dropbox_path_to_remove, entry.name)
            drop_box_object.files_delete_v2(removal_path)


def remove_month_old_os_mp3(file_location):
    ''' Get files in OS and remove them is they are older than 30 days.'''
    present = datetime.now()
    thirty_days_ago = present - timedelta(days=30)
    mp3_files = os.listdir(file_location)
    for mp3_file in mp3_files:
        file_full_path = os.path.join(file_location, mp3_file)
        file_creation_time = os.path.getctime(file_full_path)
        if datetime.fromtimestamp(file_creation_time) < thirty_days_ago:
            try:
                os.remove(file_full_path)
            except Exception as error:
                return error


def mp3_upload(drop_box_object, file_name, drop_box_path, local_mp3_file):
    '''Uploads downloaded MP3 to Dropbox.'''
    dropbox_upload_path = str(drop_box_path).replace('\\', '/')
    with open(local_mp3_file, 'rb') as file_:
        # We use WriteMode=overwrite to make sure that the settings in the file
        # are changed on upload
        print "Uploading {} to Dropbox as {} ...".format(file_name,
                                                         dropbox_upload_path)
        try:
            drop_box_object.files_upload(
                file_.read(),
                dropbox_upload_path,
                mode=WriteMode('overwrite'))
        except ApiError as err:
            # This checks for the specific error where a user doesn't have
            # enough Dropbox space quota to upload this file
            if (err.error.is_path() and
                    err.error.get_path().reason.is_insufficient_space()):
                print "ERROR: Cannot back up; insufficient space."
                return 1
            elif err.user_message_text:
                print err.user_message_text
                return 1
            else:
                print err
                return 1


def main():
    '''Runs all the things to make them work.'''
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

    # Verify that the mp3 url is valid.
    if not requests.get(mp3_url).ok:
        print "Download link not available"
        return 1


    dbx = MyDropBox(db_token)

    # Check that the access token is valid
    dbx.validate()

    # Download local copy of mp3
    download_mp3(mp3_url, local_copy_mp3)

    # Upload mp3 to dropbox
    mp3_upload(dbx, file_name, upload_path, local_copy_mp3)

    # Remove 30 day old files from dropbox
    remove_month_old_db_mp3(dbx, dropbox_folder)

    # Remove 30 day old files from OS location
    remove_month_old_os_mp3(file_location)

    print "Done!"


if __name__ == '__main__':
    sys.exit(main())


