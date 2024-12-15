from SPARQLWrapper import SPARQLWrapper, JSON
from car_search.sparql_queries import CarQueries

class SparqlManager:
    def __init__(self, endpoint_url="http://dbpedia.org/sparql"):
        self.sparql = SPARQLWrapper(endpoint_url)
        self.sparql.setReturnFormat(JSON)
        self.queries = CarQueries()
    
    def execute_query(self, query):
        self.sparql.setQuery(query)
        try:
            results = self.sparql.query().convert()
            return results["results"]["bindings"]
        except Exception as e:
            print(f"Erreur lors de l'exécution de la requête: {str(e)}")
            return []
    
    def get_manufacturers_suggestions(self, query):
        if not query:
            return []
        query = self.queries.get_manufacturers_suggestions(query)
        results = self.execute_query(query)
        return [result["name"]["value"] for result in results]
    
    def get_car_models(self, brand):
        query = self.queries.get_car_models(brand)

        return self.execute_query(query)
    
    def get_car_models_with_related(self, brand):
        # Étape 1 : Obtenir les modèles principaux
        try:
            query_models = self.queries.get_car_models(brand)
            car_models = self.execute_query(query_models)  # Liste des modèles principaux
        except Exception as e:
            raise Exception(f"Erreur lors de la récupération des modèles pour {brand}: {e}")

        # Étape 2 : Obtenir les modèles similaires pour chaque voiture principale
        for car in car_models:
            car["relatedCars"] = []  # Initialiser la liste des modèles similaires

            if "typeNames" in car:
                # Récupérer la chaîne des types séparée par des virgules
                type_names_str = car.get('typeNames', {}).get('value', '')
                # Si la chaîne contient des types séparés par des virgules, les séparer en une liste
                type_names = type_names_str.split(',') if type_names_str else []

                # Par exemple, si vous voulez récupérer le premier type :
                if type_names:
                    first_type = type_names[0].strip()  

                try:
                    # Obtenir les modèles similaires pour le premier type
                    query_related = self.queries.get_car_related(first_type)
                    related_cars = self.execute_query(query_related)
                    car["relatedCars"] = related_cars  # Ajouter les modèles similaires
                except Exception as e:
                    print(f"Erreur lors de la récupération des modèles similaires pour le type {first_type}: {e}")
            else:
                print(f"Aucun type trouvé pour la voiture {car['name']['value']}")

        # Étape 3 : Retourner la liste des modèles avec les informations des modèles similaires
        return car_models

    
    def get_car_details(self, car_uri):
        query = self.queries.get_car_details(car_uri)
        return self.execute_query(query)
    
    def search_cars(self, brand=None, year=None, engine_type=None):
        if brand and not year:
            query = self.queries.search_cars_by_brand(brand)
        elif year and not brand:
            query = self.queries.search_cars_by_year(year)
        else:
            query = self.queries.search_cars_advanced(
                manufacturer=brand,
                min_year=year,
                engine_type=engine_type
            )
        return self.execute_query(query)
    
    def get_car_details(self, car_uri):
        query = self.queries.get_car_details(car_uri)
        return self.execute_query(query)