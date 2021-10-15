# BT2102 Assignment 1 - Online Smart Home Ecommerce System Database Project (Group 9)

## ✏️ About 
With the advent and popularity of ecommerce, more and more consumers are purchasing smart-home equipment  online. A company that focuses its business on smart home equipment has decided to incorporate a new Online Smart  Home Ecommerce System. The company’s in-house IT team is expected to deliver a database software application  (named “OSHES”) to manage product sales, administration, and maintenance.  

_This project is part of the module BT2102: Data Management and Visualisation, where students are tasked to create an OSHES (Online Smart Home Ecommerce System) using only Python, MySQL and MongoDB._

<p align="center">
  <img src="https://i.imgur.com/ZfmBDbd.png" width=600 />
</div>

## 🛠️ Environment Setup
1. cd to directory of your choice and use the following commands to install through `requirements.txt` file. 
```
python3 -m venv ./env
```
2. Activate through `env/Scripts/activate.ps1` (for Windows) or `source env/bin/activate` (for Mac).

3. To install dependencies : 
```
pip install -r requirements.txt
```
4. Change python environment in VSCode or IDE to the one you have created : 
```
home = ./env/bin..
```

Ensure that MySQL is set up locally with the following credentials:
```
user: 'root'
password: 'password'
port: 3306
mysql_db: 'oshes'
host: localhost
```
Ensure that MongoDB is set up locally with the following credentials:
```
mongo_uri: 'mongodb://localhost:27017'
database_name: 'oshes'
```

## 🚀 Running the app in production

1. Ensure that you have an empty schema "oshes" on your SQL Workbench. 
2. Run gui.py
```
python gui.py
```
3. Log in as Administrator with the following credentials : 
```
User ID : admin1 
Password : password
```
You will need to first login as an admin to initialise the database by pressing the "Initialise Data" button on the Admin Portal Home Page. 



## 💻 Tech Stack
| Libraries and Frameworks  | Usage |
| ------------- | ------------- |
| Tkinter  | 	Frontend GUI |
| Python | Frontend, Backend |
| MySQL  | Database |
| MongoDB  | Database |

## 👨‍💻👩‍💻 Contributors
1. HNIN AZALI BRENDA YANG
2. LEE ZHI XUAN
3. NG SEOW TENG
4. RYAN GOH SHI JUN
5. WINY FEBRINY INDAYANG
6. YUKI NEO WEI QIAN
