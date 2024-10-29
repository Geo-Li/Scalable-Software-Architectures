import requests  # calling web service
import jsons  # relational-object mapping

import uuid
import pathlib
import logging
import base64

# doesn't work in docker (not easily):
import matplotlib.pyplot as plt
import matplotlib.image as img

from models import *
from helpers import *


###################################################################
#
# stats
#
def stats(baseurl):
    """
    Prints out S3 and RDS info: bucket status, # of users and
    assets in the database

    Parameters
    ----------
    baseurl: baseurl for web service

    Returns
    -------
    nothing
    """

    try:
        # call the web service:
        api = "/stats"
        url = baseurl + api

        res = web_service_get(url)

        if res.status_code != 200:
            # failed:
            print("Failed with status code:", res.status_code)
            print("url: " + url)
            if res.status_code in [400, 500]:  # we'll have an error message
                body = res.json()
                print("Error message:", body["message"])
            return

        # deserialize and extract stats:
        body = res.json()
        print("bucket status:", body["message"])
        print("# of users:", body["db_numUsers"])
        print("# of assets:", body["db_numAssets"])

    except Exception as e:
        logging.error("stats() failed:")
        logging.error("url: " + url)
        logging.error(e)
        return


###################################################################
#
# users
#
def users(baseurl):
    """
    Prints out all the users in the database

    Parameters
    ----------
    baseurl: baseurl for web service

    Returns
    -------
    nothing
    """

    try:
        # call the web service:
        api = "/users"
        url = baseurl + api

        res = web_service_get(url)

        if res.status_code != 200:
            # failed:
            print("Failed with status code:", res.status_code)
            print("url: " + url)
            if res.status_code in [400, 500]:  # we'll have an error message
                body = res.json()
                print("Error message:", body["message"])
            return

        # deserialize and extract users:
        body = res.json()
        # let's map each dictionary into a User object:
        users = []
        for row in body["data"]:
            user = jsons.load(row, User)
            users.append(user)

        # Now we can think OOP:
        for user in users:
            print(user.userid)
            print(" ", user.email)
            print(" ", user.lastname, ",", user.firstname)
            print(" ", user.bucketfolder)

    except Exception as e:
        logging.error("users() failed:")
        logging.error("url: " + url)
        logging.error(e)
        return


###################################################################
#
# assets
#
def assets(baseurl):
    """
    Prints out all the assets in the database

    Parameters
    ----------
    baseurl: baseurl for web service

    Returns
    -------
    nothing
    """

    try:
        # call the web service:
        api = "/assets"
        url = baseurl + api

        res = web_service_get(url)

        if res.status_code != 200:
            # failed:
            print("Failed with status code:", res.status_code)
            print("url: " + url)
            if res.status_code in [400, 500]:  # we'll have an error message
                body = res.json()
                print("Error message:", body["message"])
            return

        # deserialize and extract assets:
        body = res.json()
        # let's map each dictionary into an Asset object:
        assets = []
        for row in body["data"]:
            asset = jsons.load(row, Asset)
            assets.append(asset)

        # Now we can think OOP:
        for asset in assets:
            print(asset.assetid)
            print(" ", asset.userid)
            print(" ", asset.assetname)
            print(" ", asset.bucketkey)

    except Exception as e:
        logging.error("assets() failed:")
        logging.error("url: " + url)
        logging.error(e)
        return


###################################################################
#
# download
#
def download(baseurl, display=False, host=None):
    """
    Prompts the user for an asset id, and downloads
    that asset (image) from the bucket. Displays the
    image after download if display param is True.

    Parameters
    ----------
    baseurl: baseurl for web service,
    display: optional param controlling display of image

    Returns
    -------
    nothing
    """

    try:
        print("Enter asset id>")
        asset_id = input()

        # call the web service:
        api = "/image"
        url = baseurl + api + "/" + asset_id

        res = web_service_get(url)

        if res.status_code != 200:
            # failed:
            # print("Failed with status code:", res.status_code)
            # print("url: " + url)
            if res.status_code in [400, 500]:  # we'll have an error message
                body = res.json()
                # print("Error message:", body["message"])
                print(body["message"])
            return

        # deserialize and extract image:
        body = res.json()

        user_id = body["user_id"]
        asset_name = body["asset_name"]
        bucket_key = body["bucket_key"]
        bytes = body["data"]

        print("userid:", user_id)
        print("asset name:", asset_name)
        print("bucket key:", bucket_key)

        # write the binary data to a file (as a
        # binary file, not a text file):
        binary_asset = base64.b64decode(bytes)
        with open(asset_name, "wb") as asset_file:
            asset_file.write(binary_asset)
        print(f"Downloaded from S3 and saved as ' {asset_name} '")

        # display image if requested:
        if display:
            if host == "docker":
                print("Oops...")
                print(
                    "Docker is not setup to display images, see if you can open and view locally..."
                )
                print("Oops...")
            elif host == "localhost":
                image = img.imread(asset_name)
                plt.imshow(image)
                plt.show()

    except Exception as e:
        logging.error("download() failed:")
        logging.error("url: " + url)
        logging.error(e)
        return


###################################################################
#
# bucket_contents
#
def bucket_contents(baseurl):
    """
    Prints out the contents of the S3 bucket

    Parameters
    ----------
    baseurl: baseurl for web service

    Returns
    -------
    nothing
    """

    try:
        # call the web service:
        api = "/bucket"
        url = baseurl + api

        # we have to loop since data is returned page by page:
        last_key = ""

        while True:
            # make a request...
            res = web_service_get(url)
            # check status code, if failed break out of loop
            if res.status_code != 200:
                # failed:
                print("Failed with status code:", res.status_code)
                print("url: " + url)
                if res.status_code == 500:  # we'll have an error message
                    body = res.json()
                    print("Error message:", body["message"])
                return

            # deserialize and extract the bucket info:
            body = res.json()
            # any data? if not, break out of loop
            # display data
            if not body["data"]:
                break

            # map each dictionary into a BucketItem object:
            bucket_items = [
                jsons.load(bucket_item, BucketItem) for bucket_item in body["data"]
            ]

            # Now we can think OOP:
            for bucket_item in bucket_items:
                print(bucket_item.Key)
                print(" ", bucket_item.LastModified)
                # print(" ", bucket_item.ETag)
                print(" ", bucket_item.Size)
                # print(" ", bucket_item.StorageClass)

            if len(bucket_items) < 12:
                break

            # check for more pages
            # if 'y' then continue, else break
            print("another page? [y/n]")
            answer = input().lower()
            if answer in ["y", "yes"]:
                # last_key = body["nextToken"]
                last_key = bucket_item.Key
                # add parameter to url
                url = baseurl + api
                url += "?startafter=" + last_key
                continue
            else:
                break

    except Exception as e:
        logging.error("bucket_contents() failed:")
        logging.error("url: " + url)
        logging.error(e)
        return


###################################################################
#
# add_user
#
def add_user(baseurl):
    """
    Prompts the user for the new user's email,
    last name, and first name, and then inserts
    this user into the database. But if the user's
    email already exists in the database, then we
    update the user's info instead of inserting
    a new user.

    Parameters
    ----------
    baseurl: baseurl for web service

    Returns
    -------
    nothing
    """

    try:
        print("Enter user's email>")
        email = input()

        print("Enter user's last (family) name>")
        last_name = input()

        print("Enter user's first (given) name>")
        first_name = input()

        # generate unique folder name:
        folder = str(uuid.uuid4())

        data = {
            "email": email,
            "lastname": last_name,
            "firstname": first_name,
            "bucketfolder": folder,
        }

        # call the web service:
        api = "/user"
        url = baseurl + api

        res = web_service(url, method="PUT", data=data)
        if res.status_code != 200:
            # failed:
            print("Failed with status code:", res.status_code)
            print("url: " + url)
            if res.status_code in [400, 500]:  # we'll have an error message
                body = res.json()
                print("Error message:", body["message"])
            return

        # success, extract userid:
        body = res.json()

        userid = body["userid"]
        message = body["message"]

        print(f"User {userid} successfully {message}")

    except Exception as e:
        logging.error("add_user() failed:")
        logging.error(f"url: {url}")
        logging.error(e)
        return


###################################################################
#
# upload
#
def upload(baseurl):
    """
    Prompts the user for a local filename and user id,
    and uploads that asset (image) to the user's folder
    in the bucket. The asset is given a random, unique
    name. The database is also updated to record the
    existence of this new asset in S3.

    Parameters
    ----------
    baseurl: baseurl for web service

    Returns
    -------
    nothing
    """

    try:
        print("Enter local filename>")
        local_filename = input()

        if not pathlib.Path(local_filename).is_file():
            print(f"Local file '{local_filename}' does not exist...")
            return

        print("Enter user id>")
        userid = input()

        # build the data packet:
        infile = open(local_filename, "rb")
        bytes = infile.read()
        infile.close()

        # now encode the image as base64. Note b64encode returns
        # a bytes object, not a string. So then we have to convert
        # (decode) the bytes -> string, and then we can serialize
        # the string as JSON for upload to server:
        data = base64.b64encode(bytes)
        datastr = data.decode()

        data = {"assetname": local_filename, "data": datastr}

        # call the web service:
        api = "/image"
        url = baseurl + api + "/" + userid

        res = web_service(url, method="POST", data=data)
        if res.status_code != 200:
            # failed:
            print(f"Failed with status code: {res.status_code}")
            print(f"url: {url}")
            if res.status_code in [400, 500]:  # we'll have an error message
                body = res.json()
                print("Error message:", body["message"])
            return

        # success, extract userid
        body = res.json()
        assetid = body["assetid"]
        print(f"Image uploaded, asset id = {assetid}")

    except Exception as e:
        logging.error("upload() failed:")
        logging.error(f"url: {url}")
        logging.error(e)
        return
