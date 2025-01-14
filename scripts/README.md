# Scripts Python

## **nav.py**

Ce script pyhton a pour but de générer une barre de navigation pour le fichier racine `charte.html`. 

### Fonctionnement :
1. **Analyse du fichier HTML** :
   - Parcourt la structure HTML pour trouver, dans la div `docs-content`, les éléments suivants :
     - `article > header > h1`
     - `article > section > h2`
     - `article > section > section > h3`

2. **Création de la navbar** :
   - Ajoute des ancres aux liens du sommaire.
   - Génère un fichier `nav_charte.html` contenant le code de la barre de navigation.

3. **Mise à jour du fichier principal** :
   - Copiez/collez le code de la navbar générée dans le fichier racine `charte.html`.

### Utilisation :
- Exécutez ce script chaque fois que de nouvelles sections sont ajoutées au fichier `charte.html`.

```bash
python nav.py
```


## **url.py**

Ce script Python a pour objectif d'extraire, nettoyer et vérifier les liens hypertexte (`href`) présents dans un fichier racine (`charte.html`). 
Il produit des rapports détaillés sur l'état des liens (valide ou non) et les sauvegarde dans des fichiers textes pour une analyse ultérieure.

## Fonctionnalités

1. **Extraction des liens** :
   - Recherche des balises `<a>` ayant la classe `theme-link` dans le fichier HTML.
   - Extrait les attributs `href` des liens correspondants.

2. **Nettoyage des URLs** :
   - Corrige les espaces mal encodés en les remplaçant par `%20`.
   - Supprime les doublons.

3. **Vérification des liens** :
   - Effectue une requête HTTP `HEAD` pour chaque URL afin de vérifier son statut.
   - Classe les liens en fonction de leur code de statut HTTP (200, 404, etc.).

4. **Génération de rapports** :
   - Sauvegarde les liens uniques triés dans `extracted_links_sorted.txt`.
   - Sauvegarde les liens non valides ou problématiques dans `non_ok_links.txt`.
   - Génère un rapport complet des statuts de tous les liens dans `url_status_report.txt`.


### Utilisation :
- Exécutez ce script chaque fois que de nouveau liens sont ajoutés au fichier `charte.html`. Ou pour faire une vérification à n'importe quel moment.

```bash
python url.py
```