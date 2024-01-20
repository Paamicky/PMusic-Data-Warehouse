import configparser
ARN='aws_iam_role= arn:aws:iam::871982317973:role/myRedshiftRole'


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

########################### DROP TABLES #######################################
staging_events_table_drop = "DROP TABLE IF EXISTS staging_events_table"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs_table"
songplay_table_drop = "DROP TABLE IF EXISTS songplay_table"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artist"
time_table_drop = "DROP TABLE IF EXISTS time"


################## CREATE TABLES #############################################

staging_events_table_create= ("""
    CREATE TABLE IF NOT EXISTS staging_events_table (
        artist                 VARCHAR,
        auth                   VARCHAR,
        firstName              VARCHAR,
        gender                 VARCHAR ,
        iteminSession          INTEGER ,    
        lastName               VARCHAR,
        length                 NUMERIC,
        level                  VARCHAR,
        location               VARCHAR ,       
        method                 VARCHAR,
        page                   VARCHAR,
        registration           BIGINT,
        sessionId              INTEGER,
        song                   VARCHAR,
        status                 INTEGER,
        ts                     BIGINT,
        userAgent              VARCHAR,
        userId                 INTEGER
    
    
    );
        


""")

staging_songs_table_create = ("""
    CREATE TABLE staging_songs_table(
        artist_id                   VARCHAR,
        artist_latitude             FLOAT,
        artist_location             VARCHAR,
        artist_longitude            FLOAT,
        artist_name                 VARCHAR,
        duration                    FLOAT,
        num_songs                  INTEGER,
        song_id                    VARCHAR,
        title                   VARCHAR,
        year                       INTEGER
    );

""")

songplay_table_create = ("""
CREATE TABLE IF NOT EXISTS songplays (
        songplay_id           INTEGER PRIMARY KEY, 
        start_time            TIMESTAMP, 
        user_id               INT NOT NULL, 
        level                 VARCHAR, 
        song_id               VARCHAR, 
        artist_id             VARCHAR, 
        session_id            VARCHAR, 
        location             VARCHAR, 
        user_agent            VARCHAR);
""")

user_table_create = ("""
CREATE TABLE IF NOT EXISTS users (
            user_id          INT PRIMARY KEY, 
            first_name       VARCHAR, 
            last_name        VARCHAR, 
            gender           VARCHAR, 
            level            VARCHAR);
""")

song_table_create = ("""
CREATE TABLE songs (
        song_id         VARCHAR    PRIMARY KEY, 
        title           VARCHAR, 
        artist_id       VARCHAR, 
        year            INTEGER, 
        duration    FLOAT);
""")

artist_table_create = ("""
    CREATE TABLE IF NOT EXISTS artists (
        artist_id VARCHAR PRIMARY KEY, 
        name VARCHAR, 
        location VARCHAR, 
        lattitude FLOAT, 
        longitude FLOAT);
""")

time_table_create = ("""
CREATE TABLE time (
        start_time       BIGINT  PRIMARY KEY , 
        hour             INTEGER, 
        day              INTEGER, 
        week            INTEGER, 
        month           INTEGER, 
        year            INTEGER, 
        weekday         INTEGER);
""")


################################### STAGING TABLES ###############################

staging_events_copy = ("""
            COPY staging_events_table
            FROM {}
            iam_role {}
FORMAT AS JSON {} REGION 'us-west-2';""").format(config.get('S3','LOG_DATA'), config.get('IAM_ROLE', 'ARN'), config.get('S3','LOG_JSONPATH'))

staging_songs_copy = ("""
        COPY staging_songs_table
        FROM {}
        iam_role {}
FORMAT AS JSON 'auto' REGION 'us-west-2';""").format(config.get('S3','SONG_DATA'), config.get('IAM_ROLE', 'ARN'))





################################### inserting into tables  ######################

# Copying data from staging areas into the facts and dimension table
songplay_table_insert = ("""
INSERT INTO songplays (start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
SELECT DISTINCT
    ts,
    se.userId,
    se.level,
    ss.song_id,
    ss.artist_id,
    se.sessionId as sessionId,
    se.location,
    se.userAgent as userAgent
FROM staging_events_table se
INNER JOIN staging_songs_table ss ON ss.title = se.song 
AND se.artist = ss.artist_name
WHERE se.page = 'NextSong';
""")


user_table_insert = ("""
INSERT INTO users (user_id, first_name, last_name, gender, level)
SELECT DISTINCT
    userId,
    firstName,
    lastName,
    gender,
    level
FROM staging_events_table
WHERE userId IS NOT NULL;
""")

song_table_insert = ("""
INSERT INTO songs (song_id, title, artist_id, year, duration)
SELECT DISTINCT 
    song_id,
    title,
    artist_id,
    year,
    duration
FROM staging_songs_table
WHERE song_id IS NOT NULL;
""")

artist_table_insert = ("""
INSERT INTO artists (artist_id, name, location, lattitude, longitude)
SELECT DISTINCT
    artist_id, 
    artist_name as name, 
    artist_location as location, 
    artist_latitude as lattitude, 
    artist_longitude as longitude
FROM staging_songs_table
WHERE artist_id IS NOT NULL;
""")

time_table_insert = ("""
INSERT INTO time (start_time, hour, day, week, month, year, weekday)
SELECT DISTINCT
    TIMESTAMP 'epoch' + (ts/1000) * INTERVAL '1 second' as start_time,
    EXTRACT(HOUR FROM start_time) AS hour,
    EXTRACT(DAY FROM start_time) AS day,
    EXTRACT(WEEKS FROM start_time) AS week,
    EXTRACT(MONTH FROM start_time) AS month,
    EXTRACT(YEAR FROM start_time) AS year,
    to_char(start_time, 'Day') AS weekday
FROM staging_events_table;
""")







################## QUERY LISTS #########################
create_table_queries =   [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries   =   [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries   =   [staging_events_copy, staging_songs_copy]
insert_table_queries =   [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
