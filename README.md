# world_bank_economy
A project that pulls data from the world bank API and loads it to a duckdb database.

utils: a package that contains configurations for the API and the functions used.

How to use the repository:
1. Install duckdb and python in the virtual environment.
2. Run the python command `fetch_api_data.py` in the terminal. You should see a duckdb database file named `world_economy_data.duckdb` being added to the same folder directory. 
3. Open the database by using the command `duckdb world_economy_data.duckdb`. Run the command `SHOW TABLES;` to get a catalog of all tables available.
4. Go to the sql file `reports.sql` and run the sql command for each report.
