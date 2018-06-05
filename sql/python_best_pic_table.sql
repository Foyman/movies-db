DELETE FROM BestPic;:

ALTER TABLE BestPic auto_increment = 1;:

LOAD DATA LOCAL INFILE '../csv/best_picture.csv'
INTO TABLE BestPic
FIELDS TERMINATED BY ';'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(title, year, length, genre, winner);:
