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
            # Étape 1 : Charger les modèles principaux
            cars = manager.get_car_models_with_related(manufacturer)

            if cars:
                st.write(f"### Modèles {manufacturer}")

                # Affichage des voitures principales
                for car in cars:
                    with st.expander(car['name']['value']):
                        # Informations principales
                        st.write(f"**Released year:** {car.get('year', {}).get('value', 'Unknown')}")
                        st.write(f"**Types:** {car.get('typeNames', {}).get('value', 'No types available')}")
                        st.write(f"**Description:** {car.get('description', {}).get('value', 'No description available')}")
                        if 'image' in car:
                            st.image(car['image']['value'], use_container_width=True)
                        st.write(f"[Voir sur DBpedia]({car['car']['value']})")

                        # Modèles similaires
                        if car['relatedCars']:
                            st.write("**Modèles similaires :**")

                            # Création d'un menu déroulant pour les modèles similaires
                            related_car_names = ["Sélectionner un modèle"] + [related_car.get('name', {}).get('value', 'Nom inconnu') for related_car in car['relatedCars']]
                            selected_related_car = st.selectbox(
                                "Choisissez un modèle similaire",
                                related_car_names,
                                key=f"related_cars_{car['name']['value']}"  # Assurez-vous que la clé est unique par modèle
                            )

                            # Si l'utilisateur sélectionne un modèle, charger ses détails
                            if selected_related_car != "Sélectionner un modèle":
                                # Trouver l'URI du modèle sélectionné
                                selected_related_car_uri = None
                                for related_car in car['relatedCars']:
                                    if related_car.get('name', {}).get('value') == selected_related_car:
                                        selected_related_car_uri = related_car['car']['value']
                                        break

                                # Charger les détails uniquement si un modèle est sélectionné
                                if selected_related_car_uri:
                                    try:
                                        query_related_details = manager.queries.get_car_details(selected_related_car_uri)
                                        related_details = manager.execute_query(query_related_details)
                                        related_details = related_details[0] if related_details else None

                                        # Afficher les informations du modèle similaire
                                        if related_details:
                                            st.write(f"**Nom :** {related_details.get('name', {}).get('value', 'Nom non disponible')}")
                                            st.write(f"**Marque :** {related_details.get('manufacturer', {}).get('value', 'Inconnue')}")
                                            st.write(f"**Année de sortie :** {related_details.get('year', {}).get('value', 'Inconnue')}")
                                            st.write(f"**Description :** {related_details.get('description', {}).get('value', 'Aucune description disponible')}")
                                            if 'image' in related_details:
                                                st.image(related_details['image']['value'], use_container_width=True)
                                            st.write(f"[Voir sur DBpedia]({selected_related_car_uri})")
                                        else:
                                            st.warning("Aucun détail disponible pour ce modèle.")
                                    except Exception as e:
                                        st.error(f"Erreur lors de la récupération des détails : {str(e)}")
                        else:
                            st.warning("Aucun modèle similaire trouvé.")
            else:
                st.warning("Aucun résultat trouvé.")
        except Exception as e:
            st.error(f"Erreur lors de la recherche des modèles : {str(e)}")
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
