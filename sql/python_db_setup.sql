drop database if exists movies;:
create database movies;:
use movies;:

CREATE TABLE BestPic (
  id int auto_increment primary key,
  title varchar(200) not null,
  year int not null,
  length int not null,
  genre varchar(100) null,
  winner boolean not null,
  UNIQUE (title, year)
);:
