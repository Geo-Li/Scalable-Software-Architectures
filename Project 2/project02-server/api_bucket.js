//
// app.get('/bucket?startafter=bucketkey', async (req, res) => {...});
//
// Retrieves the contents of the S3 bucket and returns the
// information about each asset to the client. Note that it
// returns 12 at a time, use startafter query parameter to pass
// the last bucketkey and get the next set of 12, and so on.
//
const { ListObjectsV2Command } = require("@aws-sdk/client-s3");
const {
  photoapp_s3,
  s3_bucket_name,
  s3_region_name,
} = require("./photoapp_s3.js");

const PAGE_SIZE = 12;

exports.get_bucket = async (req, res) => {
  console.log("**Call to get /bucket...");

  try {
    let input = {
      Bucket: s3_bucket_name,
      MaxKeys: PAGE_SIZE,
      StartAfter: req.query.startafter || null,
    };

    console.log("/bucket: calling S3 ListObjectsV2Command...");

    let command = new ListObjectsV2Command(input);
    let s3_response = await photoapp_s3.send(command);
    const assets = s3_response.Contents || [];
    const keyCount = s3_response.KeyCount || 0;

    console.log(`/bucket: Retrieved ${keyCount} assets from S3...`);
    res.json({
      message: "success",
      data: assets,
      nextToken: keyCount ? assets[keyCount - 1].Key : null,
    });
  } catch (err) {
    //try
    console.log("**Error in /bucket");
    console.log(err.message);

    res.status(500).json({
      message: err.message,
      data: [],
    });
  } //catch
}; //get
