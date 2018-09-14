#!Python3
#Automated reporting from PALMS (SQL files\Run > Output reports)
#By Charles Han

import logging, os, glob, csv, sys, datetime#, MySQLdb,
import pymssql

logging.basicConfig(filename = 'log.txt', level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')

SQLFolder = os.getcwd()+'\\SQL files\\Run' #set SQL run file folder path
outputFolder = os.getcwd()+'\\Output reports\\' #set report output file folder

#---Loop through every file in the SQL directory---
for filename in glob.iglob(SQLFolder + '**/*.txt', recursive=True):
    print(filename)
    
    file = os.path.splitext((os.path.basename(filename)))[0] #get just the file name
    logging.debug(file)

#--- read SQL txt file ----
    with open(filename, 'r') as content_file:
        content = content_file.read()
        
#--- connect to database ----  
    server = ""
    userName = ""
    dBase = ""
    print("Logging into %s as %s \nPassword:" %(server , userName))
    password = input()
  
    conn = pymssql.connect(server, userName, password, dBase)
    cursor = conn.cursor()
#row = cursor.fetchone()
#for row in cursor:
#print('row = %r' % (row,))
#data = cursor.fetchall()
# fileOpen.write("\n".join(item))

#--- write output csv file ---
    today = str(datetime.date.today())
    #print(today)
    print('Running report...')
    
    with open(outputFolder + file +' '+ today +'.csv', 'w+') as file_handler:
        cursor.execute(content)
        #print(cursor.description)

        #--- write column names as headings if required ---
        colnames = []
        for desc in cursor.description:
            colnames.append(desc[0]) 
        print (colnames) # print column names
        print("Add above column headings to output file?(y/n):") # ask user for input 
        if input() =='y':
            for desc in cursor.description:
                colnames = desc[0] 
                # print (colnames)
                file_handler.write("%s,"%(colnames))
            file_handler.write("\n") #new line

        #--- write report data ---         
        for item in cursor:            
            for value in item:
                file_handler.write("%s,"%(value))
                #logging.debug(value)
            file_handler.write("\n") #new line
            #csv_out.writerow(item)
            
    #--- close connection to server ---
    conn.close()
    print('Report saved as '+outputFolder + file +' '+ today +'.csv')
#book.save(filename)
