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
   * waitress (WSGI server)
   * configparser
   * WTForms
   * apscheduler (runs Gold/Silver update once a month)


## Install:
The application first requires that Python3, pip and MySQL are installed.  With a running instance of MySQL,  the following scripts should be run via the command-line in the root folder of the application.

```
mysql -u [root user] -p < MySql_Statements.sql
source bin/activate
pip3 install -r requirements.txt
export FLASK_CONFIG='development'
export FLASK_ENV='development'
export FLASK_APP='app.py'
```

Alternative to the last command, we can run it with `flask run`.

Optionally, at this point we can run a `flask shell` instance, and then we  run a set of scripts to create fake users and activity.

```
flask shell
>> import create_user
>> create_user.create_manager()
>> create_user.create_clients()
>> create_user.create_traders()
```

These commands create:
 1) 100 users with the usernames like 'abc12' and password 'password'; 
 2) 100 traders with usernames like 'trader12' and password 'trader_hacker'; and 
 3) 1 manager with username 'admin' and password 'admin123.'

## Run:
```
flask run
```


