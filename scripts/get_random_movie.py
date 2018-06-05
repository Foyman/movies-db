import sys
import MySQLdb as mc

year_min = 1927
year_max = 2017
length_min = 66
length_max = 248
genre = ''
genres_table = [["Action","ACT"],["Adventure","ADV"],["Animation","ANI"],
               ["Biographic","BIO"],["Comedy","COM"],["Crime","CRI"],
               ["Documentary","DOC"],["Drama","DRA"],["Epic","EPIC"],
               ["Family","FAM"],["Fantasy","FANT"],["History","HIS"],
               ["Horror","HOR"],["Independent","INDY"],["Musical","MUS"],
               ["Mystery","MYS"],["Political","POL"],["Romance","ROM"],
               ["Sci-Fi","SCIFI"],["Silent","SIL"],["Sports","SPR"],
               ["Thriller","THR"],["War","WAR"],["Western","WEST"]]

def executeSQLScripts(c, filename):
    fd = open(filename, 'r')
    sqlFile = fd.read()
    fd.close()
    sqlCommands = sqlFile.split(';:')
    for command in sqlCommands:
        #print command
        try:
            c.execute(command)
        except mc.Error as msg:
            print ("Command skipped: " + str(msg))
    return

def checkValues(value_min, value_max):
    if value_max > 2017:
        value_max = 2017
    if value_max < 1917:
        value_max = 1917
    if value_min > 2017:
        value_min = 2017
    if value_min < 1917:
        value_min = 1917
    if value_min > value_max:
        temp = value_max
        value_max = value_min
        value_min = temp

def getStatement(x):
    return {
        1: "winner = 1",
        2: "year >= " + str(year_min) + " AND year <= " + str(year_max),
        3: "length >= " + str(length_min) + " AND length <= " + str(length_max),
        4: "genre like '%" + genre + "%'"
    }.get(x,"")

def updateMovieQuery(var):
    global randNum
    global randMovie
    if "WHERE" not in randNum:
        #print "Adding WHERE"
        randNum += " WHERE "
        randMovie += " WHERE "
    else:
        #print "Adding AND"
        randNum += " AND "
        randMovie += " AND "
    randNum += str(getStatement(var))
    randMovie += str(getStatement(var))
    return

#Main Function
connection = mc.connect (host = "localhost",
                 user = "root",
                 passwd = "BVhs2013")
cursor = connection.cursor()
executeSQLScripts(cursor, '../sql/python_db_setup.sql')
executeSQLScripts(cursor, '../sql/python_best_pic_table.sql')

cursor.execute("SELECT * from BestPic")
result = cursor.fetchall()
# for r in result:
#     print(r)

print("All yes or no questions should be answered with 1 for Yes, and 0 for No")
on = 0
while(on != 1):
    randNum = "SELECT FLOOR(RAND() * (SELECT COUNT(*) FROM BestPic"
    randMovie = "SELECT * FROM BestPic"
    win = input("Would you like only movies that won? ")
    if (int(win) == 1):
        print("Looking for winner")
        updateMovieQuery(1)

    year_select = input("Would you like to set a year range? ")
    if int(year_select) == 1:
        year_min = int(input("Set year min (lowest is 1927): "))
        year_max = int(input("Set year max (highest is 2017): "))
        checkValues(year_min, year_max)
        updateMovieQuery(2)

    length_select = input("Would you like to set a length range? ")
    if int(length_select) == 1:
        length_min = int(input("Set length min (lowest is 66): "))
        length_max = int(input("Set length max (highest is 266): "))
        checkValues(length_min, length_max)
        updateMovieQuery(3)

    genre_select = input("Would you like to select a genre? ")
    if int(genre_select) == 1:
        valid_genre = 0
        while not valid_genre:
            genre = input("Choose a genre (type 'help' for genres): ")
            if genre.lower() == "help":
                for i in genres_table:
                    print ("%s\t%s" % (i[1],i[0]))
            if any(genre in sublist for sublist in genres_table):
                #print "VALID"
                valid_genre = 1
        updateMovieQuery(4)

    print (randNum + "))")
    cursor.execute(randNum + "))")
    data = cursor.fetchone()
    print (str(int(data[0])))
    randMovie += " LIMIT 1 OFFSET " + str(int(data[0]))
    cursor.execute(randMovie)
    data = cursor.fetchone()
    if data is not None:
        print (data)
    else:
        print ("No movie fits that criteria")
    # if int(data[0]) != 0:
    #     randMovie += " LIMIT 1 OFFSET " + str(int(data[0]))
    #     #print (randMovie)
    #     cursor.execute(randMovie)
    #     data = cursor.fetchone()
    #     print (data)
    # else:
    #     print ("No movie fits that criteria")

    on = int(input("Would you like to quit? "))
#print(year_min, year_max, length_min, length_max)

cursor.close()
connection.close()
