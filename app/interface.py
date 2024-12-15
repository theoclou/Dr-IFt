import streamlit as st
from car_search.sparql_manager import SparqlManager

# Initialize SPARQL manager (global for reuse)
manager = SparqlManager()

# Define page functions
def home():
    st.title("Moteur de recherche automobile")

    # Barre de recherche avec autocomplétion
    query = st.text_input("Rechercher un constructeur")

    if query:
        try:
            suggestions = manager.get_manufacturers_suggestions(query)
            if suggestions:
                selected_manufacturer = st.selectbox(
                    "Constructeurs :",
                    suggestions,
                    key="manufacturer_suggestions"
                )
                if selected_manufacturer:
                    # Lien vers la page de la marque 
                    if st.button("Voir la marque"):
                        # Mettez à jour l'état et redirigez via session_state
                        st.session_state.page = "Marques"
                        st.session_state.manufacturer = selected_manufacturer
                        st.rerun()
                    # Lien vers la page des modèles
                    st.write(f"**Modèles de {selected_manufacturer}:**")
                    if st.button("Voir les modèles"):
                        # Mettez à jour l'état et redirigez via session_state
                        st.session_state.page = "Modèles"
                        st.session_state.manufacturer = selected_manufacturer
                        st.rerun()
                        
        except Exception as e:
            st.error(f"Erreur lors de la recherche des suggestions: {str(e)}")

def models():
    st.title("Modèles automobiles")

    # Récupérer la marque sélectionnée depuis la session
    manufacturer = st.session_state.get("manufacturer", None)
    if manufacturer:
        try:
            cars = manager.get_car_models(manufacturer)

            # Affichage des données brutes pour débogage
            #st.write("### Données brutes retournées :")
            #st.json(cars)  # Affiche les données sous forme JSON

            if cars:
                st.write(f"### Modèles {manufacturer}")

                # Affichage des résultats en grille
                for car in cars:
                    with st.expander(car['name']['value']):
                        # Informations de base
                        if 'year' in car:
                            st.write(f"Released year : {car['year']['value']}")
                        if 'description' in car:
                            st.write(f"Description : {car['description']['value']}")
                        if 'image' in car:
                            st.image(car['image']['value'], use_container_width=True)
                        # Lien vers la page DBpedia
                        st.write(f"[Voir sur DBpedia]({car['car']['value']})")
            else:
                st.warning("Aucun résultat trouvé")
        except Exception as e:
            st.error(f"Erreur lors de la recherche des modèles: {str(e)}")
    else:
        st.warning("Aucune marque sélectionnée. Retournez à l'accueil pour rechercher une marque.")


def brands():
    st.title("Marques automobiles")

    manufacturer = st.session_state.get("manufacturer", None)
    if manufacturer:

        #[{"company":{"type":"uri","value":"http://dbpedia.org/resource/Cadillac"},"cleanName":{"type":"literal","value":"Cadillac"},"cleanFoundingDate":{"type":"literal","value":"1902-08-22"},"description":{"type":"literal","value":"The Cadillac Motor Car Division (/ˈkædɪlæk/) is a division of the American automobile manufacturer General Motors (GM) that designs and builds luxury vehicles. Its major markets are the United States, Canada, and China. Cadillac models are distributed in 34 additional markets worldwide. Cadillac automobiles are at the top of the luxury field within the United States. In 2019, Cadillac sold 390,458 vehicles worldwide, a record for the brand."},"website":{"type":"literal","value":"https://www.cadillac.com/%7Ccadillac.com"},"longDescription":{"type":"literal","value":"The Cadillac Motor Car Division (/ˈkædɪlæk/) is a division of the American automobile manufacturer General Motors (GM) that designs and builds luxury vehicles. Its major markets are the United States, Canada, and China. Cadillac models are distributed in 34 additional markets worldwide. Cadillac automobiles are at the top of the luxury field within the United States. In 2019, Cadillac sold 390,458 vehicles worldwide, a record for the brand. Cadillac is among the first automotive brands in the world, fourth in the United States only to Autocar Company (1897) and fellow GM marques Oldsmobile (1897) and Buick (1899). It was named after Antoine de la Mothe Cadillac (1658–1730), who founded Detroit, Michigan. The Cadillac crest is based on his coat of arms. By the time General Motors purchased the company in 1909, Cadillac had already established itself as one of America's premier luxury car makers. The complete interchangeability of its precision parts had allowed it to lay the foundation for the modern mass production of automobiles. It was at the forefront of technological advances, introducing full electrical systems, the clashless manual transmission and the steel roof. The brand developed three engines, with its V8 setting the standard for the American automotive industry. Cadillac had the first U.S. car to win the Royal Automobile Club of the United Kingdom's Dewar Trophy by successfully demonstrating the interchangeability of its component parts during a reliability test in 1908; this spawned the firm's slogan \"Standard of the World\". It won the trophy again in 1912 for incorporating electric starting and lighting in a production automobile."}}] exemple json
        st.write(f"### Marque sélectionnée : {manufacturer}")
        st.write("Retournez à la page d'accueil pour changer de marque.")
        brand = manager.get_brand_details(manufacturer)
        if brand:
            # Affichage des données brutes 
            st.markdown(f'## {brand[0]["cleanName"]["value"]}') 
            try :
                if (brand[0]['cleanFoundingDate']['value'] != ""):
                    st.write(f"**Date de fondation :** {brand[0]['cleanFoundingDate']['value']}")
                else :
                    st.write(f"**Date de fondation :** Non disponible")
            except:
                st.write(f"**Date de fondation :** Non disponibl")
            
            try:
                if (brand[0]['cleanFounder']['value'] != ""):
                    st.write(f"**Fondateur :** {brand[0]['cleanFounder']['value']}")
                else :
                    st.write(f"**Fondateur :** Non disponible")
            except:
                st.write(f"**Fondateur :** Non disponible")
            
            try:
                if (brand[0]['website']['value'] != ""):
                    st.write(f"**Site web :** {brand[0]['website']['value']}")
                else :
                    st.write(f"**Site web :** Non disponible")
            except:
                st.write(f"**Site web :** Non disponible")

            try:
                if (brand[0]['cleanLocation']['value'] != ""):
                    st.write(f"**Localisation :** {brand[0]['cleanLocation']['value']}")
                else :
                    st.write(f"**Localisation :** Non disponible")
            except:
                st.write(f"**Localisation :** Non disponible")
            
            try:
                if (brand[0]['description']['value'] != ""):
                    st.write(f"**Description :** {brand[0]['description']['value']}")
                else :
                    st.write(f"**Description :** Non disponible")
            except:
                st.write(f"**Description :** Non disponible")
            
            try:
                if (brand[0]['longDescription']['value'] != ""):
                    st.write(f"**Description longue :** {brand[0]['longDescription']['value']}")
                else :
                    st.write(f"**Description longue :** Non disponible")
            except:
                st.write(f"**Description longue :** Non disponible")
            
            try:
                if (brand[0]['cleanProduct']['value'] != ""):
                    st.write(f"**Type de Produit :** {brand[0]['cleanProduct']['value']}")
                else :
                    st.write(f"**Type de Produit :** Non disponible")
            except:
                st.write(f"**Type de Produit :** Non disponible")
            
            try:
                if (brand[0]['parentCompany']['value'] != ""):
                    parent_uri = brand[0]['parentCompany']['value']
                    parent_uri = parent_uri.split('/')[-1]
                    parent_name = manager.get_object_name(parent_uri)
                    if parent_name:
                        st.write(f"**Compagnie Parente :** {parent_name[0]['cleanName']['value']}")
                    else:    
                        st.write(f"**Compagnie Parente :** Non disponible")
                else :
                    st.write(f"**Compagnie Parente :** Non disponible")
            except:
                st.write(f"**Compagnie Parente :** Non disponible")

            try:
                if (brand[0]['childCompanies']['value'] != ""):
                    st.write(f"**Compagnies Filiales :** {brand[0]['childCompanies']['value']}")
                else :
                    st.write(f"**Compagnies Filiales :** Non disponible")
            except:
                st.write(f"**Compagnies Filiales :** Non disponible")

            st.write(f"**Models :**")
            # Lien vers la page des modèles
            if st.button("Voir les modèles"):
                # Mettez à jour l'état et redirigez via session_state
                st.session_state.page = "Modèles"
                st.session_state.manufacturer = manufacturer
                st.rerun()

            st.write("### Données brutes retournées :")
            st.json(brand)
        else:
            st.warning("Aucun résultat trouvé")
    else:
        st.warning("Aucune marque sélectionnée. Retournez à l'accueil pour rechercher une marque.")


# Manage navigation between pages
PAGES = {
    "Accueil": home,
    "Modèles": models,
    "Marques": brands,
}

def main():
    # Initialisation de l'état de navigation
    if "page" not in st.session_state:
        st.session_state.page = "Accueil"
    if "manufacturer" not in st.session_state:
        st.session_state.manufacturer = "Cadillac" #//!\ A modifier : mettre en None après tests

    # Navigation basée sur l'état actuel
    PAGES[st.session_state.page]()

    # Barre latérale pour changer de page
    st.sidebar.title("Navigation")
    if st.sidebar.button("Accueil"):
        st.session_state.page = "Accueil"
        st.rerun()
    if st.sidebar.button("Modèles"):
        st.session_state.page = "Modèles"
        st.rerun()
    if st.sidebar.button("Marques"):
        st.session_state.page = "Marques"
        st.rerun()

# Entrypoint
if __name__ == "__main__":
    main()
