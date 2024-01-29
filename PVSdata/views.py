import os
from ftplib import FTP
from django.http import JsonResponse
from django.shortcuts import render
from dotenv import load_dotenv
import shutil

# Carica le variabili d'ambiente dal file .env
load_dotenv()

# Leggi le variabili d'ambiente per le credenziali FTP
ftp_server = os.getenv("FTP_SERVER")
ftp_username = os.getenv("FTP_USERNAME")
ftp_password = os.getenv("FTP_PASSWORD")

# Funzione per la connessione al server FTP, download e organizzazione dei file
def download_files(request):
    try:
        # Connetti al server FTP
        ftp = FTP(ftp_server)
        ftp.login(ftp_username, ftp_password)

        # Cartella di destinazione per il download
        download_folder = "XSTOCK"

        # Stampa un messaggio di debug
        print("Connessione FTP avvenuta con successo!")

        # Funzione per verificare se un file contiene la parola "XLOT" nel nome
        def contains_xlot(file_name):
            return "XLOT" not in file_name

        # Funzione per il download dei file Excel da una cartella
        def download_excel_files(folder_path, destination_folder):
            for file_name in ftp.nlst(folder_path):
                if file_name.endswith(".xlsx") and "PVSPIV-STOCKS1" in file_name and contains_xlot(file_name):
                    local_file_path = os.path.join(destination_folder, file_name)
                    with open(local_file_path, "wb") as local_file:
                        ftp.retrbinary("RETR " + file_name, local_file.write)

        # Esegui il download dei file dalla cartella desiderata
        download_excel_files("/OUT", download_folder)

        # Chiudi la connessione FTP
        ftp.quit()

        # Restituisci una risposta JSON di conferma
        return JsonResponse({"message": "Download completato!"})

    except Exception as e:
        # Stampa un messaggio di errore
        print(f"Errore durante la connessione FTP: {str(e)}")

        # Restituisci una risposta JSON di errore
        return JsonResponse({"error": f"Errore durante la connessione FTP: {str(e)}"}, status=500)
