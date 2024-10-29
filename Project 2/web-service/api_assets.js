//
// app.get('/assets', async (req, res) => {...});
//
// Return all the assets from the database:
//
const photoapp_db = require("./photoapp_db.js");
const { query_database } = require("./utils.js");

exports.get_assets = async (req, res) => {
  console.log("**Call to get /assets...");

  try {
    const sql = `
      SELECT * FROM assets
      ORDER BY assetid ASC;
    `;
    console.log("/assets: executing SQL to fetch all assets...");

    let assets = await query_database(photoapp_db, sql);
    console.log("/assets: successfully fetched assets data...");

    res.json({
      message: "success",
      data: assets,
    });
  } catch (err) {
    //try
    console.log("**Error in /assets");
    console.log(err.message);

    res.status(500).json({
      message: err.message,
      data: [],
    });
  } //catch
}; //get
