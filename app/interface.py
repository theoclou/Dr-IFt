import streamlit as st
from SPARQLWrapper import SPARQLWrapper, JSON

def get_manufacturers_suggestions(query):
    """
    Récupère les suggestions de constructeurs basées sur la saisie
    """
    if not query:
        return []
        
    query = f"""
        PREFIX dbo: <http://dbpedia.org/ontology/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        SELECT DISTINCT ?name
        WHERE {{
            ?manufacturer rdf:type dbo:Company ;
                        dbo:industry dbr:Automotive_industry ;
                        rdfs:label ?name .
            FILTER(LANG(?name) = 'en')
            FILTER(REGEX(?name, "{query}", "i"))
        }}
        ORDER BY ?name
        LIMIT 10
    """
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    try:
        results = sparql.query().convert()
        return [result["name"]["value"] for result in results["results"]["bindings"]]
    except Exception as e:
        st.error(f"Erreur lors de la requête: {str(e)}")
        return []

def get_car_models(brand):
    """
    Récupère tous les modèles d'une marque spécifique
    """
    query = f"""
        PREFIX dbo: <http://dbpedia.org/ontology/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        SELECT DISTINCT ?car ?name ?year ?engine
        WHERE {{
            ?car rdf:type dbo:Automobile ;
                 rdfs:label ?name ;
                 dbo:manufacturer ?manufacturer .
            ?manufacturer rdfs:label ?manufacturerName .
            OPTIONAL {{ ?car dbp:productionStartYear ?year }}
            OPTIONAL {{ ?car dbp:engine ?engine }}
            FILTER(LANG(?name) = 'en')
            FILTER(LANG(?manufacturerName) = 'en')
            FILTER(REGEX(?manufacturerName, "{brand}", "i"))
        }}
        ORDER BY DESC(?year)
        LIMIT 100
    """
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    try:
        results = sparql.query().convert()
        return results["results"]["bindings"]
    except Exception as e:
        st.error(f"Erreur lors de la requête: {str(e)}")
        return []

def main():
    st.title("Moteur de recherche automobile")
    
    # Barre de recherche avec autocomplétion
    query = st.text_input("Rechercher un constructeur")
    
    # Afficher les suggestions pendant la saisie
    if query:
        suggestions = get_manufacturers_suggestions(query)
        if suggestions:
            selected_manufacturer = st.selectbox(
                "Constructeurs :",
                suggestions,
                key="manufacturer_suggestions"
            )
            if selected_manufacturer:
                query = selected_manufacturer

    # Affichage des résultats
    if query:
        cars = get_car_models(query)
        
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

if __name__ == "__main__":
    main()