# Online-Smart-Home-Ecommerce-System-Database-Project

## Python Environment Setup
1. cd to directory of your choice and use the following commands to install through `requirements.txt` file. 
```
python3 -m venv ./env
```
2. Activate through `env/Scripts/activate.ps1` (for Windows) or `source env/bin/activate` (for Mac). This will install necessary sql and mongo libraries (pymysql, pymongo, sqlalchemy)
```
pip install -r requirements.txt
```
3. Change python environment in VSCode to ./env/bin..


After you pull the codes
1. Run the sql scripts to create databases and tables
``` 
cd db_connections
python3 mysqldb.py
```
2. Create customer and admin in SQL
3. Run gui.py file 