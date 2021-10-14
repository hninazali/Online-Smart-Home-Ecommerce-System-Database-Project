# BT2102 Assignment 1 - Online Smart Home Ecommerce System Database Project (Group 9)

## ✏️ About 
With the advent and popularity of ecommerce, more and more consumers are purchasing smart-home equipment  online. A company that focuses its business on smart home equipment has decided to incorporate a new Online Smart  Home Ecommerce System. The company’s in-house IT team is expected to deliver a database software application  (named “OSHES”) to manage product sales, administration, and maintenance.  

_This project is part of the module BT2102: Data Management and Visualisation, where students are tasked to create an OSHES (Online Smart Home Ecommerce System) using only Python, MySQL and MongoDB._

<p align="center">
  <img src="https://i.imgur.com/ZfmBDbd.png" width=600 />
</div>

## 🛠️ Python Environment Setup
1. cd to directory of your choice and use the following commands to install through `requirements.txt` file. 
```
python3 -m venv ./env
```
2. Activate through `env/Scripts/activate.ps1` (for Windows) or `source env/bin/activate` (for Mac). This will install necessary sql and mongo libraries (pymysql, pymongo, sqlalchemy). Install dependencies
```
pip install -r requirements.txt
```
3. Change python environment in VSCode in pyvenv.cfg file to
```
home = ./env/bin..
```

## 🚀 Building and Running for Production

After you pull the codes
1. Run the sql scripts to create databases and tables
``` 
cd db_connections
python3 mysqldb.py
```
2. Create customer and admin in mySQL workbench
3. Run gui.py file 
```
python3 gui.py
```

## 💻 Tech Stack
| Libraries and Frameworks Used  | Frontend & Databases |
| ------------- | ------------- |
| Tkinter  | 	Frontend GUI |
| MySQL  | Database |
| MongoDB  | Database |

## 👨‍💻👩‍💻 Contributors
1. HNIN AZALI
2. LEE ZHI XUAN
3. NG SEOW TENG
4. RYAN GOH SHI JUN
5. WINY FEBRINY INDAYANG
6. YUKI NEO WEI QIAN
