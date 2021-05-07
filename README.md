# MSiA423 Project Repository

Author: Christina Chang

QA: Matt Ko

<!-- toc -->

- [Project charter](#project-charter)
- [Directory structure](#directory-structure)
- [Running the app](#running-the-app)
    * [1. Load data into S3](#1-load-data-into-s3)
        + [Download the raw data](#download-the-raw-data)
        + [Configure S3 credentials](#configure-s3-credentials)
        + [Build the Docker image](#build-the-docker-image)
        + [Upload the data into S3](#upload-the-data-into-s3)
    * [2. Initialize the database](#2-initialize-the-database)
        + [Configure SQL credentials](#configure-sql-credentials)
        + [Create the SQL database](#create-the-sql-database)
        + [Test connection to the database](#test-connection-to-the-database)

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
├── data                              <- Folder that contains data used or generated. Only the external/ and sample/ subdirectories are tracked by git. 
│   ├── external/                     <- External data sources, usually reference data,  will be synced with git
│   ├── sample/                       <- Sample data used for code development and testing, will be synced with git
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

### 1. Load data into S3

#### Download the raw data

The dataset is from Kaggle and can be downloaded [here](https://www.kaggle.com/planejane/national-park-trails). You 
will need to create a Kaggle account to access the data. A copy of the dataset is located in 
`data/external/nationa-park-trails.csv`.

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
    hike run.py s3_upload --s3path <your_s3_path> --local_path <year_local_path>
```

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

First connect to the Northwestern VPN, then run:

```bash
docker run -it \                        
    -e MYSQL_HOST \
    -e MYSQL_PORT \
    -e MYSQL_USER \
    -e MYSQL_PASSWORD \
    -e DATABASE_NAME \
    hike run.py create_db --engine_string <your_engine_string>
```

By default, the `python run.py create_db` creates the database locally at `sqlite:///data/trails.db` if no MYSQL
hostname is provided.

#### Test connection to the database

You should be able to connect to a sql session with the following command (remember to build the docker image first):

```bash
docker run -it --rm \
    mysql:5.7.33 \
    mysql \
    -h$MYSQL_HOST \
    -u$MYSQL_USER \
    -p$MYSQL_PASSWORD
```

You can query the database using:

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


