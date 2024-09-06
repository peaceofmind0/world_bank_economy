# world_bank_economy
A project that pulls data from the world bank API and loads it to a duckdb database.

utils: a package that contains configurations for the API and the functions used.
`api_config.py`: provides configuration data
`api_funcs.py`: contains functions used to call the API and process the response data
`indicator_search.py`: return a list of indicators in the world bank database based on key words provided.

How to use the repository:
1. Install duckdb and python in the virtual environment.
2. Run the python command `fetch_api_data.py` in the terminal. You should see a duckdb database file named `world_economy_data.duckdb` being added to the same folder directory. The database `world_economy_data.duckdb` has already been generated and can be directly used. Calling the python process will fetch the latest updated data.
3. Open the database by using the command `duckdb world_economy_data.duckdb`. Run the command `SHOW TABLES;` to get a catalog of all tables available.
4. Go to the sql file `reports.sql` and run the sql command for each report.
