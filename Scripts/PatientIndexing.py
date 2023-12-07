#!/usr/bin/env python3
#Arthor: NyboMønster

import sqlite3


#Updating variables
database = r"/home/Gruppe2PI/Projekts/IOHTProjekt/databaseSQLite3/patientDatabase.db"
TableNamed = "PatientListe"
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
    cursor.execute(f''' 
        CREATE TABLE IF NOT EXISTS {TableNamed} (
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

def getDataFromSQLite3Database(cursor, PatientName):
    cursor.execute('SELECT id FROM users WHERE PatientName = ?', (PatientName))
    userID = cursor.fetchone()
    if userID:
        userID = userID[0]
        PatientTableName = f'Patient{userID}PilListe'
        cursor.execute(f'SELECT PilName, amount FROM {PatientTableName}')
        PileListe = cursor.fetchall()
        print(f"PileListe for {PatientName}")
        for item in PileListe:
            print(f"{item[0]}: {item[1]}")
    else:
        print(f"Patient 'PatientName' not found in databaseTable")

def interActiveMenu(cursor, TableNamed):
    while True:
        print("\nAdmin Menu:")
        print("1. Add a new Patient To the Database")
        print("2. Add a new type of medicin for the Patient")
        print("3. Exit out of admin Menu")
        choice = input("Enter you choice (1/2/3): ")

        if choice == '1':
            PatientName = input("Enter Patients full name: ")
            addPatient(cursor, PatientName)
            print("f{PatientName} was added successfully.")
        elif choice == '2':
            PatientName = input("Enter the PatientName to add a pile information for: ")
            cursor.execute('SELECT id FROM TableNamed WHERE PatientName = ?', (PatientName))
            PatientID = cursor.fetchone()
            if PatientID:
                PatientID = PatientID[0]
                PilName = input("Enter a pil name, capitel starting letters: ")
                Amount = input("Enter the amount of piles: ")
                addPilsToListe(cursor, PatientID, PilName, Amount)
                print(f"Pile was added to the patient: '{PatientID}'.")
            else:
                print(f"Patient '{PatientID}' not found in table")
        elif choice == '3':
            print("Exiting Admin Menu.")
            break
        else:
            print("Invalid coihce. Please Enter 1, 2, 3")




def makeNewEntryDatabase(databasename, TableName):
    conn, cursor = makeConnectionForSQLite3DB(database)

    #makes the tables in the database
    makePatientListe(cursor, TableName)
    
    interActiveMenu(cursor, TableNamed)
    
    conn.commit()
    conn.close()
    print("Something is wrong")
makeNewEntryDatabase(database, TableNamed)

