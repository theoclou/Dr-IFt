import streamlit as st
from car_search.sparql_manager import SparqlManager

def main():
    st.title("Moteur de recherche automobile")
    
    # Initialize SPARQL manager
    manager = SparqlManager()
    
    # Barre de recherche avec autocomplétion
    query = st.text_input("Rechercher un constructeur")
    
    # Afficher les suggestions pendant la saisie
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
                    query = selected_manufacturer
        except Exception as e:
            st.error(f"Erreur lors de la recherche des suggestions: {str(e)}")

    # Affichage des résultats
    if query:
        try:
            cars = manager.get_car_models(query)
            
            if cars:
                st.write(f"### Modèles {query}")
                
                # Affichage des résultats en grille
                for car in cars:
                    with st.expander(car['name']['value']):
                        # Informations de base
                        if 'year' in car:
                            st.write(f"Année : {car['year']['value']}")
                        if 'engine' in car:
                            st.write(f"Moteur : {car['engine']['value']}")
                        
                        # Lien vers la page DBpedia
                        st.write(f"[Voir sur DBpedia]({car['car']['value']})")
            else:
                st.warning("Aucun résultat trouvé")
        except Exception as e:
            st.error(f"Erreur lors de la recherche des modèles: {str(e)}")

if __name__ == "__main__":
    main()