## INTRODUCION
A music streaming startup, PMusic, has outgrown their user base and song database and want to move their processes and data onto the cloud. Their data resides in S3, in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.
The project is to build a pipeline that extracts from S3 and load into Redshift where it is staged and transformed

- Load the data from S3 buckets.
- Load the data into the staging area in Redshift
- facts and dimension tables were created in the Redshift
- Data is then loaded into the Redshift Cluster



We have two staging tables which copy the JSON file inside the S3 buckets.

#### Staging Table
-staging_songs - info about songs and artists
-staging_events - actions done by users (which song they are are listening, etc.. )

#### Star Schema
A star schema was created, optimized for queries on song play analysis

##### Fact Table
-songplays - records in event data associated with song plays i.e. records with page NextSong

##### Dimension Tables
-users - users in the app
-songs - songs in music database
-artists - artists in music database




## HOW TO RUN
- Run create_tables.py drop and create tables needed.
- Run etl.py to load data into the staging area and into the tables discussed in the schema


### Other files
- sql_queries.py contains the sql codes needed to drop, create and insert into tables