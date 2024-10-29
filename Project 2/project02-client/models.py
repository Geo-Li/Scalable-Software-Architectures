###################################################################
#
# classes
#
class User:
    userid: int  # these must match columns from DB table
    email: str
    lastname: str
    firstname: str
    bucketfolder: str


class Asset:
    assetid: int  # these must match columns from DB table
    userid: int
    assetname: str
    bucketkey: str


class BucketItem:
    Key: str
    LastModified: str
    ETag: str
    Size: int
    StorageClass: str
