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
        print(f"Pile type was added to patient: '{user_id}'")
    else:
        print(f"Patient 'user_id' not found.")

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

def GetDataFormPatientsListe(cursor, PatientInfo):
    if PatientInfo.isnumeric():
        cursor.execute(f'SELECT * FROM {Conf[1]} WHERE id = ?', (PatientInfo,))
    else:
        cursor.execute(f'SELECT * FROM {Conf[1]} WHERE patientname = ?', (PatientInfo,))
    tableContent = cursor.fetchone()
    print(tableContent)
    if tableContent:
        patientID = tableContent[0]
        patientTableName = Conf[2].format(patientID=patientID)
        cursor.execute(f"SELECT * FROM {patientTableName}")
        pilListeData = cursor.fetchall()
        combinedData = {'PatientData': tableContent, 'PileListData': pilListeData}
        return combinedData
    else:
        return None



def interActiveMenu(conn, cursor, TableNamed, PileListeFormat):
    StoreData = None
    while True:
        print("\nAdmin Menu:")
        print("1. Add a new Patient To the Database")
        print("2. Add a new type of medicin for the Patient")
        print("3. Display content of a Patients PilListe")
        print("4. Save displayed data to variable")
        print("5. Exit out of admin Menu")
        
        choice = input("Enter you choice (1/2/3/4/5): ")

        if choice == '1':
            makePatientListe(cursor, TableNamed)

        elif choice == '2':
            userID = input("Enter the PatientName to add a pile information for: ")
            PilName = input("Enter a pil name, capitel starting letters: ")
            Amount = input("Enter the amount of piles: ")
            addPilsToListe(cursor, userID, PilName, Amount)
            print(f"Pile was added to the patient: '{userID}'.")
            conn.commit()

        elif choice == '3':
            userID = input("Enter the PatientName or ID-Number to display the content of table for: ")
            StoreData = displayContentOfTable(cursor, userID, PileListeFormat)
        
        elif choice == '4':
            PatientInfo = input("Enter the PatientInfo or ID-Number for outputting: ")
            StoreData = GetDataFormPatientsListe(cursor, PatientInfo)
            if StoreData:
                print("Search Result:")
                if 'pilListeData' in StoreData:
                    print(StoreData)
                    print("\nPilListe Details:")
                    for PileData in StoreData:
                        print(PileData)
                else:
                    print("No PileListe Data found in the table.")
            else:
                print(f"No data to save for '{PatientInfo}'.")
            conn.commit()
        elif choice == '5':
            print("Exiting Admin Menu.")
            break

        else:
            print("Invalid choice. Please Enter 1, 2, 3, 4 or 5")

def DataBaseControl(databasename, TableName, PileListeFormat):
    conn, cursor = makeConnectionForSQLite3DB(databasename)

    cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{TableName}'")
    patientsTableExists = cursor.fetchone()

    if not patientsTableExists:
        # makes the tables in the database
        makePatientListe(cursor, TableName)
        conn.commit()

    interActiveMenu(conn, cursor, TableName, PileListeFormat)

    conn.commit()
    conn.close()
    print("Closing Database")

