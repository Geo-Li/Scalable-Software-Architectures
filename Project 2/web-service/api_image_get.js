//
// app.get('/image/:assetid', async (req, res) => {...});
//
// downloads an asset from S3 bucket and sends it back to the
// client as a base64-encoded string.
//
const photoapp_db = require("./photoapp_db.js");
const { query_database } = require("./utils.js");
const { GetObjectCommand } = require("@aws-sdk/client-s3");
const {
  photoapp_s3,
  s3_bucket_name,
  s3_region_name,
} = require("./photoapp_s3.js");

exports.get_image = async (req, res) => {
  console.log("**Call to get /image/:assetid...");

  try {
    const assetId = req.params.assetid;
    const sql = `
      SELECT * FROM assets
      WHERE assetid = ?;
    `;
    const asset = await query_database(
      photoapp_db,
      sql,
      (parameters = [assetId])
    );
    if (!asset.length) {
      console.log(`**Error: asset with id ${assetId} not found.`);
      res.status(400).json({
        message: "no such asset...",
        user_id: -1,
        asset_name: "?",
        bucket_key: "?",
        data: [],
      });
      return;
    }
    const bucketKey = asset[0].bucketkey;
    console.log(`/image: Found bucket key: ${bucketKey}`);

    let input = {
      Bucket: s3_bucket_name,
      Key: bucketKey,
    };
    let command = new GetObjectCommand(input);
    let s3_response = await photoapp_s3.send(command);
    const imgStr = await s3_response.Body.transformToString("base64");
    console.log(
      `/image: Successfully retrieved and encoded image for asset ID ${assetId}.`
    );
    res.json({
      message: "success",
      user_id: asset[0].userid,
      asset_name: asset[0].assetname,
      bucket_key: bucketKey,
      data: imgStr,
    });
  } catch (err) {
    //try
    console.log("**Error in /image");
    console.log(err.message);

    res.status(500).json({
      message: err.message,
      user_id: -1,
      asset_name: "?",
      bucket_key: "?",
      data: [],
    });
  } //catch
}; //get
