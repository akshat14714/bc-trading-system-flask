# bc-trading-system-flask

CS 6360 Term Project 
* Akshat Maheshwari (AXM210024)
* Vallabh Ashish Kedarisetti (VXK200001)
* Vaishnavi Mehare (VXM200054)


## Tools:
* Python 3
* Flask
* MySQL
* Python3 Packages:
   * flask
   * flask-sqlalchemy
   * flask-cors
   * sqlalchemy
   * pymysql
   * werkzeug.security
   * configparser
   * apscheduler (runs Gold/Silver update once a month)


## Install:
The application first requires that Python3, pip and MySQL are installed.  With a running instance of MySQL,  the following scripts should be run via the command-line in the root folder of the application.

```
mysql -u [root user] -p < sql_queries.sql
source bin/activate
pip3 install -r requirements.txt
export FLASK_CONFIG='development'
export FLASK_ENV='development'
export FLASK_APP='app.py'
```

These commands create:
 1) Users with the usernames like 'client12' and password 'password';
 2) Traders with usernames like 'trader12' and password 'trader_hacker'
 3) 1 manager with username 'admin' and password 'admin123'

## Run:
```
flask run
```


