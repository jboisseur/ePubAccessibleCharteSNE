import os
from bs4 import BeautifulSoup

# Charger le fichier HTML
input_file = "../../charte-image.html"

with open(input_file, "r", encoding="utf-8") as file:
    html_content = file.read()

# Parser le contenu HTML complet
soup = BeautifulSoup(html_content, "html.parser")

# Isoler le contenu dans <div class="docs-content">
docs_content = soup.find("div", class_="docs-content")
if not docs_content:
    raise ValueError("Le contenu 'docs-content' n'a pas été trouvé dans le fichier HTML.")

# Trouver toutes les balises concernées (h1, h2, h3 dans la hiérarchie)
elements = docs_content.select("article > header > h1, article > section > h2, article > section > section > h3")

# Générer le contenu de la liste de navigation
nav_items = []
for element in elements:
    parent = element.find_parent(["article", "section"])
    parent_id = parent.get("id", "id_non_trouvé")  # Récupérer l'ID du parent ou un ID par défaut
    if element.name == "h1":
        nav_items.append(f'<li class="nav-item section-title"><a class="nav-link scrollto active" href="#{parent_id}">{element.get_text(strip=True)}</a></li>')
    elif element.name == "h2":
        nav_items.append(f'<li class="nav-item"><a class="nav-link scrollto" href="#{parent_id}">{element.get_text(strip=True)}</a></li>')
    elif element.name == "h3":
        nav_items.append(f'<li class="nav-item sous-item"><a class="nav-link scrollto" href="#{parent_id}">{element.get_text(strip=True)}</a></li>')

# Générer le contenu HTML complet avec le menu de navigation
nav_html = f"""
<!DOCTYPE html>
<html lang="fr"> 
<head>
    <title>Menu de navigation</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="assets/css/theme.css">
</head>
<body>
<nav id="docs-nav" class="docs-nav navbar">
    <ul class="section-items list-unstyled nav flex-column pb-3">
        {'\n        '.join(nav_items)}
    </ul>
</nav>
</body>
</html>
"""

# Sauvegarder le fichier de navigation HTML
output_nav_file = "nav_charte.html"
with open(output_nav_file, "w", encoding="utf-8") as file:
    file.write(nav_html)

# Afficher le fichier généré
print(f"Fichier de navigation généré : {output_nav_file}")
