--
-- inserts one user and one asset into respective tables:
--
-- NOTE: userid in users table is automatically generated, so we
-- don't provide a userid. Likewise for assetid in assets table.
--

USE photoapp;

INSERT INTO
	users(email, lastname, firstname, bucketfolder)
	values
		('xixi@pet.cats', '', 'xixi',
			'527f4650-a4b9-4aec-9d9f-06dea966afa9'),
		('japan@country.travel', 'japan', 'kyoto',
			'b36cef53-8e11-413b-b084-c10e9d1c6e7a'),
		('usa@country.travel', 'states', 'united', 
			'9dc74e4d-e7f2-47d3-b56c-2f465a52935b');

INSERT INTO 
	assets(userid, assetname, bucketkey)
	values
		(80001,
			'Cat Stretched.JPG',
			'527f4650-a4b9-4aec-9d9f-06dea966afa9/70a730f8-b382-4745-b81d-c5977c984b05.JPG'),
        (80001,
			'Cat Watching.JPG',
			'527f4650-a4b9-4aec-9d9f-06dea966afa9/3b86a956-1cbb-446a-ac14-68fc8d8177d6.JPG'),
        (80002,
			'Kyoto Night.JPG',
			'9dc74e4d-e7f2-47d3-b56c-2f465a52935b/418c09b1-b3f0-43c4-8705-ec5d5f055502.JPG'),
        (80002,
			'Raining Garden.JPG',
			'9dc74e4d-e7f2-47d3-b56c-2f465a52935b/aeafb918-c335-4362-8842-15e030f0e2c1.JPG'),
        (80003,
			'Red Rock.JPG',
			'b36cef53-8e11-413b-b084-c10e9d1c6e7a/d77d8731-ed54-4eda-a693-74bd14f2ebcf.JPG'),
        (80003,
			'West Coast Bay.JPG',
			'b36cef53-8e11-413b-b084-c10e9d1c6e7a/c1231002-6e6e-43a2-a819-3fd6e173255d.JPG');

