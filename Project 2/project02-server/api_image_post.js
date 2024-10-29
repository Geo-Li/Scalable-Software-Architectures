//
// app.post('/image/:userid', async (req, res) => {...});
//
// Uploads an image to the bucket and updates the database,
// returning the asset id assigned to this image.
//
const photoapp_db = require("./photoapp_db.js");
const { query_database } = require("./utils.js");
const { PutObjectCommand } = require("@aws-sdk/client-s3");
const {
  photoapp_s3,
  s3_bucket_name,
  s3_region_name,
} = require("./photoapp_s3.js");

const uuid = require("uuid");

exports.post_image = async (req, res) => {
  console.log("**Call to post /image/:userid...");

  try {
    const userId = req.params.userid;
    const data = req.body; // data => JS object
    const get_user_sql = `
      SELECT * FROM users
      WHERE userid = ?;
    `;
    const user = await query_database(
      photoapp_db,
      get_user_sql,
      (parameters = [userId])
    );
    if (!user.length) {
      console.log(`**Error: user with id ${userId} not found.`);
      res.status(400).json({
        message: "no such user...",
        assetid: -1,
      });
      return;
    }
    const assetNameId = uuid.v4();
    const bucketKey = user[0].bucketkey + "/" + assetNameId + ".jpg";
    const imgStr = data["data"];
    const bytes = Buffer.from(imgStr, "base64");

    const input = {
      Bucket: s3_bucket_name,
      Key: bucketKey,
      Body: bytes,
      ContentType: "image/jpg",
      ACL: "public-read",
    };
    const command = new PutObjectCommand(input);
    await photoapp_s3.send(command);
    console.log(
      "/image/:userid: Successfully encoded image and stored in S3..."
    );

    // Save the asset into the assets table
    const insert_asset_sql = `
      INSERT INTO assets (userid, assetname, bucketkey)
      VALUES (?, ?, ?);
    `;
    const new_asset = await query_database(
      photoapp_db,
      insert_asset_sql,
      (parameters = [user[0].userid, data["assetname"], bucketKey])
    );
    if (new_asset.affectedRows !== 1) {
      throw new Error("asset insertion failed...");
    }

    console.log("/image/:userid: Successfully added new asset into RDS...");
    res.json({
      message: "success",
      assetid: new_asset.insertId,
    });
  } catch (err) {
    //try
    console.log("**Error in /image");
    console.log(err.message);

    res.status(500).json({
      message: err.message,
      assetid: -1,
    });
  } //catch
}; //post
