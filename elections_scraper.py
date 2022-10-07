"""
elections_scraper.py: třetí projekt do Engeto Online Python Akademie
author: Martin Žůrek
email: zurek.m@email.cz
discord: MartinZ#0894
"""

import requests
from bs4 import BeautifulSoup
import os
import csv
import random
import time
import sys


def stahni_html_kod(url_adresa: str) -> BeautifulSoup:
    """
    Funkce stahne html kod z webu. Vrati naparsovany kod, pripraveny k prohledavani.

    Beautifulsoup =
    <html><body>
    ... telo ...
    </body></html>

    :param url_adresa: "url_adresa"
    :return: objekt BeautifulSoup
    """
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0"}
    for _ in range(5):
        try:
            odpoved = requests.get(url_adresa, headers=headers)
            continue
        except requests.exceptions.ConnectionError as e:
            print(f"error: {e}")
            time.sleep(1 * random.random())
    return BeautifulSoup(odpoved.text, "html.parser")


def vytvor_list_v_listu(odkazy_na_mesta_obce: list) -> list[list]:
    """
    Funkce vytvori prazdny list listu, do ktereho budou ulozena volebni data.

    :param odkazy_na_mesta_obce: [odkaz1, odkaz2, odkaz3, ...]
    :return: [[], [], [], [], ...]
    """
    list_v_listu = []
    # Nadefinuje list v listu podle poctu obci. Pro kazdou obec jeden list. Napr.: [[],[],[]]
    # Prvni list je pro hlavicku souboru
    for idx in range(len(odkazy_na_mesta_obce) + 1):
        list_v_listu.append([])
    return list_v_listu


def stahni_odkazy_na_mesta_obce(html_kod_okresu: BeautifulSoup, prvni_cast_url: str) -> list:
    """
    Funkce stahne odkazy na volebni vysledky mest/obci v zadanem okrese.

    Ukazka vystupu:

    ['https://www.volby.cz...obec=506761&xvyber=7103',
    'https://www.volby.cz...obec=589268&xvyber=7103',
    'https://www.volby.cz...obec=589276&xvyber=7103' ...]

    :param html_kod_okresu: "odkaz_na_okres"
    :param prvni_cast_url: "prvni_cas_url"
    :return: [odkaz1, odkaz2, odkaz3, ...]
    """
    bs_obj = html_kod_okresu
    tabulka = bs_obj.find_all("tr")
    odkazy_na_mesta_obce = []
    for tr in tabulka:
        odkaz_na_mesto_obci = tr.find("td", {"class": "cislo"})
        if odkaz_na_mesto_obci:
            odkazy_na_mesta_obce.append(prvni_cast_url + tr.find("a").get("href"))
    return odkazy_na_mesta_obce


def stahni_data_okresu(html_kod_okresu: BeautifulSoup, odkazy_na_mesta_obce: list) -> list[list]:
    """
    Funkce stahne data daneho okresu a ulozi je do listu listu.

    Ukazka vystupu:

    [['Kód', 'Lokalizace', 'Voliči v seznamu', 'Vydané obálky', 'Platné hlasy'],
    ['506761', 'Alojzov'], ['589268', 'Bedihošť'], ['589276', 'Bílovice-Lutotín'],
    ['589284', 'Biskupice'], ...]

    :param html_kod_okresu: objekt Beautifulsoup
    :param odkazy_na_mesta_obce: [odkaz1, odkaz2, odkaz3, ...]
    :return: [[hlavicka], [obec1], [obec2], [obec3], ...]
    """
    data_okresu = vytvor_list_v_listu(odkazy_na_mesta_obce)
    # Zacatek hlavicky na prvnim radku csv souboru
    data_okresu[0] = ["Kód", "Lokalizace", "Voliči v seznamu", "Vydané obálky", "Platné hlasy"]
    bs_obj = html_kod_okresu
    tabulka = bs_obj.find_all("tr")
    idx_okres = 1
    for tr in tabulka:
        data_kod = tr.find("td", {"class": "cislo"})
        data_mesto = tr.find("td", {"class": "overflow_name"})
        if data_kod:
            data_okresu[idx_okres].extend([data_kod.text, data_mesto.text])
            idx_okres += 1
    return data_okresu


def stahni_data_mesta_obce(odkazy_na_mesta_obce: list) -> list[list]:
    """
    Funkce stahne data daneho mesta/obce a ulozi je do listu listu.

    Ukazka vystupu:

    [['Občanská demokratická strana', 'Řád národa - Vlastenecká unie', ...],
    ['205', '145', '144', '29', ...], ['834', '527', '524', '51', ...],
    ['431', '279', '275', '13', ...], ['238', '132', '131', '14', ...], ...]

    :param odkazy_na_mesta_obce: [odkaz1, odkaz2, odkaz3, ...]
    :return: [[hlavicka], [obec1], [obec2], [obec3], ...]
    """
    data_mesta_obce = vytvor_list_v_listu(odkazy_na_mesta_obce)
    idx_mesto_obec = 1
    vytvor_hlavicku = True
    for odkaz in odkazy_na_mesta_obce:
        bs_obj = stahni_html_kod(odkaz)
        tabulka = bs_obj.find_all("tr")
        for tr in tabulka:
            volici_v_seznamu = tr.find("td", {"headers": "sa2"})
            vydane_obalky = tr.find("td", {"headers": "sa3"})
            platne_hlasy = tr.find("td", {"headers": "sa6"})
            if volici_v_seznamu:
                data_mesta_obce[idx_mesto_obec].extend([volici_v_seznamu.text, vydane_obalky.text, platne_hlasy.text])
            nazev_strany = tr.find("td", {"class": "overflow_name"})
            pocet_hlasu = tr.find_all("td", {"class": "cislo"})
            if nazev_strany:
                data_mesta_obce[idx_mesto_obec].append(pocet_hlasu[1].text)
                if vytvor_hlavicku:
                    data_mesta_obce[0].append(nazev_strany.text)
        idx_mesto_obec += 1
        vytvor_hlavicku = False
    return data_mesta_obce


def vygeneruj_celkova_volebni_data_okresu(data_okresu: list[list], data_mesta_obce: list[list]) -> list[list]:
    """
    Funkce spoji dohromady data okresu a data mest a obci.

    Ukazka vystupu:

    [['Kód', 'Lokalizace', 'Voliči v seznamu', 'Vydané obálky', 'Platné hlasy', ...],
    ['506761', 'Alojzov', '205', '145', '144', ...],
    ['589276', 'Bílovice-Lutotín', '431', '279', '275', ...], ...]

    :param data_okresu: [[hlavicka], [obec1], [obec2], [obec3], ...]
    :param data_mesta_obce: [[hlavicka], [obec1], [obec2], [obec3], ...]
    :return: [[hlavicka], [obec1], [obec2], [obec3], ...]
    """
    velikost_pole = len(data_okresu)
    for i in range(velikost_pole):
        data_okresu[i].extend(data_mesta_obce[i])
    celkova_volebni_data = data_okresu
    return celkova_volebni_data


def vygeneruj_csv_soubor(nazev_csv_souboru: str, data_pro_csv_tabulku: list[list]) -> None:
    """
    Funkce vytvori .csv soubor.

    :param nazev_csv_souboru: "nazev_csv_souboru"
    :param data_pro_csv_tabulku: [[], [], [], [], ...]
    :return: None
    """
    print(f"Ukladam stazena data do souboru: {nazev_csv_souboru}")
    # Nastaveni oddelovace na středník
    csv.register_dialect('myDialect', delimiter=';', quoting=csv.QUOTE_NONE)
    # Nachystani noveho souboru na zapis
    nove_csv = open(nazev_csv_souboru, mode="w", newline='', encoding='utf-8')
    # Vytvoreni noveho csv souboru
    zapisovac = csv.writer(nove_csv, dialect='myDialect')
    # Zaspis stazenych dat do csv souboru
    for idx in range(len(data_pro_csv_tabulku)):
        zapisovac.writerow(data_pro_csv_tabulku[idx])
    # Uzavreni csv souboru
    nove_csv.close()


def kontrola_vstupnich_parametru_python_programu() -> None:
    """
    Funkce zkontroluje pocet a spravnost zadanych vstupnich parametru python souboru.

    :return: None
    """
    # Spusteny program ma 3 argumenty (0 - vzdy nazev souboru, 1 - url, 2 - nazev csv souboru)
    if len(sys.argv) == 1:
        sys.exit("Pro spuštění zadej 2 parametry: 'URL' mezera 'nazev_souboru.csv'")
    elif len(sys.argv) == 2:
        sys.exit("Pro spusteni chybi zadat jeden z argumentu: 'URL' mezera 'nazev_souboru.csv'")
    elif len(sys.argv) == 3:
        if "https://www.volby.cz/" not in sys.argv[1]:
            sys.exit("Spatne zadana html adresa. Prvni cast adresy musi byt ve tvaru: https://www.volby.cz/")
        # [-4:] - vybere posledni 4 znaky ve stringu
        if sys.argv[2][-4:] != ".csv":
            sys.exit("Spatne zadana pripona csv souboru. Soubor musi mit priponou .csv")
    else:  # argv > 3:
        sys.exit("Zadal jsi prilis mnoho argumentu")


def main():

    prvni_cast_url = "https://www.volby.cz/pls/ps2017nss/"
    # url = "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103"
    # nazev_csv_souboru = "prostejov_vysledky.csv"
    url = sys.argv[1]
    nazev_csv_souboru = sys.argv[2]

    os.system("cls")
    kontrola_vstupnich_parametru_python_programu()
    print(f"Stahuji data ze zadaneho URL: {url}")
    html_kod_okresu = stahni_html_kod(url)
    odkazy_na_mesta_obce = stahni_odkazy_na_mesta_obce(html_kod_okresu, prvni_cast_url)
    data_okresu = stahni_data_okresu(html_kod_okresu, odkazy_na_mesta_obce)
    data_mesta_obce = stahni_data_mesta_obce(odkazy_na_mesta_obce)
    celkova_volebni_data_okresu = vygeneruj_celkova_volebni_data_okresu(data_okresu, data_mesta_obce)
    vygeneruj_csv_soubor(nazev_csv_souboru, celkova_volebni_data_okresu)
    print("Ukoncuji elections_scraper.py")


if __name__ == "__main__":
    main()
