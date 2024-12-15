from SPARQLWrapper import SPARQLWrapper, JSON
from car_search.sparql_queries import CarQueries
import re

def strip_dbpedia_prefix(value):
    """
    Removes the 'http://dbpedia.org/resource/' prefix from a given string if it exists.
    
    Args:
        value (str): The string to process.
        
    Returns:
        str: The processed string without the prefix.
    """
    prefix = "http://dbpedia.org/resource/"
    if isinstance(value, str) and value.startswith(prefix):
        return value[len(prefix):]
    return value

class SparqlManager:
    def __init__(self, endpoint_url="http://dbpedia.org/sparql"):
        self.sparql = SPARQLWrapper(endpoint_url)
        self.sparql.setReturnFormat(JSON)
        self.queries = CarQueries()

    def sanitize_input(self, input_str):
        """
        Sanitize input to prevent SPARQL injection.
        Removes characters that are not alphanumeric, spaces, underscores, or hyphens.
        """
        return input_str
# transform the resukts of the query into a list of dictionaries
    def execute_query(self, query):
        self.sparql.setQuery(query)
        try:
            results = self.sparql.query().convert()
            return results["results"]["bindings"]
        except Exception as e:
            print(f"Erreur lors de l'exécution de la requête: {str(e)}")
            return []

# all the methods below are used to execute the queries defined in the sparql_queries.py file   
    def get_manufacturers_suggestions(self, query):
        if not query:
            return []
        query = self.queries.get_manufacturers_suggestions(query.replace(" ", "_"))
        results = self.execute_query(query)
        suggestions = [result["name"]["value"] for result in results]
        return suggestions
    
    def get_car_models(self, brand):
        query = self.queries.get_car_models(brand.replace(" ", "_"))
        result = self.execute_query(query)
        print(result)
        return result
    
    def get_car_details(self, car_uri):
        query = self.queries.get_car_details(car_uri.replace(" ", "_"))
        return self.execute_query(query)
    
    def get_total_manufacturers(self):
        query = self.queries.get_total_manufacturers()
        result = self.execute_query(query)
        return result[0]["count"]["value"]
        
    def get_total_cars(self):
        query = self.queries.get_total_cars()
        result = self.execute_query(query)
        return result[0]["count"]["value"]
    
    def get_top_manufacturers(self):
        query = self.queries.get_top_manufacturers()
        results = self.execute_query(query)
        return results
    
    def get_top_engine_types(self):
        query = self.queries.get_top_engine_types()
        results = self.execute_query(query)
        return results
    
    def get_top_fuel_types(self):
        query = self.queries.get_fuel_types()
        results = self.execute_query(query)
        return results
    
    def get_car_by_production_year_from1950_to2020(self):
        query = self.queries.get_car_by_production_year()
        results = self.execute_query(query)
        return results
    
    def get_manufacturers_by_country(self):
        query = self.queries.get_manufacturers_by_country()
        results = self.execute_query(query)
        return results
    
    def get_best_carrosserie(self):
        query = self.queries.get_best_carrosserie()
        results = self.execute_query(query)
        return results
    
    def get_class_car(self):
        query = self.queries.get_class_car()
        results = self.execute_query(query)
        return results
    
    def get_company_turnover(self):
        query = self.queries.get_company_turnover()
        results = self.execute_query(query)
        return results


    ##########################################################
    #################### Group functions #####################
    ##########################################################
        
    def execute_query(self, query):
        self.sparql.setQuery(query)
        try:
            results = self.sparql.query().convert()
            return results["results"]["bindings"]
        except Exception as e:
            logging.error(f"Error executing query: {str(e)}")
            return []

    def get_parent_group_of_car(self, brand):
        if not brand:
            return []
        sanitized_brand = self.sanitize_input(brand).replace(" ", "_")
        query = self.queries.search_parent_group_of_car(sanitized_brand)
        results = self.execute_query(query)
        processed_results = [{
            "name": strip_dbpedia_prefix(result["name"]["value"]),
            "manufacturer": strip_dbpedia_prefix(result.get("manufacturer", {}).get("value", "N/A")),
            "parentCompany": strip_dbpedia_prefix(result.get("parentCompany", {}).get("value", "N/A"))
        } for result in results]
        return processed_results

    def get_parent_group_of_manufacturer(self, manufacturer):
        if not manufacturer:
            return []
        sanitized_manufacturer = self.sanitize_input(manufacturer).replace(" ", "_")
        query = self.queries.search_parent_group_of_manufacturer(sanitized_manufacturer)
        results = self.execute_query(query)
        processed_results = [{
            "manufacturer": strip_dbpedia_prefix(result.get("manufacturer", {}).get("value", "N/A")),
            "parentCompany": strip_dbpedia_prefix(result.get("parentCompany", {}).get("value", "N/A"))
        } for result in results]
        return processed_results

    def get_country_of_group(self, group):
        if not group:
            return []
        sanitized_group = self.sanitize_input(group).replace(" ", "_")
        query = self.queries.search_country_of_group(sanitized_group)
        results = self.execute_query(query)
        processed_results = [{
            "parentCompany": strip_dbpedia_prefix(result.get("parentCompany", {}).get("value", "N/A")),
            "Country": strip_dbpedia_prefix(result.get("Country", {}).get("value", "N/A"))
        } for result in results]
        return processed_results

    def get_founding_date_of_group(self, group):
        if not group:
            return []
        sanitized_group = self.sanitize_input(group).replace(" ", "_")
        query = self.queries.search_founding_date(sanitized_group)
        results = self.execute_query(query)
        processed_results = [{
            "parentCompany": strip_dbpedia_prefix(result.get("parentCompany", {}).get("value", "N/A")),
            "foundingDate": strip_dbpedia_prefix(result.get("foundingDate", {}).get("value", "N/A"))
        } for result in results]
        return processed_results

    def get_founder_of_group(self, group):
        if not group:
            return []
        sanitized_group = self.sanitize_input(group).replace(" ", "_")
        query = self.queries.search_founder(sanitized_group)
        results = self.execute_query(query)
        processed_results = [{
            "parentCompany": strip_dbpedia_prefix(result.get("parentCompany", {}).get("value", "N/A")),
            "founder": strip_dbpedia_prefix(result.get("founder", {}).get("value", "N/A"))
        } for result in results]
        return processed_results

    def get_list_of_brands_of_group(self, group):
        if not group:
            return []
        sanitized_group = self.sanitize_input(group).replace(" ", "_")
        query = self.queries.search_list_of_brands(sanitized_group)
        results = self.execute_query(query)
        processed_results = [{
            "parentCompany": strip_dbpedia_prefix(result.get("parentCompany", {}).get("value", "N/A")),
            # "founder": strip_dbpedia_prefix(result.get("founder", {}).get("value", "N/A")),
            "brand": strip_dbpedia_prefix(result.get("brands", {}).get("value", "N/A"))
        } for result in results]
        return processed_results

    def get_revenue_of_group(self, group):
        if not group:
            return []
        sanitized_group = self.sanitize_input(group).replace(" ", "_")
        query = self.queries.search_revenue(sanitized_group)
        results = self.execute_query(query)
        processed_results = [{
            "parentCompany": strip_dbpedia_prefix(result.get("parentCompany", {}).get("value", "N/A")),
            "founder": strip_dbpedia_prefix(result.get("founder", {}).get("value", "N/A")),
            "revenue": result.get("revenue", {}).get("value", "N/A"),
            "revenueCurrency": strip_dbpedia_prefix(result.get("revenueCurrency", {}).get("value", "N/A"))
        } for result in results]
        return processed_results

    def get_investors_of_group(self, group):
        if not group:
            return []
        sanitized_group = self.sanitize_input(group).replace(" ", "_")
        query = self.queries.search_investors_of_group(sanitized_group)
        results = self.execute_query(query)
        processed_results = [{
            "parentCompany": strip_dbpedia_prefix(result.get("parentCompany", {}).get("value", "N/A")),
            "owner": strip_dbpedia_prefix(result.get("owner", {}).get("value", "N/A"))
        } for result in results]
        return processed_results

