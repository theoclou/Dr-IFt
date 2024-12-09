import streamlit as st
from car_search.sparql_manager import SparqlManager

# Initialize SPARQL manager (global for reuse)
manager = SparqlManager()

st.set_page_config(
    page_title="Moteur de recherche automobile",  # Titre de la page
    page_icon="🚗",  # Icône de la page
    #layout="wide",  # Utilise la mise en page large pour maximiser l'espace
    initial_sidebar_state="expanded",  # État initial de la barre latérale (ouverte)
    menu_items={
        'Get Help': 'https://www.streamlit.io',
        'About': 'https://www.streamlit.io/about',
    }
)

# Function to get suggestions dynamically
def get_live_suggestions(query):
    if query:
        return manager.get_manufacturers_suggestions(query)
    return []

# Define page functions
def home():
    # Centrer l'image et la rendre plus petite
    st.markdown(
        """
        <div style="display: flex; justify-content: center;">
            <img src="https://png.pngtree.com/png-vector/20220617/ourmid/pngtree-auto-car-logo-template-png-image_5181062.png" width="400">
        </div>
        """,
        unsafe_allow_html=True
    )
    st.title("Bienvenue sur AutoSearch")

    # Contenu de la page
    st.write("Cette application vous permet de rechercher des constructeurs automobiles et leurs modèles.")

    # Barre de recherche avec autocomplétion
    query = st.text_input(
        "Rechercher un constructeur",
        key="query",
        placeholder="Entrez un constructeur...",
        label_visibility="collapsed",  # Hide the label for a cleaner UI
        help="Tapez un constructeur pour voir des suggestions.",
        autocomplete="off",  # Disable browser autocomplete to prevent interference
    )

    if query:
        try:
            # Get live suggestions based on the query
            suggestions = get_live_suggestions(query)
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
