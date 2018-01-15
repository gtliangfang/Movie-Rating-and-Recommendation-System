Drop Database if exists Grape;
Create Database Grape;
use Grape;
SET NAMES utf8;
SET CHARACTER SET utf8;
SET character_set_client=utf8;
SET character_set_database=utf8;
SET character_set_results=utf8;
SET character_set_server=utf8;

Drop Table if exists groups;
Create Table groups(
group_id int not null primary key,
name varchar(90) not null,
topic varchar(256) not null,#director
description varchar(256) not null,#genra
create_time timestamp not null default CURRENT_TIMESTAMP,
confirmMessage int,#year
leader_id int not null default 0
)ENGINE=INNODB DEFAULT CHARSET=utf8;


Drop Table if exists user;
Create Table user(
user_id int not null primary key AUTO_INCREMENT,
username varchar(128) not null,
password varchar(128) not null,
email varchar(128) not null,
role int not null default 0
)ENGINE=INNODB DEFAULT CHARSET=utf8;


Drop Table if exists bulletin;
CREATE TABLE bulletin (
bulletin_id int primary key not null AUTO_INCREMENT,
user_id int not null,
group_id int not null,
#title varchar(4) not null,#rate it is string
title float not null,#rate it is string
text varchar(8) not null default " ",
read_num int not null default 0,
create_time timestamp not null default CURRENT_TIMESTAMP,
constraint `BULLETIN_LINK` foreign key (group_id) references groups(group_id) on delete cascade
) ENGINE=INNODB;

Drop Table if exists recommender;
CREATE TABLE recommender (
user_id int not null,
item_id int not null,
score float not null,
rank int not null
);
