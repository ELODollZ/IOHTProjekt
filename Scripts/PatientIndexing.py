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
    patientname = input("Enter a new patientname: ")
    cursor.execute(f'INSERT INTO {TableNamed} (patientname) VALUE (?)', ())
    print(f"Patient {patientname} added to the PatientListe.")

    patientID = cursor.lastrowid
    patientstablename = f'Patient{patientID}PilListe'
    cursor.execute(f''' 
        CREATE TABLE IF NOT EXISTS {patientstablename} (
            id INTEGER PRIMARY KEY,
            PilName TEXT NOT NULL,
            Amount INTEGER NOT NULL
        )
    ''')
    print(f"PilListe table created for patient '{patientID}'")

def addPatient(cursor, PatientName):
    cursor.execute('INSERT INTO users (PatientName) VALUES (?)', (PatientName,))
    
def addPilsToListe(cursor, userID, PilName, Amount):
    PatientTableName = f'Patient{userID}PilListe'
    cursor.execute(f'INSERT INTO {PatientTableName} (PilName, Amount) VALUES (?, ?)', (PilName, Amount))
    return PatientTableName

def interActiveMenu(cursor, TableNamed):
    while True:
        print("\nAdmin Menu:")
        print("1. Add a new Patient To the Database")
        print("2. Add a new type of medicin for the Patient")
        print("3. Exit out of admin Menu")
        choice = input("Enter you choice (1/2/3): ")

        if choice == '1':
            PatientName = input("Enter Patients full name: ")
            makePatientListe(cursor, PatientName)
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

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='patients'")
    patientsTableExists = cursor.fetchone()

    if not patientsTableExists:
        #makes the tables in the database
        makePatientListe(cursor, TableName)
        conn.commit()

    interActiveMenu(cursor, TableNamed)
    
    conn.commit()
    conn.close()
    print("Something is wrong")
makeNewEntryDatabase(database, TableNamed)

