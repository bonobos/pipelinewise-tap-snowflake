# pipelinewise-tap-snowflake

[![PyPI version](https://badge.fury.io/py/pipelinewise-tap-snowflake.svg)](https://badge.fury.io/py/pipelinewise-tap-snowflake)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pipelinewise-tap-snowflake.svg)](https://pypi.org/project/pipelinewise-tap-snowflake/)
[![License: Apache2](https://img.shields.io/badge/License-Apache2-yellow.svg)](https://opensource.org/licenses/Apache-2.0)

[Singer](https://www.singer.io/) tap that extracts data from a [Snowflake](https://www.snowflake.com/) database and produces JSON-formatted data following the [Singer spec](https://github.com/singer-io/getting-started/blob/master/docs/SPEC.md).

This is a [PipelineWise](https://transferwise.github.io/pipelinewise) compatible tap connector.

## How to use it

The recommended method of running this tap is to use it from [PipelineWise](https://transferwise.github.io/pipelinewise). When running it from PipelineWise you don't need to configure this tap with JSON files and most of things are automated. Please check the related documentation at [Tap Snowflake](https://transferwise.github.io/pipelinewise/connectors/taps/snowflake.html)

If you want to run this [Singer Tap](https://singer.io) independently please read further.

### Install and Run

First, make sure Python 3 is installed on your system or follow these
installation instructions for [Mac](http://docs.python-guide.org/en/latest/starting/install3/osx/) or
[Ubuntu](https://www.digitalocean.com/community/tutorials/how-to-install-python-3-and-set-up-a-local-programming-environment-on-ubuntu-16-04).

It's recommended to use a virtualenv:

```bash
  python3 -m venv venv
  pip install pipelinewise-tap-snowflake
```

or

```bash
  python3 -m venv venv
  . venv/bin/activate
  pip install --upgrade pip
  pip install .
```

### Configuration

1. Create a `config.json` file with connection details to snowflake.

   ```json
   {
     "account": "rtxxxxx.eu-central-1",
     "dbname": "database_name",
     "user": "my_user",
     "password": "password",
     "warehouse": "my_virtual_warehouse",
     "tables": "db.schema.table1,db.schema.table2"
   }
   ```

Optional Metadata can be provided in the config to define the syncing strategy for tables so that auto discovery creates a fully configured catalog.
   ```json
   {
      "account": "rtxxxxx.eu-central-1",
      "dbname": "database_name",
      "user": "my_user",
      "password": "password",
      "warehouse": "my_virtual_warehouse",
      "tables": "db.schema.table1,db.schema.table2",
      "metadata": {
          "db.schema.table1": {
              "table-key-properties": ["key1"],
              "replication-key": "column1",
              "replication-method": "INCREMENTAL",
              "selected": true
          }
      }
   }
   ```

**Note**: `tables` is a mandatory parameter as well to avoid long running catalog discovery process.
Please specify fully qualified table and view names and only that ones that you need to extract otherwise you can
end up with very long running discovery mode of this tap. Discovery mode is analysing table structures but
Snowflake doesn't like selecting lot of rows from `INFORMATION_SCHEMA` or running `SHOW` commands that returns lot of
rows. Please be as specific as possible.

2. Run it in discovery mode to generate a `properties.json`

3. Edit the `properties.json` and select the streams to replicate

4. Run the tap like any other singer compatible tap:

```
  tap-snowflake --config config.json --properties properties.json --state state.json
```

### Discovery mode

The tap can be invoked in discovery mode to find the available tables and
columns in the database:

```bash
$ tap-snowflake --config config.json --discover

```

A discovered catalog is output, with a JSON-schema description of each table. A
source table directly corresponds to a Singer stream.

## Replication methods

The two ways to replicate a given table are `FULL_TABLE` and `INCREMENTAL`.

Note: Discovery does not include these values in the output catalog, you must add them to
the metadata of the configured tables. Alternatively if you run the tap without a catalog then
it will auto-discover and default to full table replication unless overridden by config metadata.

### Full Table

Full-table replication extracts all data from the source table each time the tap
is invoked.

```
  "metadata": {
    "replication-method": "FULL_TABLE",
    "selected-by-default": false,
    "database-name": "DB_123",
    "schema-name": "SCHEMA_456",
    "row-count": 0,
    "is-view": false,
    "selected": true
  }
```

Additionally, the full table sync can be configured to use a look back window to limit the size of the data set being synced. The look period is from the current time minus the configured rolling_lookback period. `time_unit` is any date or time part [supported by snowflake](https://docs.snowflake.com/en/sql-reference/functions-date-time.html#label-supported-date-time-parts) and the `time_amount` is the positive integer of time units to look backwards. 
```
   "rolling_lookback": {
      "db-schema-table": {
         "time_unit": "day",
         "time_amount": "7",
         "time_column": "DATE_OR_TS_COL_NAME"
      }
   }
```

### Incremental

Incremental replication works in conjunction with a state file to only extract
new records each time the tap is invoked. This requires a replication key to be
specified in the table's metadata as well.

Below is an example of an incremental sync setting for a view. Replication is based on source
data with `UPDATED_DATE` that's `>=` to the current bookmarked value provided in the state.json
file. `view-key-properties` or `table-key-properties` defines the key properties associated with the
view/table being replicated.

```
  "metadata": {
    "view-key-properties": [
      "ID"
    ],
    "replication-key": "UPDATED_DATE",
    "replication-method": "INCREMENTAL",
    "selected-by-default": false,
    "database-name": "DB_123",
    "schema-name": "SCHEMA_456",
    "row-count": 0,
    "is-view": true,
    "selected": true
  }
```

### To run tests:

1. Define environment variables that requires running the tests
```
  export TAP_SNOWFLAKE_ACCOUNT=<snowflake-account-name>
  export TAP_SNOWFLAKE_DBNAME=<snowflake-database-name>
  export TAP_SNOWFLAKE_USER=<snowflake-user>
  export TAP_SNOWFLAKE_PASSWORD=<snowfale-password>
  export TAP_SNOWFLAKE_WAREHOUSE=<snowflake-warehouse>
```

NOTE: User must have permission to create/drop schema (TAP_SNOWFLAKE_TEST), create/drop table, insert into those tables. DEG's implementation uses DATA_DEG_TEST.TAP_SNOWFLAKE_TEST - credentials are in the 1Pass vault.

2. Install python dependencies in a virtual env and run unit and integration tests
```
  python3 -m venv venv
  . venv/bin/activate
  pip install --upgrade pip
  pip install .
  pip install tox
```

3. To run unit tests:
```
  tox
```

## License

Apache License Version 2.0

See [LICENSE](LICENSE) to see the full text.

