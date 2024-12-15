import requests
from bs4 import BeautifulSoup
import wikipediaapi

def get_car_brand_logo(brand_name, save_path='logo.png'):
    """
    Recherche le logo d'une marque de voiture sur Wikipédia et le télécharge.
    
    Args:
        brand_name (str): Nom de la marque de voiture (ex : "Toyota", "BMW", etc.)
        save_path (str): Chemin complet où enregistrer le logo (par défaut 'logo.png').
        
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
    response = requests.get(page_url, headers={'User-Agent': 'MyCarLogoBot/1.0 (https://example.com; contact@example.com)'})
    if response.status_code != 200:
        return f"Impossible de récupérer la page Wikipédia. Statut: {response.status_code}"
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Chercher la première image de l'infobox
    infobox = soup.find('table', {'class': 'infobox'})
    if infobox is None:
        return "Aucune infobox trouvée sur la page."
    
    image_tag = infobox.find('img')
    if image_tag is None:
        return "Aucune image trouvée dans l'infobox."
    
    # Vérifier si l'URL de l'image commence par '//', 'http', ou 'https'
    src = image_tag.get('src')
    if src.startswith('//'):
        image_url = 'https:' + src
    elif src.startswith('http://') or src.startswith('https://'):
        image_url = src
    else:
        image_url = 'https://en.wikipedia.org' + src  # Cas relatif
    
    print(f"URL de l'image du logo : {image_url}")
    
    # Télécharger l'image avec un User-Agent
    headers = {
        'User-Agent': 'MyCarLogoBot/1.0 (https://example.com; contact@example.com)'
    }
    try:
        image_response = requests.get(image_url, headers=headers)
        print(f"Statut de la réponse de l'image: {image_response.status_code}")
        if image_response.status_code == 200:
            with open(save_path, 'wb') as f:
                f.write(image_response.content)
            print(f"Logo de {brand_name} enregistré sous {save_path}")
            return save_path
        else:
            return f"Impossible de télécharger l'image. Statut: {image_response.status_code}"
    except Exception as e:
        return f"Erreur lors du téléchargement de l'image : {e}"

def get_group_logo(group_name, save_path='group_logo.png'):
    """
    Recherche le logo d'un groupe automobile sur Wikipédia et le télécharge.
    
    Args:
        group_name (str): Nom du groupe automobile (ex : "Volkswagen Group", "Toyota Group", etc.)
        save_path (str): Chemin complet où enregistrer le logo (par défaut 'group_logo.png').
        
    Returns:
        str: Chemin du fichier image enregistré ou message d'erreur.
    """
    # Initialisation de l'API Wikipedia avec un User-Agent
    wiki_wiki = wikipediaapi.Wikipedia(
        language='en', 
        user_agent='MyCarGroupLogoBot/1.0 (https://example.com; contact@example.com)'
    )
    
    # Rechercher la page du groupe
    page = wiki_wiki.page(group_name)
    if not page.exists():
        return f"La page Wikipédia pour le groupe '{group_name}' n'existe pas."
    
    # Récupération de l'URL de la page de Wikipédia
    page_url = page.fullurl
    print(f"Page Wikipédia trouvée : {page_url}")
    
    # Télécharger le contenu HTML de la page
    response = requests.get(page_url, headers={'User-Agent': 'MyCarGroupLogoBot/1.0 (https://example.com; contact@example.com)'})
    if response.status_code != 200:
        return f"Impossible de récupérer la page Wikipédia. Statut: {response.status_code}"
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Chercher la première image de l'infobox
    infobox = soup.find('table', {'class': 'infobox'})
    if infobox is None:
        return "Aucune infobox trouvée sur la page."
    
    image_tag = infobox.find('img')
    if image_tag is None:
        return "Aucune image trouvée dans l'infobox."
    
    # Vérifier si l'URL de l'image commence par '//', 'http', ou 'https'
    src = image_tag.get('src')
    if src.startswith('//'):
        image_url = 'https:' + src
    elif src.startswith('http://') or src.startswith('https://'):
        image_url = src
    else:
        image_url = 'https://en.wikipedia.org' + src  # Cas relatif
    
    print(f"URL de l'image du logo : {image_url}")
    
    # Télécharger l'image avec un User-Agent
    headers = {
        'User-Agent': 'MyCarGroupLogoBot/1.0 (https://example.com; contact@example.com)'
    }
    try:
        image_response = requests.get(image_url, headers=headers)
        print(f"Statut de la réponse de l'image: {image_response.status_code}")
        if image_response.status_code == 200:
            with open(save_path, 'wb') as f:
                f.write(image_response.content)
            print(f"Logo du groupe {group_name} enregistré sous {save_path}")
            return save_path
        else:
            return f"Impossible de télécharger l'image. Statut: {image_response.status_code}"
    except Exception as e:
        return f"Erreur lors du téléchargement de l'image : {e}"

if __name__ == "__main__":
    # Exemple pour la marque Volvo
    # logo_path = get_car_brand_logo("Volvo", "volvo_logo.png")
    # print(logo_path)
    
    # Exemple pour le groupe Toyota
    logo_path = get_group_logo("Volvo", "volvo_group_logo.png")
    print(logo_path)
