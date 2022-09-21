"""
Elections_scraper.py: třetí projekt do Engeto Online Python Akademie
author: Martin Žůrek
email: zurek.m@email.cz
discord: MartinZ#0894
"""

import requests
from bs4 import BeautifulSoup
import os
import csv
import sys

os.system("cls")

# Spusteny program ma 3 argumenty (0 - vzdy nazev souboru, 1 - URL, 2 - nazev csv souboru)
if len(sys.argv) == 1:
    sys.exit("Pro spusteni chybi zadat dva argumenty")
if len(sys.argv) == 2:
    sys.exit("Pro spusteni chybi zadat jeden z argumentu")
if len(sys.argv) == 3:
    # [:17] - vybere prvnich 16 znaku ve stringu 
    if sys.argv[1][:17] != "https://volby.cz/":
            sys.exit("Spatne zadana html adresa")
    # [-4:] - vybere posledni 4 znaky ve stringu 
    if sys.argv[2][-4:] != ".csv":
            sys.exit("Spatne zadana pripona csv souboru. Soubor nekonci priponou .csv")
if len(sys.argv) > 3:
    sys.exit("Pri spusteni jsi zadal prilis mnoho argumentu")

# URL = "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103"
URL = sys.argv[1]
odpoved = requests.get(URL)
bs_obj = BeautifulSoup(odpoved.text, "html.parser")

# V promenne csv_soubor je ulozen nazev souboru do ktereho se ulozi data
csv_soubor = sys.argv[2]

print(f"Stahuji data ze zadaneho URL: {URL}")

# Ulozi do listu vsechny odkazy na obce
odkazy = [0]
for td_1 in bs_obj.find_all("td", {"class": "cislo"}):
    # print(td_1.find("a").get("href"))
    odkazy.append(td_1.find("a").get("href"))

# print(odkazy)

# print(len(odkazy))

# Nadefinuje list v listu podle poctu obci
data = []
for idx in range(len(odkazy)):
    data.append([])

# print(len(data))

# print(data)

# Zacatek hlavicky na prvnim radku csv souboru
data[0] = ["Kód", "Lokalizace", "Voliči v seznamu", "Vydané obálky", "Platné hlasy"]

i = 1
uloz_hlavicku = True

# Projde vsechny bunky, ktere jsou potreba stahnout
for tr_1 in bs_obj.find_all("tr"):

    # Prvni dva "tr" nemaji "td" a byly by v csv 2 radky mezera
    zvysit_i_1 = True

    # Cislo obce napr.: 506761
    try:
        # print(tr_1.find("td", {"class": "cislo"}).text)
        data[i].append(tr_1.find("td", {"class": "cislo"}).text)
    except:
        zvysit_i_1 = False

    # Nazev obce napr.: Alojzov
    try:
        # print(tr_1.find("td", {"class": "overflow_name"}).text)
        data[i].append(tr_1.find("td", {"class": "overflow_name"}).text)
    except:
        zvysit_i_1 = False

    # Chceme prozkoumat odkaz pouze pokud jsme v "tr" v obci 
    if zvysit_i_1 == True:
        
        # URL odkaz konkretni obce
        URL_2 = "https://volby.cz/pls/ps2017nss/" + str(odkazy[i])
        # print(URL_2)
        odpoved_2 = requests.get(URL_2)
        bs_obj_2 = BeautifulSoup(odpoved_2.text, "html.parser")

        for tr_2 in bs_obj_2.find_all("tr"):

            # Ulozi hlavicku souboru pouze jednou
            if uloz_hlavicku == True:

                # Kolonka "Strana nazev"
                # Pro strany, ktere jsou vlevo
                try:
                    # print(tr_2.find("td", {"headers": "t1sa1 t1sb2"}).text)
                    data[0].append(tr_2.find("td", {"headers": "t1sa1 t1sb2"}).text)
                except:
                    pass

                # Kolonka "Strana nazev"
                # Pro strany, ktere jsou vpravo
                try:
                    # print(tr_2.find("td", {"headers": "t1sa2 t1sb3"}).text)
                    data[0].append(tr_2.find("td", {"headers": "t2sa1 t2sb2"}).text)
                except:
                    pass

            # Kolonka "Volici v seznamu" napr.: 205
            try:
                # print(tr_2.find("td", {"headers": "sa2"}).text)
                data[i].append(tr_2.find("td", {"headers": "sa2"}).text)
            except:
                pass

            # Kolonka "Vydane obalky" napr.: 145
            try:
                # print(tr_2.find("td", {"headers": "sa3"}).text)
                data[i].append(tr_2.find("td", {"headers": "sa3"}).text)
            except:
                pass

            # Kolonka "Platne hlasy" napr.: 144
            try:
                # print(tr_2.find("td", {"headers": "sa6"}).text)
                data[i].append(tr_2.find("td", {"headers": "sa6"}).text)
            except:
                pass

            # Kolonka "Platne hlasy celkem" napr.: 29
            # Pro strany, ktere jsou vlevo
            try:
                # print(tr_2.find("td", {"headers": "t1sa2 t1sb3"}).text)
                data[i].append(tr_2.find("td", {"headers": "t1sa2 t1sb3"}).text)
            except:
                pass

            # Kolonka "Platne hlasy celkem" napr.: 29
            # Pro strany, ktere jsou vpravo
            try:
                # print(tr_2.find("td", {"headers": "t1sa2 t1sb3"}).text)
                data[i].append(tr_2.find("td", {"headers": "t2sa2 t2sb3"}).text)
            except:
                pass

        uloz_hlavicku = False       
        
    # Zvysit inkrement chceme pouze pokud jsme v bunce s daty obce.
    if zvysit_i_1 == True:
        i += 1

# print(data[0])


print(f"Ukladam do souboru: {csv_soubor}")

################################################################################
# Generovani CSV
################################################################################

# Nastaveni oddelovace na středník
csv.register_dialect('myDialect', delimiter=';', quoting=csv.QUOTE_NONE)

# Nachystani noveho souboru na zapis
# Kdyz nenapisu newline='' tak budu mit mezi radky mezeru
nove_csv = open(csv_soubor, mode="w",  newline='')

# Vytvoreni noveho csv souboru
zapisovac = csv.writer(nove_csv, dialect='myDialect')

# Zaspis stazenych dat do csv souboru
for idx in range(len(odkazy)):
    zapisovac.writerow(data[idx])

# Uzavreni csv souboru
nove_csv.close()

print("Ukoncuji Elections scraper")