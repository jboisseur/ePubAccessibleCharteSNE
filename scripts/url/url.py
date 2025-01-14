import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote, unquote, urlparse, urlunparse

# Fonction pour encoder les espaces non encodés en %20
def clean_url(url):
    # Décoder d'abord pour récupérer les espaces encodés en %20
    decoded_url = unquote(url)
    # Remplacer les espaces par %20
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

# Extraction des liens href des balises <a> avec la classe "theme-link"
theme_links = soup.find_all("a", class_="theme-link")
urls = [link.get("href") for link in theme_links if link.get("href")]

# Supprimer les doublons, corriger les espaces, et trier les URLs par ordre alphabétique
unique_sorted_urls = sorted(set(clean_url(url) for url in urls))

# Tester chaque URL et collecter les résultats
url_statuses = []
non_ok_urls = []  # Liste des URLs qui ne sont pas OK
for url in unique_sorted_urls:
    try:
        response = requests.head(url, timeout=5)  # Effectue une requête HEAD pour minimiser la charge
        status = response.status_code
        if status == 200:
            url_statuses.append(f"{url} -> OK")
        else:
            url_statuses.append(f"{url} -> HTTP {status}")
            non_ok_urls.append(f"{url} -> HTTP {status}")  # Ajouter l'URL avec son code d'erreur
    except requests.RequestException as e:
        url_statuses.append(f"{url} -> Erreur ({e})")
        non_ok_urls.append(f"{url} -> Erreur ({e})")  # Ajouter l'URL avec l'erreur

# Sauvegarder les URLs triées sans doublons dans un fichier texte
output_sorted_links_file = "extracted_links_sorted.txt"
with open(output_sorted_links_file, "w", encoding="utf-8") as file:
    file.write("\n".join(unique_sorted_urls))

# Sauvegarder les URLs qui ne sont pas OK dans un fichier texte (avec le code d'erreur)
output_non_ok_links_file = "non_ok_links.txt"
with open(output_non_ok_links_file, "w", encoding="utf-8") as file:
    file.write("\n".join(non_ok_urls))

# Sauvegarder les résultats des tests dans un fichier texte (avec les codes d'erreur)
output_url_status_file = "url_status_report.txt"
with open(output_url_status_file, "w", encoding="utf-8") as file:
    file.write("\n".join(url_statuses))

# Afficher les fichiers générés
print(f"Fichier des liens triés et sans doublons généré : {output_sorted_links_file}")
print(f"Fichier des liens non OK généré : {output_non_ok_links_file}")
print(f"Rapport des statuts d'URLs généré : {output_url_status_file}")
