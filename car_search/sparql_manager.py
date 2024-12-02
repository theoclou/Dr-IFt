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