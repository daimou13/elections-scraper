import csv
import sys
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


def get_soup(url: str) -> BeautifulSoup:
    """Download a web page and return its parsed HTML content."""
    response = requests.get(url)
    response.raise_for_status()

    return BeautifulSoup(response.text, "html.parser")

def get_municipality_cells(soup: BeautifulSoup) -> list:
    """Find and return table cells containing municipality codes."""
    municipality_cells = soup.find_all("td", class_="cislo")
    return municipality_cells

def get_municipality_data(cell, base_url: str) -> tuple[str, str, str]:
    """Extract municipality code, name and detail page URL from a table row."""
    row = cell.find_parent("tr")
    cells = row.find_all("td")

    code = cells[0].get_text(strip=True)
    name = cells[1].get_text(strip=True)

    link = cell.find("a")
    municipality_url = urljoin(base_url, link["href"])

    return code, name, municipality_url

def get_municipalities(
    municipality_cells: list,
    base_url: str,
) -> list[tuple[str, str, str]]:
    """Create a list of municipalities with code, name and detail URL."""
    municipalities = []

    for cell in municipality_cells:
        municipality = get_municipality_data(cell, base_url)
        municipalities.append(municipality)

    return municipalities

def get_summary_data(soup: BeautifulSoup) -> tuple[str, str, str]:
    """Extract registered voters, issued envelopes and valid votes."""
    registered = soup.find("td", headers="sa2")
    envelopes = soup.find("td", headers="sa3")
    valid = soup.find("td", headers="sa6")

    return (
    "".join(registered.get_text(strip=True).split()),
    "".join(envelopes.get_text(strip=True).split()),
    "".join(valid.get_text(strip=True).split()),
    )

def get_party_results(soup: BeautifulSoup) -> list:
    """Extract party names and their vote counts from a municipality page."""
    party_results = []

    party_cells = soup.find_all("td", class_="overflow_name")

    for party_cell in party_cells:
        row = party_cell.find_parent("tr")
        cells = row.find_all("td")

        party_name = party_cell.get_text(strip=True)
        votes = "".join(cells[2].get_text().split())

        party_results.append((party_name, votes))

    return party_results

def get_municipality_result(
    code: str,
    name: str,
    url: str
) -> dict:
    """Build a complete election result dictionary for one municipality."""
    soup = get_soup(url)

    registered, envelopes, valid = get_summary_data(soup)
    party_results = get_party_results(soup)

    result = {
        "code": code,
        "location": name,
        "registered": registered,
        "envelopes": envelopes,
        "valid": valid,
    }

    for party_name, votes in party_results:
        result[party_name] = votes

    return result

def get_all_results(municipalities: list) -> list:
    """Download and collect election results for all municipalities."""
    results = []

    for code, name, municipality_url in municipalities:
        municipality_result = get_municipality_result(
            code,
            name,
            municipality_url,
        )
        results.append(municipality_result)

    return results

def save_to_csv(results: list[dict[str, str]], output_file: str) -> None:
    """Save election results to a CSV file."""
    if not results:
        return

    fieldnames = results[0].keys()

    with open(output_file, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

def is_valid_url(url: str) -> bool:
    """Check whether the URL points to a valid 2017 election district page."""
    return (
        url.startswith("https://volby.gov.cz/pls/ps2017nss/ps32")
        or url.startswith("https://volby.cz/pls/ps2017nss/ps32")
    )

def main() -> None:
    """Validate arguments, scrape election results and save them to CSV."""
    if len(sys.argv) != 3:
        print("Error: Enter URL and output CSV filename.")
        return

    url = sys.argv[1]
    output_file = sys.argv[2]

    if not is_valid_url(url):
        print("Error: Enter a valid election district URL.")
        return
    
    if not output_file.endswith(".csv"):
        print("Error: Output filename must end with .csv.")
        return

    print(f"Stahuji data z vybraneho URL: {url}")

    soup = get_soup(url)
    municipality_cells = get_municipality_cells(soup)
    municipalities = get_municipalities(municipality_cells, url)

    results = get_all_results(municipalities)

    print(f"Ukladam do souboru: {output_file}")
    save_to_csv(results, output_file)

    print("Hotovo.")

if __name__ == "__main__":
    main()