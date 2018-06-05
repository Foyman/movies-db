/*
SET @rowcount := (SELECT FLOOR(RAND() * (SELECT COUNT(*) FROM BestPic WHERE @parameters)));
SET @sql := CONCAT('SELECT * FROM BestPic WHERE @parameters LIMIT 1 OFFSET ', @rowcount);
*/
SET @rowcount := (SELECT FLOOR(RAND() * (SELECT COUNT(*) FROM BestPic WHERE winner = 1)));
SET @sql := CONCAT('SELECT * FROM BestPic WHERE winner = 1 LIMIT 1 OFFSET ', @rowcount);

PREPARE stmt1 FROM @sql;
EXECUTE stmt1;
