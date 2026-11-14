# Elections Scraper

Projekt slouží ke stažení výsledků voleb do Poslanecké sněmovny Parlamentu České republiky z roku 2017 z webu volby.gov.cz.

Program načte výsledky všech obcí z vybraného územního celku a uloží je do CSV souboru.

## Instalace

Pro projekt je doporučeno použít virtuální prostředí.

Potřebné knihovny jsou uvedeny v souboru `requirements.txt`.

Instalace knihoven:

```bash
pip install -r requirements.txt
```

## Spuštění programu

Program se spouští z příkazové řádky pomocí dvou argumentů:

```bash
python main.py <URL_uzemniho_celku> <nazev_vystupniho_souboru.csv>
```

První argument je URL vybraného územního celku z webu volby.cz.

Druhý argument je název výstupního CSV souboru.

### Příklad

Výsledky pro okres Benešov:

```bash
python main.py "https://volby.gov.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2101" vysledky_benesov.csv
```

Program následně vypíše například:

```text
Stahuji data z vybraneho URL: https://volby.gov.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2101
Ukladam do souboru: vysledky_benesov.csv
Hotovo.
```

## Výstup

Výsledkem je CSV soubor, kde každý řádek představuje jednu obec.

Soubor obsahuje:

- kód obce,
- název obce,
- počet voličů v seznamu,
- počet vydaných obálek,
- počet platných hlasů,
- počet hlasů pro jednotlivé kandidující strany.

Ukázkový výstup je uložen v souboru `vysledky_benesov.csv`.