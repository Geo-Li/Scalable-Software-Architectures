#
# Main program for photoapp program using AWS S3 and RDS to
# implement a simple photo application for photo storage and
# viewing.
#
# Authors:
#   Zhuoyuan Li
#   Prof. Joe Hummel (initial template)
#   Northwestern University
#

import datatier  # MySQL database access
import awsutil  # helper functions for AWS
import boto3  # Amazon AWS

import uuid
import pathlib
import logging
import sys
import os
import textwrap

from configparser import ConfigParser

import matplotlib.pyplot as plt
import matplotlib.image as img


ENV = "submission"


###################################################################
#
# helper functions
#
def get_id(dbConn, field):
  retrieve_id_sql = """
  SELECT LAST_INSERT_ID();
  """
  row = datatier.retrieve_one_row(dbConn, retrieve_id_sql)
  if row is None or row == ():
    print("Database operation failed...")
  else:
    print(f"Recorded in RDS under {field} {row[0]}")


###################################################################
#
# prompt
#
def prompt():
  """
  Prompts the user and returns the command number
  
  Parameters
  ----------
  None
  
  Returns
  -------
  Command number entered by user (0, 1, 2, ...)
  """

  try:
    print()
    print(">> Enter a command:")
    print("   0 => end")
    print("   1 => stats")
    print("   2 => users")
    print("   3 => assets")
    print("   4 => download")
    print("   5 => download and display")
    print("   6 => upload")
    print("   7 => add user")

    cmd = int(input())
    return cmd

  except Exception as e:
    print("ERROR")
    print("ERROR: invalid input")
    print("ERROR")
    return -1


###################################################################
#
# stats
#
def stats(bucketname, bucket, endpoint, dbConn):
  """
  Prints out S3 and RDS info: bucket name, # of assets, RDS 
  endpoint, and # of users and assets in the database
  
  Parameters
  ----------
  bucketname: S3 bucket name,
  bucket: S3 boto bucket object,
  endpoint: RDS machine name,
  dbConn: open connection to MySQL server
  
  Returns
  -------
  nothing
  """
  
  #
  # helper functions
  #
  def display_count(sql: str, table_name: str):
    row = datatier.retrieve_one_row(dbConn, sql)
    if row is None:
      print("Database operation failed...")
    elif row == ():
      print("Unexpected query failure...")
    else:
      print(f"# of {table_name}: {row[0]}")
  
  #
  # bucket info:
  #
  try: 
    print("S3 bucket name:", bucketname)

    assets = bucket.objects.all()
    print("S3 assets:", len(list(assets)))

    #
    # MySQL info:
    #
    print("RDS MySQL endpoint:", endpoint)

    users_count_sql = """
    SELECT COUNT(*) FROM users;
    """
    assets_count_sql = """
    SELECT COUNT(*) FROM assets;
    """

    #
    # Tables info:
    #
    display_count(users_count_sql, "users")
    display_count(assets_count_sql, "assets")

  except Exception as e:
    print("ERROR")
    print("ERROR: an exception was raised and caught")
    print("ERROR")
    print("MESSAGE:", str(e))
    
    
#
# users
#
def users(dbConn):
  """
  Prints out users info in the descending order by user id
  FORMAT
  User id: {user_id}
    Email: {email}
    Name: {first_name, last_name}
    Folder: {bucket_folder}
  
  Parameters
  ----------
  dbConn: open connection to MySQL server
  
  Returns
  -------
  nothing
  """  
  
  try: 
    users_sql = """
    SELECT * FROM users
    ORDER BY userid DESC;
    """
    
    rows = datatier.retrieve_all_rows(dbConn, users_sql)
    if rows is None:
      print("Database operation failed...")
    elif rows == ():
      print("Unexpected query failure...")
    else:
      for row in rows:
        users_info_str = textwrap.dedent(f"""\
        User id: {row[0]}
          Email: {row[1]}
          Name: {row[2]} , {row[3]}
          Folder: {row[4]}
        """).rstrip()
        print(users_info_str)
      
  except Exception as e:
    print("ERROR")
    print("ERROR: an exception was raised and caught")
    print("ERROR")
    print("MESSAGE:", str(e))
    
    
#
# assets
#
def assets(dbConn):
  """
  Prints out assets info in the descending order by asset id
  FORMAT
  Asset id: {asset_id}
    User id: {user_id}
    Original name: {asset_name}
    Key name: {bucket_key}
  
  Parameters
  ----------
  dbConn: open connection to MySQL server
  
  Returns
  -------
  nothing
  """  

  try: 
    assets_sql = """
    SELECT * FROM assets
    ORDER BY assetid DESC;
    """
    
    rows = datatier.retrieve_all_rows(dbConn, assets_sql)
    if rows is None:
      print("Database operation failed...")
    elif rows == ():
      print("Unexpected query failure...")
    else:
      for row in rows:
        users_info_str = textwrap.dedent(f"""\
        Asset id: {row[0]}
          User id: {row[1]}
          Original name: {row[2]}
          Key name: {row[3]}
        """).rstrip()
        print(users_info_str)
      
  except Exception as e:
    print("ERROR")
    print("ERROR: an exception was raised and caught")
    print("ERROR")
    print("MESSAGE:", str(e))
    

#
# download
#
def download(dbConn, bucket):
  """
  Takes an asset id as input, if asset info exists in the database,
  downloads the file from S3, and renames it to {asset_name}
  
  Parameters
  ----------
  dbConn: open connection to MySQL server,
  bucket: S3 boto bucket object
  
  Returns
  -------
  filename: downloaded and renamed file name
  """  
  
  try: 
    assets_sql = """
    SELECT * FROM assets
    WHERE assetid = %s;
    """
    
    asset_id = int(input("Enter asset id>\n"))
    row = datatier.retrieve_one_row(dbConn, assets_sql, [asset_id])
    if row is None:
      print("Database operation failed...")
    elif row == ():
      print("No such asset...")
    else:
      # Download the file from S3 and rename it
      bucket.download_file(row[3], row[2])
      print(f"Downloaded from S3 and saved as ' {row[2]} '")
      return row[2]
      
  except Exception as e:
    print("ERROR")
    print("ERROR: an exception was raised and caught")
    print("ERROR")
    print("MESSAGE:", str(e))
    

#
# download and display
#
def download_and_display(dbConn, bucket):
  """
  Download the image (refer to download()),
  and display the image using matplotlib
  
  Parameters
  ----------
  dbConn: open connection to MySQL server,
  bucket: S3 boto bucket object
  
  Returns
  -------
  nothing
  """  
  
  try: 
    filename = download(dbConn, bucket)
    # Display the image
    image = img.imread(filename)
    plt.imshow(image)
    plt.show()
      
  except Exception as e:
    print("ERROR")
    print("ERROR: an exception was raised and caught")
    print("ERROR")
    print("MESSAGE:", str(e))
    
    
#
# upload
#
def upload(dbConn, bucket):
  """
  Uploads a new file to user's S3 folder, the file is given a
  unique name in S3 (uuid)
  Then, we insert the file info into RDS
  
  Parameters
  ----------
  dbConn: open connection to MySQL server,
  bucket: S3 boto bucket object
  
  Returns
  -------
  nothing
  """  
  
  try: 
    get_user_sql = """
    SELECT * FROM users
    WHERE userid = %s;
    """
    asset_insertion_sql = """
    INSERT INTO assets(userid, assetname, bucketkey)
    VALUES (%s, %s, %s);
    """
    # Get the local filename
    local_file_name = input("Enter local filename>\n")
    if not os.path.exists(local_file_name):
      print(f"Local file ' {local_file_name} ' does not exist...")
      return
    _, file_extension = os.path.splitext(local_file_name)
    # Get the user id
    user_id = int(input("Enter user id>\n"))
    row = datatier.retrieve_one_row(dbConn, get_user_sql, [user_id])
    if row is None:
      print("Database operation failed...")
    elif row == ():
      print("No such user...")
    else:
      # Upload the file to the S3 folder
      unique_file_name = str(uuid.uuid4())
      s3_obj_key = row[4] + '/' + unique_file_name + file_extension
      key = awsutil.upload_file(local_file_name, bucket, key=s3_obj_key)
      if not key:
        return
      print(f"Uploaded and stored in S3 as ' {s3_obj_key} '")
      # Save the file info into the assets table
      row_count = datatier.perform_action(dbConn, asset_insertion_sql,
        [user_id, local_file_name, s3_obj_key]
      )
      if row_count == 0:
        print("Failed to insert the assets table")
        return
      elif row_count == 1:
        get_id(dbConn, "asset id")
      
  except Exception as e:
    print("ERROR")
    print("ERROR: an exception was raised and caught")
    print("ERROR")
    print("MESSAGE:", str(e))
    
    
#
# add user
#
def add_user(dbConn):
  """
  Adds a new user info into RDS by parsing user inputs
  
  Parameters
  ----------
  dbConn: open connection to MySQL server
  
  Returns
  -------
  nothing
  """  
  
  try: 
    user_insertion_sql = """
    INSERT INTO users(email, lastname, firstname, bucketfolder)
	  VALUES (%s, %s, %s, %s);
    """
    # Get user's email
    email = input("Enter user's email>\n")
    # Get user's last name
    last_name = input("Enter user's last (family) name>\n")
    # Get user's first name
    first_name = input("Enter user's first (given) name>\n")
    # Generate the unique folder name
    unique_folder_name = str(uuid.uuid4())
    # Save the user info into the users table
    row_count = datatier.perform_action(dbConn, user_insertion_sql,
      [email, last_name, first_name, unique_folder_name]
    )
    if row_count == 0:
      print("Failed to insert the users table")
      return
    elif row_count == 1:
      get_id(dbConn, "user id")
      
  except Exception as e:
    print("ERROR")
    print("ERROR: an exception was raised and caught")
    print("ERROR")
    print("MESSAGE:", str(e))


#########################################################################
#
# main
#
print('** Welcome to PhotoApp **')
print()

# eliminate traceback so we just get error message:
sys.tracebacklimit = 0

#
# what config file should we use for this session?
#
config_file = 'photoapp-config.ini'

print("What config file to use for this session?")
print("Press ENTER to use default (photoapp-config.ini),")
print("otherwise enter name of config file>")
s = input()

if s == "":  # use default
  pass  # already set
else:
  config_file = s

#
# does config file exist?
#
if not pathlib.Path(config_file).is_file():
  print("**ERROR: config file '", config_file, "' does not exist, exiting")
  sys.exit(0)

#
# gain access to our S3 bucket:
#
s3_profile = 's3readwrite'

os.environ['AWS_SHARED_CREDENTIALS_FILE'] = config_file

boto3.setup_default_session(profile_name=s3_profile)

configur = ConfigParser()
configur.read(config_file)
bucketname = configur.get('s3', 'bucket_name')

s3 = boto3.resource('s3')
bucket = s3.Bucket(bucketname)

#
# now let's connect to our RDS MySQL server:
#
endpoint = configur.get('rds', 'endpoint')
portnum = int(configur.get('rds', 'port_number'))
username = configur.get('rds', 'user_name')
pwd = configur.get('rds', 'user_pwd')
dbname = configur.get('rds', 'db_name')

dbConn = datatier.get_dbConn(endpoint, portnum, username, pwd, dbname)

if dbConn is None:
  print('**ERROR: unable to connect to database, exiting')
  sys.exit(0)

#
# main processing loop:
#
cmd = prompt()

while cmd != 0:
  #
  if cmd == 1:
    stats(bucketname, bucket, endpoint, dbConn)
  elif cmd == 2:
    users(dbConn)
  elif cmd == 3:
    assets(dbConn)
  elif cmd == 4:
    download(dbConn, bucket)
  elif cmd == 5:
    download_and_display(dbConn, bucket)
  elif cmd == 6:
    upload(dbConn, bucket)
  elif cmd == 7:
    add_user(dbConn)
  else:
    print("** Unknown command, try again...")
  #
  cmd = prompt()

#
# done
#
print()
print('** done **')
