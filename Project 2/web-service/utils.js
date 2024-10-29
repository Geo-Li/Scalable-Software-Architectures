/*
query_database(db, sql)
input:
  db:
  sql:

Queries database, returning a PROMISE that you can
await on. When the PROMISE resolves, you'll have the 
results of your query (or you'll get an error thrown
back).
*/
const query_database = (db, sql, parameters = []) => {
  let response = new Promise((resolve, reject) => {
    try {
      db.query(sql, parameters, (err, results) => {
        if (err) {
          reject(err);
        } else {
          resolve(results);
        }
      });
    } catch (err) {
      reject(err);
    }
  });
  return response;
};

/*
get_s3()

calling S3 to get bucket status, returning a PROMISE
we have to wait on eventually:

build input object for S3 with request parameters:
*/

const get_s3 = async () => {
  try {
    let input = {
      Bucket: s3_bucket_name,
    };

    console.log("/stats: calling S3...");

    let command = new HeadBucketCommand(input);
    return await photoapp_s3.send(command);
  } catch (error) {
    throw new Error(error);
  }
};

module.exports = { query_database, get_s3 };
