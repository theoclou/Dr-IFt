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
                        if 'year1' in car:
                            st.write(f"Année : {car['year1']['value']}")
                        if 'engine' in car:
                            st.write(f"Moteur : {car['engine']['value']}")
                        # Lien vers la page DBpedia
                        st.write(f"[Voir sur DBpedia]({car['car']['value']})")
            else:
                st.warning("Aucun résultat trouvé")
        except Exception as e:
            st.error(f"Erreur lors de la recherche des modèles: {str(e)}")
    else:
        st.warning("Aucune marque sélectionnée. Retournez à l'accueil pour rechercher une marque.")

# Manage navigation between pages
PAGES = {
    "Accueil": home,
    "Modèles": models
}

def main():
    # Initialisation de l'état de navigation
    if "page" not in st.session_state:
        st.session_state.page = "Accueil"
    if "manufacturer" not in st.session_state:
        st.session_state.manufacturer = None

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

# Entrypoint
if __name__ == "__main__":
    main()
