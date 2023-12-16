#!/usr/bin/env python3
#Arthor: NyboMønster

import sqlite3
from ConfigFile import ListOfConfig as Conf

# Function
def makeConnectionForSQLite3DB(databaseName):
    conn = sqlite3.connect(databaseName)
    return conn, conn.cursor()

# Function to make tables
def makePatientListe(cursor, conn, TableNamed):
    cursor.execute(f'DROP TABLE IF EXISTS {TableNamed}')
    cursor.execute(f''' 
        CREATE TABLE IF NOT EXISTS {TableNamed} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patientname TEXT NOT NULL,
            diagnose TEXT,
            changeStatus BOOLEAN
        ) 
    ''')
    patientname = input("Enter a new patientname: ")
    print(f"DEBUG: patient name entered: {patientname}")
    cursor.execute(f'INSERT INTO {TableNamed} (patientname, diagnose, changeStatus) VALUES (?, ?, ?)', (patientname, "", False))
    print(f"Patient {patientname} added to the PatientListe.")

    patientID = cursor.lastrowid
    print(f"DEBUG: patient ID lastrowid: {patientID}")
    patientsTableName = Conf[2].format(patientID=patientID)
    cursor.execute(f''' 
        CREATE TABLE IF NOT EXISTS {patientsTableName} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            PilName TEXT NOT NULL,
            Amount INTEGER NOT NULL,
            diagnose TEXT,
            changeStatus BOOLEAN
        )
    ''')
    print(f"PilListe table created for patient '{patientID}'")
    conn.commit()

def addPilsToListe(cursor, conn, userID, PilName, Amount, diagnose, changeStatus, TableNamed):
    if userID and str(userID).isnumeric():
        userid = int(userID)
        print("userid is a integere", userid)
    else:
        cursor.execute(f"SELECT id FROM {TableNamed} WHERE patientname = ?", (userID,))
        result = cursor.fetchone()
        if result:
            userid = result[0]
        else:
            print(f"Patient '{userID}' not found")
            return
    PatientTableName = f'Patient{userid}PilListe'
    cursor.execute(f'INSERT INTO {PatientTableName} (PilName, Amount, diagnose, changeStatus) VALUES (?, ?, ?, ?)', (PilName, Amount, diagnose, changeStatus))
    conn.commit()
    print(f"Pile type was added to patient: '{userid}'")

def displayContentOfTable(cursor, patientID, PileListeFormat):
    userID = None
    if patientID and patientID.isnumeric():
        userID = int(patientID)
    else:
        cursor.execute(f'SELECT id FROM {Conf[1]} WHERE patientname = ?', (patientID,))
        result = cursor.fetchone()
        if result:
            userID = result[0]

    if userID is not None:
        PileListeFormat = Conf[2].format(patientID=userID)
        cursor.execute(f'SELECT * FROM {PileListeFormat}')
        tableContent = cursor.fetchall()
        if tableContent:
            print(f"Content of table '{PileListeFormat}':")
            for row in tableContent:
                 print([str(col, 'utf-8') if isinstance(col, bytes) else col for col in row])
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
    if tableContent:
        patientID = tableContent[0]
        patientTableName = Conf[2].format(patientID=patientID)
        cursor.execute(f"SELECT * FROM {patientTableName}")
        pilListeData = cursor.fetchall()
        combinedData = {'PatientData': tableContent, 'PileListData': pilListeData}
        return combinedData
    else:
        print(f"No data found for '{PatientInfo}'")
        return None

global StoreData
StoreData = None

def interActiveMenu(conn, cursor, TableNamed, PileListeFormat):
    global StoreData
    while True:
        print("\nAdmin Menu:")
        print("1. Add a new Patient To the Database")
        print("2. Add a new type of medicin for the Patient")
        print("3. Display content of a Patients PilListe")
        print("4. Save displayed data to variable")
        print("5. Exit out of admin Menu")
        
        choice = input("Enter you choice (1/2/3/4/5): ")

        if choice == '1':
            makePatientListe(cursor, conn, TableNamed)
        elif choice == '2':
            userID = input("Enter the PatientName to add a pile information for: ")
            PilName = input("Enter a pil name, capitel starting letters: ")
            Amount = input("Enter the amount of piles: ")
            diagnose = input("What diagnose does the patient have?: ")
            changeStatus = input("Has the diagnose changed? (True/False): ")
            addPilsToListe(cursor, conn, userID, PilName, Amount, diagnose, changeStatus, TableNamed)
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
                if 'PileListData' in StoreData:
                    print("\nPilListe Details:")
                    for PileData in StoreData['PileListData']:
                        print([str(col, 'utf-8') if isinstance(col, bytes) else col for col in PileData])
                else:
                    print("No PileListe Data found in the table.")
            else:
                print(f"No data to save for '{PatientInfo}'.")
            conn.commit()
            return StoreData
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

    outputFromMenu = interActiveMenu(conn, cursor, TableName, PileListeFormat)

    conn.commit()
    conn.close()
    print("Closing Database")
    return outputFromMenu
