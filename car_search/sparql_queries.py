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
    
    def get_manufacturers_suggestions(self, query):
        return f"""
            {self.prefix}
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
    
    def get_car_models(self, brand):
        return f"""
            {self.prefix}
            SELECT DISTINCT ?car ?name ?year (GROUP_CONCAT(DISTINCT ?typeName ;
            separator=",") as ?typeNames) ?description ?image
            WHERE {{
                ?car dbo:manufacturer dbr:{brand} ;
                    a dbo:Automobile ;
                    rdfs:label ?name ;
                    dbo:abstract ?description ;
                    dbo:thumbnail ?image ;
                    dbo:class ?type .

                ?type rdfs:label ?typeName .

                OPTIONAL {{
                    ?car dbo:productionStartYear ?year .
                    FILTER (YEAR(?year) > 1800)
                }}

                FILTER (lang(?name) = "en" && lang(?description) = "en" &&
            lang(?typeName) = "en")
            }}
            GROUP BY ?car ?name ?year ?description ?image
            ORDER BY DESC(?year)
            LIMIT 20
        """
    
    def get_car_related(self, typeRelated):
        return f"""
            {self.prefix}
            SELECT DISTINCT ?car ?name
            WHERE {{
                ?car a dbo:Automobile ;
                     dbo:class ?type;
                     rdfs:label ?name .
                ?type rdfs:label ?typeName .
                FILTER(lang(?typeName) = "en" && str(?typeName) = "{typeRelated}" && lang(?name) = "en")
            }}
            LIMIT 2
        """

    def get_car_details(self, car_uri):
        return f"""
            {self.prefix}
           SELECT DISTINCT ?name ?brand ?year ?description ?image
            WHERE {{
            <{car_uri}> rdfs:label ?name ;
                dbo:abstract ?description ;
                dbo:thumbnail ?image .

            OPTIONAL {{
                <{car_uri}> dbo:manufacturer ?brand .
            }}

            OPTIONAL {{
                <{car_uri}> dbo:productionStartYear ?year .
                FILTER (YEAR(?year) > 1800)
            }}

            FILTER (lang(?name) = "en" && lang(?description) = "en")
            }}
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