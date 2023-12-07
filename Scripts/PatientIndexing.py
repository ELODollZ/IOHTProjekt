#!/usr/bin/env python3
#Arthor: NyboMønster

import sqlite3


#Updating variables
database = r"/home/Gruppe2PI/Projekts/IOHTProjekt/databaseSQLite3/patientDatabase.db"
TableNamed = "PatientListe"
PileListeFormat = 'Patient{patientID}PilListe'

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
    cursor.execute(f'INSERT INTO {TableNamed} (patientname) VALUES (?)', (patientname,))
    print(f"Patient {patientname} added to the PatientListe.")

    patientID = cursor.lastrowid
    patientstablename = PileListeFormat.format(patientID=patientID)
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
    userID = None
    if userID.isdigit():
        userID = int(userID)
    else:
        cursor.execute(f'SLEELCT id FROM {TableNamed} WHERE PatientName = ?', (userID,))
        result = cursor.fetchone()
        if result:
            userID = result[0]
    if userID is not None:
        PatientTableName = f'Patient{userID}PilListe'
        cursor.execute(f'INSERT INTO {PatientTableName} (PilName, Amount) VALUES (?, ?)', (PilName, Amount))
        return PatientTableName
    
def displayContentOfTable(cursor, patientID, PileListeFormat):
    userID = None
    if userID.isdigit():
        userID = int(userID)
    else:
        cursor.execute(f'SLEELCT id FROM {TableNamed} WHERE PatientName = ?', (userID,))
        result = cursor.fetchone()
        if result:
            userID = result[0]
            
    if userID is not None:
        PileListeFormat = PileListeFormat.format(patientID=patientID)
        cursor.execute(f'SELECT * FROM {patientID}')
        tableContent = cursor.fetchall()
        if tableContent:
            print(f"Content of table '{PileListeFormat}':")
            for each in PileListeFormat:
                print(each)
            else:
                print(f"Table '{PileListeFormat}' is empty.")

def interActiveMenu(cursor, TableNamed, PileListeFormat):
    while True:
        print("\nAdmin Menu:")
        print("1. Add a new Patient To the Database")
        print("2. Add a new type of medicin for the Patient")
        print("3. Display content of a Patients PilListe")
        print("4. Exit out of admin Menu")
        choice = input("Enter you choice (1/2/3/4): ")

        if choice == '1':
            makePatientListe(cursor, TableNamed)
        
        elif choice == '2':
            PatientName = input("Enter the PatientName to add a pile information for: ")
            cursor.execute(f'SELECT id FROM {TableNamed} WHERE PatientName = ?', (PatientName,))
            patientID = cursor.fetchone()
            if patientID:
                patientID = patientID[0]
                PilName = input("Enter a pil name, capitel starting letters: ")
                Amount = input("Enter the amount of piles: ")
                addPilsToListe(cursor, patientID, PilName, Amount)
                print(f"Pile was added to the patient: '{patientID}'.")
            else:
                print(f"Patient '{patientID}' not found in table")
        elif choice == '3':
            PatientName = input("Enter the PatientName to display the content of table for: ")
            cursor.execute(f'SELECT id FROM {TableNamed} WHERE PatientName= ?', (PatientName,))
            patientID = cursor.fetchone()
            if patientID:
                patientID = patientID[0]
                displayContentOfTable(cursor, patientID, PileListeFormat)
            else:
                print(f"Patient '{patientID}' is not found in table")
                
        elif choice == '4':
            print("Exiting Admin Menu.")
            break
        
        else:
            print("Invalid choice. Please Enter 1, 2, 3, or 4")


def makeNewEntryDatabase(databasename, TableName, PileListeFormat):
    conn, cursor = makeConnectionForSQLite3DB(databasename)

    cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{TableNamed}'")
    patientsTableExists = cursor.fetchone()

    if not patientsTableExists:
        #makes the tables in the database
        makePatientListe(cursor, TableName)
        conn.commit()

    interActiveMenu(cursor, TableNamed, PileListeFormat)
    
    conn.commit()
    conn.close()
    print("Closing Database")
makeNewEntryDatabase(database, TableNamed, PileListeFormat)

