#!/usr/bin/env python3
#Arthor: NyboMønster

ListOfConfig =[
    r"/home/Gruppe2PI/Projekts/IOHTProjekt/databaseSQLite3/patientDatabase.db",         # DB Path
    "PatientListe",                                                                     # Navn på Index listen af alle patienter
    'Patient{patientID}PilListe'                                                        # Navn på formattering af alle sub lister for hver patients medicin
    ]
RPIServerAddress = "192.168.57.54"
RPIPortNumber = 2902