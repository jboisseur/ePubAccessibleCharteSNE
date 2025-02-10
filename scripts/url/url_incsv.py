import os
import csv
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote, unquote

# Fonction pour encoder les espaces non encodés en %20
def clean_url(url):
    decoded_url = unquote(url)
    encoded_url = quote(decoded_url, safe=":/#?=&")
    return encoded_url

# Charger le fichier HTML
input_file = "../../charte.html"

with open(input_file, "r", encoding="utf-8") as file:
    html_content = file.read()

# Parser le contenu HTML complet
soup = BeautifulSoup(html_content, "html.parser")

# Isoler le contenu dans <div class="docs-content">
docs_content = soup.find("div", class_="docs-content")
if not docs_content:
    raise ValueError("Le contenu 'docs-content' n'a pas été trouvé dans le fichier HTML.")

# Extraction des liens href et des libellés des balises <a> avec la classe "theme-link"
theme_links = soup.find_all("a", class_="theme-link")
links_data = [(link.get_text(strip=True), clean_url(link.get("href"))) for link in theme_links if link.get("href")]

# Tester chaque URL et collecter les résultats
url_statuses = []
non_ok_urls = []  # Liste des URLs qui ne sont pas OK
csv_data = []

for text, url in links_data:
    try:
        response = requests.head(url, timeout=5)
        status = response.status_code
        state = "OK" if status == 200 else f"HTTP {status}"
        if status != 200:
            non_ok_urls.append(f"{url} -> {state}")
    except requests.RequestException as e:
        state = f"Erreur ({e})"
        non_ok_urls.append(f"{url} -> {state}")
    
    url_statuses.append(f"{url} -> {state}")
    csv_data.append([text, url, state])

# Sauvegarder les URLs triées sans doublons dans un fichier texte
output_sorted_links_file = "extracted_links_sorted.txt"
with open(output_sorted_links_file, "w", encoding="utf-8") as file:
    file.write("\n".join(url for _, url in sorted(set(links_data), key=lambda x: x[1])))

# Sauvegarder les URLs qui ne sont pas OK dans un fichier texte
output_non_ok_links_file = "non_ok_links.txt"
with open(output_non_ok_links_file, "w", encoding="utf-8") as file:
    file.write("\n".join(non_ok_urls))

# Sauvegarder les résultats des tests dans un fichier texte
output_url_status_file = "url_status_report.txt"
with open(output_url_status_file, "w", encoding="utf-8") as file:
    file.write("\n".join(url_statuses))

# Sauvegarder les résultats dans un fichier CSV avec séparateur ; et encodage UTF-8 avec BOM
output_csv_file = "url_status_report.csv"
with open(output_csv_file, "w", encoding="utf-8-sig", newline='') as file:
    writer = csv.writer(file, delimiter=';')
    writer.writerow(["Libellé", "Lien", "État"])
    writer.writerows(csv_data)

# Afficher les fichiers générés
print(f"Fichier des liens triés et sans doublons généré : {output_sorted_links_file}")
print(f"Fichier des liens non OK généré : {output_non_ok_links_file}")
print(f"Rapport des statuts d'URLs généré : {output_url_status_file}")
print(f"Fichier CSV des liens généré : {output_csv_file}")
