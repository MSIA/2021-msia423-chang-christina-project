# MSiA423 Project Repository

Author: Christina Chang

QA: Matt Ko

<!-- toc -->

- [Project charter](#project-charter)
- [Directory structure](#directory-structure)
- [Running the app](#running-the-app)
    * 0. Set environment variables and connect to the VPN
    * 1. Acquire the data, land it in S3, and create the database
    * 2. Clean the data, create features, and build the model
    * 3. Run the app
    * 4. Run unit tests
- [Running the app step by step](#running-the-app-step-by-step)
    * 1. Load data into S3
    * 2. Initialize the database
    * 3. Clean the data
    * 4. Create features
    * 5. Train the model
    * 6. Run the app
    * 7. Run unit tests

<!-- tocstop -->

## Project charter

### Vision

What’s the best way to experience earth’s natural wonders? Through visiting national parks, of course! From the glaciers
of Alaska to the sandstone arches of Utah, national parks provide millions of acres of public lands to explore. However,
finding a good trail that is enjoyable and suits your abilities can be time consuming. This web app is designed to help
users find national park trails according to the type of hike they like.

### Mission

The user will input the length, elevation gain, state, and other keywords that describe their ideal hike. The app will
classify the difficulty of the hike and provide recommendations for hiking trails in national parks. The difficulty will
be classified into three groups: easy, moderate, or hard. The app will use content based filtering to suggest trails
based on the user’s specifications. The goal is to provide relevant hiking trail recommendations and help users
understand the difficulty of the hike they’re interested in so they can properly plan ahead. The dataset can be
accessed [here](https://www.kaggle.com/planejane/national-park-trails).

### Success criteria

The model will be deployed if the cross validated accuracy of the classification model surpasses 70%. Business success
will be evaluated through various measures of user engagement. The app will be considered successful if 50% of new users
return to use the app again, the average time spent on the app in a single visit surpasses 3 minutes, and there is a 10%
increase in the number of users each month for the first six months.

## Directory structure

```
├── README.md                         <- You are here
├── api
│   ├── static/                       <- CSS, JS files that remain static
│   ├── templates/                    <- HTML (or other code) that is templated and changes based on a set of inputs
│   ├── boot.sh                       <- Start up script for launching app in Docker container.
│   ├── Dockerfile                    <- Dockerfile for building image to run app  
│
├── config                            <- Directory for configuration files 
│   ├── local/                        <- Directory for keeping environment variables and other local configurations that *do not sync** to Github 
│   ├── logging/                      <- Configuration of python loggers
│   ├── flaskconfig.py                <- Configurations for Flask API 
│
├── data                              <- Folder that contains data used or generated. Only the external/, sample/, and raw/ subdirectories are tracked by git. 
│   ├── external/                     <- External data sources, usually reference data,  will be synced with git
│   ├── sample/                       <- Sample data used for code development and testing, will be synced with git
│   ├── raw/                          <- Raw data files, will be synced with git
│
├── deliverables/                     <- Any white papers, presentations, final work products that are presented or delivered to a stakeholder 
│
├── docs/                             <- Sphinx documentation based on Python docstrings. Optional for this project. 
│
├── figures/                          <- Generated graphics and figures to be used in reporting, documentation, etc
│
├── models/                           <- Trained model objects (TMOs), model predictions, and/or model summaries
│
├── notebooks/
│   ├── archive/                      <- Develop notebooks no longer being used.
│   ├── deliver/                      <- Notebooks shared with others / in final state
│   ├── develop/                      <- Current notebooks being used in development.
│   ├── template.ipynb                <- Template notebook for analysis with useful imports, helper functions, and SQLAlchemy setup. 
│
├── reference/                        <- Any reference material relevant to the project
│
├── src/                              <- Source data for the project 
│
├── test/                             <- Files necessary for running model tests (see documentation below) 
│
├── app.py                            <- Flask wrapper for running the model 
├── run.py                            <- Simplifies the execution of one or more of the src scripts  
├── requirements.txt                  <- Python package dependencies 
```

## Running the app

This section covers the fastest way to run the app.

### 0. Set environment variables and connect to the VPN

Set environment variables for AWS:
```bash
export AWS_ACCESS_KEY_ID="MY_ACCESS_KEY_ID"
export AWS_SECRET_ACCESS_KEY="MY_SECRET_ACCESS_KEY"
```

Set environment variables for SQL:
```bash
export MYSQL_USER="MY_USERNAME"
export MYSQL_PASSWORD="MY_PASSWORD"
export MYSQL_HOST="MY_HOST"
export MYSQL_PORT="MY_PORT"
export DATABASE_NAME="MY_DATABASE"
```

Remember to connect to the Northwestern VPN to access the database!

### 1. Upload the data to S3, download the data from S3, and create the database

Build the image:
```bash
docker build -f app/Dockerfile_acquire -t hike-acquire .
```

This command will upload the raw data to S3, download the data from S3, and 
create the SQL database.
```bash
docker run \
    -e AWS_ACCESS_KEY_ID \
    -e AWS_SECRET_ACCESS_KEY \
    -e MYSQL_HOST \
    -e MYSQL_PORT \
    -e MYSQL_USER \
    -e MYSQL_PASSWORD \
    -e DATABASE_NAME \
    --mount type=bind,source="$(pwd)/data",target=/app/data/ \
    hike-acquire run_acquire.sh
```

### 2. Clean the data, create features, and build the model

Build the image:
```bash
docker build -f app/Dockerfile_pipeline -t hike-pipeline .
```

This command will clean the data, create features for modeling, and build a
random forest classification model.
```bash
docker run --mount type=bind,source="$(pwd)/",target=/app/ hike-pipeline run_pipeline.sh
```

### 3. Run the app

Build the image:
```bash
docker build -f app/Dockerfile -t hike .
```

This command will run the app. You can access the app at http://0.0.0.0:5000/
in your browser.
```bash
docker run -e SQLALCHEMY_DATABASE_URI -p 5000:5000 --name test hike app.py
```

When you're done with the app, run the following command to stop the container:
```bash
docker rm test
```

### 4. Run unit tests

This command will run units tests.
```bash
docker run hike -m pytest
```

## Running the app step by step

### 1. Load data into S3

#### Download the raw data

The dataset is from Kaggle and can be downloaded [here](https://www.kaggle.com/planejane/national-park-trails). You will
need to create a Kaggle account to access the data. Alternatively, acopy of the dataset is located in
`data/raw/national-park-trails.csv`.

#### Configure S3 credentials

```bash
export AWS_ACCESS_KEY_ID="MY_ACCESS_KEY_ID"
export AWS_SECRET_ACCESS_KEY="MY_SECRET_ACCESS_KEY"
```

#### Build the Docker image

The Dockerfile that defines the image for data acquisition and table generation is in the `app/` folder. To build the
image, run from this directory (the root of the repo):

```bash
docker build -f app/Dockerfile -t hike .
```

This command builds the Docker image, with the tag `hike`, based on the instructions in `app/Dockerfile` and the files
existing in this directory.

#### Upload the data into S3

```bash
docker run \
    -e AWS_ACCESS_KEY_ID \
    -e AWS_SECRET_ACCESS_KEY \
    hike run.py s3_upload --s3path <your_s3_path> --local_path <your_local_path>
```

This command uploads a CSV file from the specified `--local_path` to the S3 bucket. The `--s3path` is a required 
argument. By default, the `local_path` is set to `data/raw/national-park-trails.csv`.

### Download the data from S3

```bash
docker run \
    -e AWS_ACCESS_KEY_ID \
    -e AWS_SECRET_ACCESS_KEY \
    hike run.py s3_download --s3path <your_s3_path> --local_path <your_local_path>
```

This command downloads a CSV file from the specified S3 bucket to the `--local_path`. The `--s3path` is a required 
argument. By default, the `local_path` is set to `data/raw/national-park-trails.csv`.

### 2. Initialize the database

#### Configure SQL credentials

```bash
export MYSQL_USER="MY_USERNAME"
export MYSQL_PASSWORD="MY_PASSWORD"
export MYSQL_HOST="MY_HOST"
export MYSQL_PORT="MY_PORT"
export DATABASE_NAME="MY_DATABASE"
```

#### Create the SQL database

Connect to the Northwestern VPN and remember to build the docker image first, then run:

```bash
docker run -it \
    -e MYSQL_HOST \
    -e MYSQL_PORT \
    -e MYSQL_USER \
    -e MYSQL_PASSWORD \
    -e DATABASE_NAME \
    hike run.py create_db --engine_string
```

By default, the `python run.py create_db` creates the database locally at `sqlite:///data/trails.db` if no MYSQL
hostname is provided.

#### Test connection to the database

You should be able to connect to a sql session with the following command:

```bash
docker run -it --rm \
    mysql:5.7.33 \
    mysql \
    -h$MYSQL_HOST \
    -u$MYSQL_USER \
    -p$MYSQL_PASSWORD
```

You can query the database by entering:

```bash
use msia423_db;
```

Now enter queries. For instance, view the `trails` table:

```bash
SELECT * FROM trails;
```

You can also see other tables in the database using:

```bash
show tables;
```

### 3. Clean the data
```bash
docker run --mount type=bind,source="$(pwd)/data/",target=/app/data/ hike run.py clean
```

### 4. Create features
```bash
docker run --mount type=bind,source="$(pwd)/data/",target=/app/data/ hike run.py featurize
```

### 5. Train the model
```bash
docker run --mount type=bind,source="$(pwd)/",target=/app/ hike run.py model
```

### 6. Run the app
```bash
docker run -p 5000:5000 --name test hike app.py
```

### 7. Run unit tests
```bash
docker run hike -m pytest
```







```bash
docker build -f app/Dockerfile -t hike .
docker run \
    -e AWS_ACCESS_KEY_ID \
    -e AWS_SECRET_ACCESS_KEY \
    hike run.py s3_upload --s3path <your_s3_path> --local_path <your_local_path>
docker run \
    -e AWS_ACCESS_KEY_ID \
    -e AWS_SECRET_ACCESS_KEY \
    hike run.py s3_download --s3path <your_s3_path> --local_path <your_local_path>
docker run -it \
    -e MYSQL_HOST \
    -e MYSQL_PORT \
    -e MYSQL_USER \
    -e MYSQL_PASSWORD \
    -e DATABASE_NAME \
    hike run.py create_db --engine_string
docker run --mount type=bind,source="$(pwd)/data/",target=/app/data/ hike run.py clean
docker run --mount type=bind,source="$(pwd)/data/",target=/app/data/ hike run.py featurize
docker run --mount type=bind,source="$(pwd)/",target=/app/ hike run.py model


docker build -f app/Dockerfile_python -t hike .
docker build -f app/Dockerfile -t hike .
docker run -p 5000:5000 --name test hike app.py

http://0.0.0.0:5000/
```


Docker command Data acquisition / landing in S3 (upload and download), creating RDS, running app
```bash
docker build -f app/Dockerfile_acquire -t hike-acquire .
docker run \
    -e AWS_ACCESS_KEY_ID \
    -e AWS_SECRET_ACCESS_KEY \
    -e MYSQL_HOST \
    -e MYSQL_PORT \
    -e MYSQL_USER \
    -e MYSQL_PASSWORD \
    -e DATABASE_NAME \
    -e SQLALCHEMY_DATABASE_URI \
    --mount type=bind,source="$(pwd)/data",target=/app/data/ \
    hike-acquire run_acquire.sh
```

Docker for acquiring running pipeline
```bash
docker build -f app/Dockerfile_pipeline -t hike-pipeline .
docker run \
    --mount type=bind,source="$(pwd)/",target=/app/ \
    hike-pipeline run_pipeline.sh
```

Docker for running app
```bash
docker build -f app/Dockerfile -t hike .
docker run -p 5000:5000 --name test hike app.py

docker run -e SQLALCHEMY_DATABASE_URI="mysql+pymysql://msia423instructor:clc3780@nw-msia423-clc3780.cbqlcxzmovlx.us-east-1.rds.amazonaws.com:3306/msia423_db" -p 5000:5000 hike app.py
```
http://0.0.0.0:5000/
when youre done with the app run
```bash
docker rm test
```

Docker for running tests
```bash
docker run hike -m pytest
```

