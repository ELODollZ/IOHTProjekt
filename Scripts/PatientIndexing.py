#!/usr/bin/env python3
#Arthor: NyboMønster

import sqlite3


#Updating variables
database = r"/home/Gruppe2PI/Projekts/IOHTProjekt/databaseSQLite3/patientDatabase.db"
TableName = "PatientListe"
PatientName = "Sarah"
PilName = "PainKiller"
Amount = 2
newInput = False
TheInput = "Name"
#Function 
def makeConnectionForSQLite3DB(databaseName):
    conn = sqlite3.connect(databaseName)
    return conn, conn.cursor()
    
#Function to make tables
def makePatientListe(cursor, TableNamed):
    TableName = TableNamed
    cursor.execute(f''' 
        CREATE TABLE IF NOT EXISTS {TableName} (
            id integer PRIMARY KEY,
            patientname text NOT NULL
        ) 
    ''')

def makePilListe(cursor, userID):
    patientstablename = f'Patient{userID}PilListe'
    cursor.execute(f''' 
        CREATE TABLE IF NOT EXISTS {patientstablename} (
            id INTEGER PRIMARY KEY,
            PilName TEXT NOT NULL,
            Amount INTEGER NOT NULL
        )
    ''')


def addPatient(cursor, PatientName):
    cursor.execute('INSERT INTO users (PatientName) VALUES (?)', (PatientName,))
    
def addPilsToListe(cursor, userID, PilName, Amount):
    PatientTableName = f'Patient{userID}PilListe'
    cursor.execute(f'INSERT INTO {PatientTableName} (PilName, Amount) VALUES (?, ?)', (PilName, Amount))    
def getDataFromSQLite3Database(cursor, PullRequested):
    pullRequest = f'''SELECT * FROM {PullRequested}'''
    cursor.execute(pullRequest)
    output = cursor.fetchall()
    for row in output:
        print(row)



def GetUserInputForTesting():
    pullData = False
    username = input("Enter a name for Patient: ")
    PilName = input("Name the Pil with starting Capitel letter: ")
    Amount = input("How Many of this type of Pil?: ")
    pullData = input("Do you want to see the data in database?()True/False: ")
    newInput == False
    return PatientName, PilName, Amount, pullData
def makeNewEntryDatabase(databasename, TableName):
    conn, cursor = makeConnectionForSQLite3DB(database)
    PatientName, PilName, Amount, PullData = GetUserInputForTesting()
    print(PullData)
    #makes the tables in the database
    makePatientListe(cursor, TableName)
    
    if newInput == False:
        if PullData == True:
            var1 = getDataFromSQLite3Database()
            print(var1)
        elif PullData == False:
            print("Not Requested data from database")
        else:
            print("Error in code pulling data")
        userIDTemp = cursor.fetchall()
        if isinstance(userIDTemp, int):
            userID = userIDTemp
            print(userID)
            makePilListe(cursor, userID)
        else:
            userID = input("Patient number?: ")
            makePilListe(cursor, userID)
            addPilsToListe(cursor, userID, PilName, Amount)
    if newInput == True:
        addPatient(cursor, username)
    if newInput == True:
        
        conn.commit()
    if newInput == False:
        conn.commit()
        conn.close()
    else:
        conn.close()
        print("Something is wrong")
makeNewEntryDatabase(database, TableName)



