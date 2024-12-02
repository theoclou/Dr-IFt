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
    
    def search_cars_by_brand(self, brand):
        return f"""
            {self.prefix}
            SELECT DISTINCT ?car ?name ?manufacturer ?year
            WHERE {{
                ?car rdf:type dbo:MeanOfTransportation ;
                     rdf:type dbo:Automobile ;
                     rdfs:label ?name ;
                     dbo:manufacturer ?manuf .
                ?manuf rdfs:label ?manufacturer .
                OPTIONAL {{ ?car dbp:productionStartYear ?year }}
                FILTER(LANG(?name) = 'en')
                FILTER(LANG(?manufacturer) = 'en')
                FILTER(REGEX(?manufacturer, "{brand}", "i"))
            }}
            LIMIT 20
        """
    
    def search_cars_by_year(self, year):
        return f"""
            {self.prefix}
            SELECT DISTINCT ?car ?name ?manufacturer ?year
            WHERE {{
                ?car rdf:type dbo:MeanOfTransportation ;
                     rdf:type dbo:Automobile ;
                     rdfs:label ?name ;
                     dbo:manufacturer ?manuf ;
                     dbp:productionStartYear ?year .
                ?manuf rdfs:label ?manufacturer .
                FILTER(LANG(?name) = 'en')
                FILTER(LANG(?manufacturer) = 'en')
                FILTER(?year = {year})
            }}
            LIMIT 20
        """
    
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
                ?car rdf:type dbo:MeanOfTransportation ;
                     rdf:type dbo:Automobile ;
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