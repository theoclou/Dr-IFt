import streamlit as st
from car_search.sparql_manager import SparqlManager

from about import about
from home import home
from models import models
from stats import stats
from group import group_information
from brand import brands

# Initialize SPARQL manager (global for reuse)
manager = SparqlManager()

st.set_page_config(
    page_title="Moteur de recherche automobile",  # Titre de la page
    page_icon="🚗",  # Icône de la page
    layout="wide",  # Active la mise en page large
    initial_sidebar_state="expanded",  # État initial de la barre latérale (ouverte)
    menu_items={
        'Get Help': 'https://www.streamlit.io',
        'About': 'https://www.streamlit.io/about',
    }
)


# Manage navigation between pages
PAGES = {
    "Accueil": home,
    "Modèles": models,
    "About": about,
    "Statistiques": stats,
    "Groupes": group_information,
    "Marques": brands
}

# Main function
def main():
    # Initialisation de l'état de navigation
    if "page" not in st.session_state:
        st.session_state.page = "Accueil"
    if "manufacturer" not in st.session_state:
        st.session_state.manufacturer = None
    if "search_performed" not in st.session_state:
        st.session_state.search_performed = False

    # Navigation basée sur l'état actuel
    PAGES[st.session_state.page](manager)

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
    if st.sidebar.button("Statistiques"):
        st.session_state.page = "Statistiques"
        st.rerun()
    if st.sidebar.button("Groupes"):
        st.session_state.page = "Groupes"
        st.rerun()
    if st.sidebar.button("À propos"):
        st.session_state.page = "About"
        st.rerun()

# Entrypoint
if __name__ == "__main__":
    main()
