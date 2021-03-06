drop database if exists btctradingflask;
create user 'sql_admin'@'localhost' identified by 'sql_admin';
create database btctradingflask;
GRANT ALL PRIVILEGES ON btctradingflask . * TO 'sql_admin'@'localhost';
use btctradingflask;

CREATE TABLE users (
  id int NOT NULL AUTO_INCREMENT,
  username varchar(30) NOT NULL DEFAULT '',
  email varchar(50) NOT NULL DEFAULT '',
  first_name varchar(30) NOT NULL DEFAULT '',
  last_name varchar(50) NOT NULL DEFAULT '',
  password varchar(100) NOT NULL DEFAULT '',
  mobile_phone varchar(20) NOT NULL DEFAULT '',
  user_type int NOT NULL,
  level int DEFAULT NULL,
  street varchar(255) DEFAULT NULL,
  city varchar(100) DEFAULT NULL,
  state varchar(50) DEFAULT NULL,
  zipcode varchar(10) DEFAULT NULL,
  bitcoin_balance float NOT NULL DEFAULT '0',
  fiat_balance float NOT NULL DEFAULT '0',
  total_transaction float DEFAULT '0',
  PRIMARY KEY (id),
  UNIQUE KEY username (username),
  UNIQUE KEY email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE transactions (
  id int NOT NULL AUTO_INCREMENT,
  xid_type varchar(20) NOT NULL DEFAULT '',
  status varchar(30) NOT NULL DEFAULT '',
  client_id int NOT NULL,
  trader_id int NOT NULL,
  timestamp datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  fiat_amount float NOT NULL DEFAULT '0',
  PRIMARY KEY (id),
  KEY payment_client (client_id),
  KEY payment_trader (trader_id),
  CONSTRAINT payment_client FOREIGN KEY (client_id) REFERENCES users (id),
  CONSTRAINT payment_trader FOREIGN KEY (trader_id) REFERENCES users (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE trades (
  id int NOT NULL AUTO_INCREMENT,
  xid_type varchar(20) NOT NULL DEFAULT '',
  status varchar(30) NOT NULL DEFAULT '',
  client_id int NOT NULL,
  trader_id int NOT NULL,
  timestamp datetime NOT NULL,
  fiat_amount float NOT NULL,
  bitcoin_amount float NOT NULL,
  exchange_rate float NOT NULL,
  commission float NOT NULL,
  commission_type varchar(10) NOT NULL DEFAULT '',
  PRIMARY KEY (id),
  KEY client_trade (client_id),
  KEY trader_trade (trader_id),
  CONSTRAINT client_trade FOREIGN KEY (client_id) REFERENCES users (id),
  CONSTRAINT trader_trade FOREIGN KEY (trader_id) REFERENCES users (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE changelogs (
  id int NOT NULL AUTO_INCREMENT,
  timestamp datetime NOT NULL,
  xid int NOT NULL,
  status varchar(255) NOT NULL,
  xid_type varchar(255) NOT NULL,
  client_id int NOT NULL,
  trader_id int NOT NULL,
  PRIMARY KEY (id),
  KEY client_id (client_id),
  KEY trader_id (trader_id),
  KEY xid (xid),
  CONSTRAINT changelogs_ibfk_1 FOREIGN KEY (client_id) REFERENCES users (id),
  CONSTRAINT changelogs_ibfk_2 FOREIGN KEY (trader_id) REFERENCES users (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


INSERT INTO users (username, email, first_name, last_name, password, mobile_phone, user_type, street, city, state, zipcode)
VALUES ('admin', 'admin@example.com', 'admin', 'manager', 'pbkdf2:sha256:150000$oxDpouOh$c5166b20f43c5a1cf398fdca8f401ae724c507d0c08df380dbb769020fca9306',
'1234567890', 1, 'UT Dallas', 'Dallas', 'Texas', '75080');

INSERT INTO users (username, email, first_name, last_name, password, mobile_phone, user_type, street, city, state, zipcode)
VALUES ('bot_trader', 'bot_trader@example.com', 'bot', 'trader', 'pbkdf2:sha256:150000$b9SpYxyd$ce37e32c3b9e18c5720db06e841e22725349673848cbb529350fb6bb2d50d39e',
'1234567809', 2, 'UT Dallas', 'Dallas', 'Texas', '75080');



delimiter $$
create procedure add_clients_traders()
begin
	declare id int;
	set id = 3;
	while id <= 100 do

        INSERT INTO users (username, email, first_name, last_name, password, mobile_phone, user_type, street, city, state, zipcode)
        VALUES (concat('trader', id), concat('trader', id, '@example.com'), concat('trader', id), concat('TraderLast', id), 'pbkdf2:sha256:150000$b9SpYxyd$ce37e32c3b9e18c5720db06e841e22725349673848cbb529350fb6bb2d50d39e',
            concat('4694229', id), 2, 'UT Dallas', 'Dallas', 'Texas', '75080');


        INSERT INTO users (username, email, first_name, last_name, password, mobile_phone, user_type, level, street, city, state, zipcode)
        VALUES (concat('client', id), concat('client', id, '@example.com'), concat('client', id), concat('ClientLast', id), 'pbkdf2:sha256:150000$oRMrdJl8$efb97140f18b93a6d61bc253fbfa45747df12d46bd0481135b1995e7fac87d3e',
            concat('4694229', id), 3, 1, 'UT Dallas', 'Dallas', 'Texas', '75080');
        
        
        set id = id + 1;
	end while;
end; $$


delimiter ;
call add_clients_traders();