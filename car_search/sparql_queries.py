import requests

class CarQueries:
    def __init__(self):
        self.prefix = """
            PREFIX dbo: <http://dbpedia.org/ontology/>
            PREFIX dbp: <http://dbpedia.org/property/>
            PREFIX dbr: <http://dbpedia.org/resource/>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX yago: <http://dbpedia.org/class/yago/>
        """

#Page d'accueil + modèle de voiture

    def get_manufacturers_suggestions(self, query):
        return f"""
            {self.prefix}
            SELECT DISTINCT ?name
            WHERE {{
                ?manufacturer rdf:type dbo:Company ;
                            dbo:industry dbr:Automotive_industry ;
                            rdfs:label ?name .
                
                FILTER(LANG(?name) = 'en')
                FILTER(REGEX(?name, "^{query}", "i"))
                
                # Vérification que le constructeur a au moins un modèle
                FILTER EXISTS {{
                    ?car dbo:manufacturer ?manufacturer ;
                        a dbo:Automobile .
                }}
            }}
            ORDER BY ?name
            LIMIT 10
        """
    

    def get_car_models(self, brand):
        query = f"""
            {self.prefix}
            SELECT ?car ?name ?description ?image ?year
            WHERE {{
                ?car dbo:manufacturer <http://dbpedia.org/resource/{brand}> ;
                    a dbo:Automobile ;
                    rdfs:label ?name ;
                    dbo:abstract ?description .

                OPTIONAL {{
                    ?car dbo:thumbnail ?image .
                }}

                OPTIONAL {{
                    ?car dbo:productionStartYear ?year .
                    FILTER (?year > 1800)
                }}

                FILTER (lang(?name) = "en" && lang(?description) = "en")
            }}
            ORDER BY DESC(?year)
        """

        """headers = {
            'Accept': 'application/sparql-results+json',  # Correct Accept header for DBpedia JSON response
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'  # Ajoute cet en-tête

        }

        response = requests.get(sparql_endpoint, params={'query': query, 'format': 'json'}, headers=headers)"""

        return query


    
    def get_car_details(self, car_uri):
        return f"""
            {self.prefix}
            SELECT DISTINCT ?propertyLabel ?value
            WHERE {{
                <{car_uri}> ?property ?value .
                ?property rdfs:label ?propertyLabel .
                FILTER(LANG(?propertyLabel) = 'en')
                FILTER(
                    isLiteral(?value) && 
                    (LANG(?value) = 'en' || LANG(?value) = '')
                )
            }}
            LIMIT 30
        """
    
# Page statistiques

    def get_total_manufacturers(self):
        return f"""
            {self.prefix}
            SELECT (COUNT(DISTINCT ?manufacturer) AS ?count)
            WHERE {{
                ?manufacturer rdf:type dbo:Company ;
                            dbo:industry dbr:Automotive_industry ;
                            rdfs:label ?name .
                
                FILTER(LANG(?name) = 'en')
                
                # Vérification que le constructeur a au moins un modèle
                FILTER EXISTS {{
                    ?car dbo:manufacturer ?manufacturer ;
                        a dbo:Automobile .
                }}
            }}
        """

    def get_total_cars(self):
        return f"""
            {self.prefix}
            SELECT (COUNT(DISTINCT ?car) AS ?count)
            WHERE {{
                     rdf:type dbo:Automobile .
            }}
        """
    
    def get_top_manufacturers(self):
        return f"""
            {self.prefix}
            SELECT ?manufacturerName (COUNT(?car) AS ?count)
            WHERE {{
                ?car rdf:type dbo:Automobile ;
                     dbo:manufacturer ?manufacturer .
                ?manufacturer rdfs:label ?manufacturerName .
                FILTER(LANG(?manufacturerName) = 'en')
            }}
            GROUP BY ?manufacturerName
            ORDER BY DESC(?count)
            LIMIT 10
        """
    
    def get_manufacturers_by_country(self):
        return f"""
            {self.prefix}
            SELECT ?countryName (COUNT(?manufacturer) AS ?count)
            WHERE {{
                ?manufacturer rdf:type dbo:Company ;
                            dbo:industry dbr:Automotive_industry ;
                            rdfs:label ?manufacturerName ;
                            dbo:country ?country .
                ?country rdfs:label ?countryName .
                
                FILTER(LANG(?manufacturerName) = 'en')
                FILTER(LANG(?countryName) = 'en')
            }}
            GROUP BY ?countryName
            ORDER BY DESC(?count)
            LIMIT 10
        """


































    
    def search_cars_advanced(self, manufacturer=None, min_year=None, max_year=None):
        filters = []
        if manufacturer:
            filters.append(f'FILTER(REGEX(?manufacturerName, "{manufacturer}", "i"))')
        if min_year:
            filters.append(f'FILTER(?year >= {min_year})')
        if max_year:
            filters.append(f'FILTER(?year <= {max_year})')
            
        filters_str = "\n".join(filters)
        
        return f"""
            {self.prefix}
            SELECT DISTINCT ?car ?name ?manufacturerName ?year
            WHERE {{
                ?car rdf:type dbo:Automobile ;
                     rdfs:label ?name ;
                     dbo:manufacturer ?manufacturer .
                ?manufacturer rdfs:label ?manufacturerName .
                OPTIONAL {{ ?car dbp:productionStartYear ?year }}
                FILTER(LANG(?name) = 'en')
                FILTER(LANG(?manufacturerName) = 'en')
                {filters_str}
            }}
            ORDER BY ?year
            LIMIT 20
        """