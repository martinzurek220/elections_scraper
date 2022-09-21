# Elections scraper
Třetí závěrečný projekt na Python Akademii od Engeta

## Popis projektu
Tento projekt slouží ke stažení výsledků z parlamentních voleb v roce 2017.
Odkaz je zde: https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ

## Instalace knihoven
Knihovny, které jsou použity v kódu jsou uložené v souboru `requirements.txt`. Pro instalaci doporučuji použít nové virtuální prostředí a s nainstalovaným manažerem spustit následovně:
```
$ pip3 --version                    # overim verzi manazeru
$ pip3 install -r requirements.txt  # nainstalujeme knihovny
```

## Spuštění projektu
Spuštění souboru `Elections_scraper.py` v rámci příkazového řádku požaduje dva povinné argumenty.
```
python Elections_scraper <odkaz-uzemniho-celku> <vysledny-soubor>
```
Následně se vám stáhnou výsledky jako soubor s příponou `.csv`.

## Ukázka projektu
Výsledky hlasování pro okres Prostějov:
 1. argument: `https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103`
 2. argument: `vysledky_prostejov.csv`

Spuštění programu:
```
python elections_scraper.py 'https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103' 'vysledky_prostejov.csv'
```

Průběh stahování:
```
Stahuji data ze zadaneho URL: https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103
Ukladam do souboru: vysledky_prostejov.csv
Ukoncuji Elections scraper
```

Částečný výstup:
```
Kód;Lokalizace;Voliči v seznamu;Vydané obálky;Platné hlasy;...
506761;Alojzov;205;145;144;29;0;0;9;0;5;17;4;1;1;0;0;18;0;5;32;0;0;6;0;0;1;1;15;0
589268;Bedihošť;834;527;524;51;0;0;28;1;13;123;2;2;14;1;0;34;0;6;140;0;0;26;0;0;0;0;82;1
...
```



