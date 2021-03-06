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


def download_mp3(url, path):
    '''Download the mp3 from the ULR pull and place in selected path.'''
    request = requests.get(url)
    with open(path, 'wb') as file_:
        file_.write(request.content)


def is_old(ds, days):
    return ds < datetime.now() - timedelta(days=days)


def remove_old_db_mp3(drop_box_object, dropbox_path_to_remove, days=30):
    '''Remove mp3s that are older than 30 days from dropbox.'''
    result = drop_box_object.files_list_folder(dropbox_path_to_remove)
    for entry in result.entries:
        creation_time = entry.server_modified
        if is_old(creation_time, days):
            print "Deleting dropbox file {}".format(entry.name)
            removal_path = '{}/{}'.format(dropbox_path_to_remove, entry.name)
            drop_box_object.files_delete_v2(removal_path)


def remove_old_os_mp3(dir_, days=30):
    # get files in OS and check thier time:
    for mp3_file in os.listdir(dir_):
        path = os.path.join(dir_, mp3_file)
        creation_time = os.path.getctime(path)
        if is_old(datetime.fromtimestamp(creation_time), days):
            try:
                os.remove(path)
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

def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Download an MP3 and upload it to the cloud.')
    parser.add_argument('--cloud-host', '-n',
                        type=str,
                        dest='cloud_host',
                        default='dropbox',
                        help='Name of cloud service to upload to.'
                             ' Options: dropbox, google, onedrive.'
                             ' Default: dropbox')
    parser.add_argument('--past-mp3-count', '-p',
                        type=int,
                        dest='past_mp3_count',
                        default='1',
                        help='Number of days for historical mp3 download')
    parser.add_argument('--reference-email', '-e', type=str, nargs='+',
                        dest='reference_email',
                        help='email address of reference(s)')

    args = parser.parse_args()
    #cloud_host_name = args.cloud_host
    return args


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
    mp3_url = ("https://mohler-media-5ox2mshyj.stackpathdns.com/Podcast/"
               "{}_TheBriefing.mp3".format(today))

    # Verify that the mp3 url is valid.
    if not requests.get(mp3_url).ok:
        print "Download link not available"
        return 1

    # Check for an access token
    # Checking if list or string is empty should be done like this
    if not db_token:
        print "ERROR: Looks like you didn't add your access token. \
               You will need to get this token from dropbox.com."
        return 1
    # Create an instance of a Dropbox class, which can make requests to the API
    print "Creating a Dropbox object..."
    dbx = dropbox.Dropbox(db_token)

    # Check that the access token is valid
    try:
        dbx.users_get_current_account()
    except AuthError as err:
        print err, "ERROR: Invalid access token; try re-generating an "\
                 "access token from the app console on the web."
        return 1

    # Download local copy of mp3
    download_mp3(mp3_url, local_copy_mp3)

    # Upload mp3 to dropbox
    mp3_upload(dbx, file_name, upload_path, local_copy_mp3)

    # Remove 30 day old files from dropbox
    remove_old_db_mp3(dbx, dropbox_folder)

    # Remove 30 day old files from OS location
    remove_old_os_mp3(file_location)

    print "Done!"


if __name__ == '__main__':

    sys.exit(main())
