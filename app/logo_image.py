import requests
from bs4 import BeautifulSoup
import wikipediaapi
import os

def get_car_brand_logo(brand_name, save_path='car_logos/logo.jpg'):
    """
    Recherche le logo d'une marque de voiture sur Wikipédia et le télécharge.

    Args:
        brand_name (str): Nom de la marque de voiture (ex : "Toyota", "BMW", etc.)
        save_path (str): Chemin complet où enregistrer le logo (par défaut 'logo.jpg').

    Returns:
        str: Chemin du fichier image enregistré ou message d'erreur.
    """
    # Initialisation de l'API Wikipedia avec un User-Agent
    wiki_wiki = wikipediaapi.Wikipedia(
        language='en',
        user_agent='MyCarLogoBot/1.0 (https://example.com; contact@example.com)'
    )

    # Rechercher la page de la marque
    page = wiki_wiki.page(brand_name)
    if not page.exists():
        return f"La page Wikipédia pour la marque '{brand_name}' n'existe pas."

    # Récupération de l'URL de la page de Wikipédia
    page_url = page.fullurl
    print(f"Page Wikipédia trouvée : {page_url}")

    # Télécharger le contenu HTML de la page
    response = requests.get(page_url)
    if response.status_code != 200:
        return "Impossible de récupérer la page Wikipédia."

    soup = BeautifulSoup(response.content, 'html.parser')

    # Chercher la première image de l'infobox
    infobox = soup.find('table', {'class': 'infobox'})
    if infobox is None:
        return "Aucune infobox trouvée sur la page."

    image_tag = infobox.find('img')
    if image_tag is None:
        return "Aucune image trouvée dans l'infobox."

    image_url = 'https:' + image_tag['src']
    print(f"URL de l'image du logo : {image_url}")

    # Télécharger l'image
    try:
        image_response = requests.get(image_url, headers={'User-Agent': 'MyCarLogoBot/1.0'})
        if image_response.status_code == 200:
            # Créer le dossier s'il n'existe pas
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            with open(save_path, 'wb') as f:
                f.write(image_response.content)
            print(f"Logo de {brand_name} enregistré sous {save_path}")
            return save_path
        else:
            return "Impossible de télécharger l'image."
    except Exception as e:
        return f"Erreur lors du téléchargement de l'image : {e}"

# Exemple d'utilisation
if __name__ == "__main__":
    logo_path = get_car_brand_logo("Iran Khodro", "../car_logos/logo.jpg")