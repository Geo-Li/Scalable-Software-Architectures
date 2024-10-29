//
// app.get('/users', async (req, res) => {...});
//
// Return all the users from the database:
//
const photoapp_db = require("./photoapp_db.js");
const { query_database } = require("./utils.js");

exports.get_users = async (req, res) => {
  console.log("**Call to get /users...");

  try {
    const sql = `
      SELECT * FROM users
      ORDER BY userid ASC;
    `;
    console.log("/users: executing SQL to fetch all users...");

    let users = await query_database(photoapp_db, sql);
    console.log("/users: successfully fetched users data...");

    res.json({
      message: "success",
      data: users,
    });
  } catch (err) {
    //try
    console.log("**Error in /users");
    console.log(err.message);

    res.status(500).json({
      message: err.message,
      data: [],
    });
  } //catch
}; //get
