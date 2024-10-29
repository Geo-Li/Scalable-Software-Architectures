//
// app.put('/user', async (req, res) => {...});
//
// Inserts a new user into the database, or if the
// user already exists (based on email) then the
// user's data is updated (name and bucket folder).
// Returns the user's userid in the database.
//
const photoapp_db = require("./photoapp_db.js");
const { query_database } = require("./utils.js");

exports.put_user = async (req, res) => {
  console.log("**Call to put /user...");

  try {
    let data = req.body; // data => JS object
    console.log(data);
    const email = data["email"];
    const last_name = data["lastname"];
    const first_name = data["firstname"];
    const bucket_folder = data["bucketfolder"];
    const get_user_sql = `
      SELECT * FROM users
      WHERE email = ?;
    `;
    query_database(db=photoapp_db)
    const user = await query_database(
      photoapp_db,
      get_user_sql,
      (parameters = [email])
    );
    if (!user.length) {
      console.log(`/user: Didn't find the user with email: ${email}`);
      console.log("/user: Insert the new user into users");
      // user not found, insert into the users table
      const insert_user_sql = `
        INSERT INTO users (email, firstname, lastname, bucketfolder)
        VALUES (?, ?, ?, ?);
      `;
      const new_user = await query_database(
        photoapp_db,
        insert_user_sql,
        (parameters = [email, first_name, last_name, bucket_folder])
      );
      if (new_user.affectedRows !== 1) {
        throw new Error("user insertion failed...");
      }

      console.log("/user: New user added successfully...");
      res.json({
        message: "inserted",
        userid: new_user.insertId,
      });
    } else {
      // user found, update the user info
      console.log(`/user: Found the user with email: ${email}`);
      console.log("/user: Update the existing user in users");
      const update_user_sql = `
        UPDATE users
        SET email = ?, firstname = ?, lastname = ?, bucketfolder = ?
        WHERE email = ?;
      `;
      const updated_user = await query_database(
        photoapp_db,
        update_user_sql,
        (parameters = [email, first_name, last_name, bucket_folder, email])
      );
      if (updated_user.affectedRows !== 1) {
        throw new Error("user update failed...");
      }

      console.log("/user: Existing user updated successfully...");
      res.json({
        message: "updated",
        userid: user[0].userid,
      });
    }
  } catch (err) {
    //try
    console.log("**Error in /user");
    console.log(err.message);

    res.status(500).json({
      message: err.message,
      userid: -1,
    });
  } //catch
}; //put
