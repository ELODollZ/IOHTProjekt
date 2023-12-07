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
    return PatientTableName
def getDataFromSQLite3Database(cursor, PullRequested):
    pullRequest = f'''SELECT * FROM {PullRequested}'''
    cursor.execute(pullRequest)
    output = cursor.fetchall()
    for row in output:
        print(row)



def GetUserInputForTesting():
    pullData = False
    adduser = input("Do you want to add a user entry?(True/False): ")
    adduser = eval(adduser)
    if (adduser == True):
        username = input("Enter a name for Patient: ")
        PilName = input("Name the Pil with starting Capitel letter: ")
        Amount = input("How Many of this type of Pil?: ")
    pullData = input("Do you want to see the data in database?(True/False): ")
    pullData = eval(pullData)
    newInput == False
    if (adduser == False):
        return bool(adduser), PatientName, PilName, Amount, bool(pullData)
    if (adduser == True):
        return bool(adduser), bool(pullData)
def makeNewEntryDatabase(databasename, TableName):
    conn, cursor = makeConnectionForSQLite3DB(database)
    adduser = GetUserInputForTesting()
    if adduser == True:
        adduser, PatientName, PilName, Amount, PullData = GetUserInputForTesting()
    else:
        adduser, PullData = GetUserInputForTesting()
    #makes the tables in the database
    makePatientListe(cursor, TableName)
    
    if newInput == False:
        #if adduser == True:
        #   addPatient(cursor, PatientName)
        userIDTemp = cursor.fetchall()
        if isinstance(userIDTemp, int):
            userID = userIDTemp
            print(userID)
            makePilListe(cursor, userID)
        else:
            userID = input("Patient name?: ")
            makePilListe(cursor, userID)
            PatientTableName = addPilsToListe(cursor, userID, PilName, Amount)
            if PullData == True:
                var1 = getDataFromSQLite3Database(cursor, PatientTableName)
            elif PullData == False:
                print("Not Requested data from database")
            else:
                print("Error in code pulling data")
    if newInput == True:
        addPatient(cursor, PatientName)
    if newInput == True:
        
        conn.commit()
    if newInput == False:
        conn.commit()
        conn.close()
    else:
        conn.close()
        print("Something is wrong")
makeNewEntryDatabase(database, TableName)



