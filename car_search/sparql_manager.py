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
        suggestions = [result["name"]["value"] for result in results]
        
    
        
        return suggestions
    
    def get_car_models(self, brand):
        print("Brand:", brand)
        print("Formatted Brand:", brand.replace(" ", "_"))
        query = self.queries.get_car_models(brand.replace(" ", "_"))
        result = self.execute_query(query)
        return result
    
    def get_car_details(self, car_uri):
        query = self.queries.get_car_details(car_uri)
        return self.execute_query(query)