#!/usr/bin/env python3
#Arthor: NyboMønster

import sqlite3
from ConfigFile import ListOfConfig as Conf
# Updating variables
#database = r"/home/Gruppe2PI/Projekts/IOHTProjekt/databaseSQLite3/patientDatabase.db"
#TableNamed = "PatientListe"
#PileListeFormat = 'Patient{patientID}PilListe'

# Function
def makeConnectionForSQLite3DB(databaseName):
    conn = sqlite3.connect(databaseName)
    return conn, conn.cursor()

# Function to make tables
def makePatientListe(cursor, TableNamed):
    cursor.execute(f''' 
        CREATE TABLE IF NOT EXISTS {TableNamed} (
            id INTEGER PRIMARY KEY,
            patientname TEXT NOT NULL
        ) 
    ''')
    patientname = input("Enter a new patientname: ")
    cursor.execute(f'INSERT INTO {TableNamed} (patientname) VALUES (?)', (patientname,))
    print(f"Patient {patientname} added to the PatientListe.")

    patientID = cursor.lastrowid
    patientstablename = Conf[2].format(patientID=patientID)
    cursor.execute(f''' 
        CREATE TABLE IF NOT EXISTS {patientstablename} (
            id INTEGER PRIMARY KEY,
            PilName TEXT NOT NULL,
            Amount INTEGER NOT NULL
        )
    ''')
    print(f"PilListe table created for patient '{patientID}'")

def addPilsToListe(cursor, userID, PilName, Amount):
    user_id = None
    if userID and userID.isnumeric():
        user_id = int(userID)
    else:
        cursor.execute(f'SELECT id FROM {Conf[1]} WHERE patientname = ?', (userID,))
        result = cursor.fetchone()
        if result:
            user_id = result[0]
    if user_id is not None:
        PatientTableName = f'Patient{user_id}PilListe'
        cursor.execute(f'INSERT INTO {PatientTableName} (PilName, Amount) VALUES (?, ?)', (PilName, Amount))
        return PatientTableName

def displayContentOfTable(cursor, patientID, PileListeFormat):
    user_id = None
    if patientID and patientID.isnumeric():
        user_id = int(patientID)
    else:
        cursor.execute(f'SELECT id FROM {Conf[1]} WHERE patientname = ?', (patientID,))
        result = cursor.fetchone()
        if result:
            user_id = result[0]

    if user_id is not None:
        PileListeFormat = PileListeFormat.format(patientID=user_id)
        cursor.execute(f'SELECT * FROM {PileListeFormat}')
        tableContent = cursor.fetchall()
        if tableContent:
            print(f"Content of table '{PileListeFormat}':")
            for row in tableContent:
                print(row)
        else:
            print(f"Table '{PileListeFormat}' is empty.")
    else:
        print(f"Patient '{patientID}' is not found in the table.")

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
            userID = input("Enter the PatientName to add a pile information for: ")
            PilName = input("Enter a pil name, capitel starting letters: ")
            Amount = input("Enter the amount of piles: ")
            addPilsToListe(cursor, userID, PilName, Amount)
            print(f"Pile was added to the patient: '{userID}'.")

        elif choice == '3':
            userID = input("Enter the PatientName or ID-Number to display the content of table for: ")
            displayContentOfTable(cursor, userID, PileListeFormat)

        elif choice == '4':
            print("Exiting Admin Menu.")
            break

        else:
            print("Invalid choice. Please Enter 1, 2, 3, or 4")

def DataBaseControl(databasename, TableName, PileListeFormat):
    conn, cursor = makeConnectionForSQLite3DB(databasename)

    cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{TableName}'")
    patientsTableExists = cursor.fetchone()

    if not patientsTableExists:
        # makes the tables in the database
        makePatientListe(cursor, TableName)
        conn.commit()

    interActiveMenu(cursor, TableName, PileListeFormat)

    conn.commit()
    conn.close()
    print("Closing Database")

#DataBaseControl(Conf[0], Conf[1], Conf[2])
