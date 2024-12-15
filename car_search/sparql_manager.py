from SPARQLWrapper import SPARQLWrapper, JSON
from car_search.sparql_queries import CarQueries, BrandQueries

class SparqlManager:
    def __init__(self, endpoint_url="http://dbpedia.org/sparql"):
        self.sparql = SPARQLWrapper(endpoint_url)
        self.sparql.setReturnFormat(JSON)
        self.queries = CarQueries()
        self.brand_queries = BrandQueries()
    
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
        suggestions = [result["name"]["value"] for result in results]
        
        # Filtrer les suggestions qui retournent des modèles
        valid_suggestions = []
        for manufacturer in suggestions:
            print(f"Vérification des modèles pour {manufacturer}")
            car_models = self.get_car_models(manufacturer.replace(" ", "_"))  # Adapter pour DBpedia
            if car_models:  # Si des modèles sont retournés
                valid_suggestions.append(manufacturer)
        
        return valid_suggestions
    
    def get_car_models(self, brand):
        query = self.queries.get_car_models(brand.replace(" ", "_"))  # Adapter pour DBpedia    
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
    
    def get_brand_details(self, brand_uri):
        query = self.brand_queries.get_brand_details_2(brand_uri)
        return self.execute_query(query)
    
    def get_object_name(self, object_uri):
        query = self.brand_queries.get_object_name(object_uri)
        results = self.execute_query(query)
        if results == []:
            return object_uri.replace("_", " ")
        print(results)
        return results