# Kids First OMOP Imports
This repository is primarily meant to store configurations for importing
study datasets into the experimental Kids First OMOP Database.

***Note***

Currently, the repository also contains a basic library (source code in `common`) with command line interface for running the ingestions in OMOP Postgres database. This is in place of the soon to be complete Kids First Data Ingest library. Once the Kids First Data Ingest library is complete, the `common` package will go away and the new library can be used.

There are only two datasets that have ingest configurations implemented: Vilain 2015 and CBTTC Proteomics.

# Getting Started

## Install

```
 # Git clone this repository
git clone git@github.com:kids-first/kf-omop-imports.git

# Setup and activate virtual env
python3 -m venv venv
source venv/bin/activate

# Install requirements
pip install -e .
pip install -r requirements.txt
```

## Set Environment Variables
The import tool loads data into the OMOP database by connecting directly to it. It uses the following environment variables to make the connection URL. Change these to control the database connection.

1. `PG_HOST` - if not set will default to `localhost`
2. `PG_NAME` - if not set will default to `omop`
3. `PG_USER` - if not set will default to `postgres`
4. `PG_PASS` - if not set will default to empty string

## Usage
``` bash
$ cd kf-omop-imports
$ omop ingest <path to folder containing extract configs>
```

## Example
```bash
$ omop ingest cbttc_proteomics
```
