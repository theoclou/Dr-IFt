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
           SELECT ?car ?name ?year1 ?year2
            WHERE {{
            ?car dbo:manufacturer dbr:{brand} ;
                a dbo:Automobile ;
                rdfs:label ?name .

            OPTIONAL {{
                ?car dbo:productionStartYear ?year .
                FILTER (YEAR(?year) > 1800)
            }}

            OPTIONAL {{
                ?car dbp:production ?year2 .
                FILTER (xsd:integer(?year2) > 1800)
            }}

            BIND(IF(BOUND(?year), YEAR(?year), "") AS ?year1)

            FILTER (lang(?name) = "fr")
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
        
    def search_parent_group_of_car(self,brand):
        return f"""
            {self.prefix}
        SELECT DISTINCT ?car ?name ?manufacturer ?parentCompany 
        WHERE {{
            ?car rdf:type dbo:MeanOfTransportation ;
            rdf:type dbo:Automobile ;
            rdfs:label ?name ;
            dbo:manufacturer ?manufacturer .
            OPTIONAL {{ ?manufacturer dbo:parentCompany ?parentCompany . }}
            
            FILTER(LANG(?name) = 'en')
            FILTER NOT EXISTS {{
                ?parentCompany dbo:parentCompany ?grandParentCompany . 
            }}
            FILTER(REGEX(STR(?name), '{brand}', 'i'))
            }}
            LIMIT 1
            
        """ 
        
    def search_parent_group_of_manufacturer(self,manufacturer):
        return f"""
            {self.prefix}
        SELECT DISTINCT ?manufacturer ?parentCompany 
        WHERE {{
            ?car rdf:type dbo:MeanOfTransportation ;
            rdf:type dbo:Automobile ;
            dbo:manufacturer ?manufacturer .
            OPTIONAL {{ ?manufacturer dbo:parentCompany ?parentCompany . }}
            FILTER NOT EXISTS {{
                ?parentCompany dbo:parentCompany ?grandParentCompany . 
            }}
            FILTER(REGEX(STR(?manufacturer), '{manufacturer}', 'i'))
            }}
            LIMIT 20
        """ 
    def search_country_of_group(self , group):
        return f"""
            {self.prefix}
        SELECT DISTINCT ?parentCompany ?Country 
        WHERE {{
            ?car rdf:type dbo:MeanOfTransportation ;
            rdf:type dbo:Automobile ;
            dbo:manufacturer ?manufacturer .
            OPTIONAL {{ ?manufacturer dbo:parentCompany ?parentCompany . }}
            OPTIONAL {{ ?parentCompany dbp:locationCountry ?Country . }}
            FILTER NOT EXISTS {{
                ?parentCompany dbo:parentCompany ?grandParentCompany . 
            }}
            FILTER(REGEX(STR(?parentCompany), '{group}', 'i'))
            }}
            LIMIT 20
        """ 
    
    def search_founding_date(self ,group):
         return f"""
            {self.prefix}
        SELECT DISTINCT ?parentCompany ?foundingdate 
        WHERE {{
            ?car rdf:type dbo:MeanOfTransportation ;
            rdf:type dbo:Automobile ;
            dbo:manufacturer ?manufacturer .
            OPTIONAL {{ ?manufacturer dbo:parentCompany ?parentCompany . }}
            FILTER NOT EXISTS {{
                ?parentCompany dbo:parentCompany ?grandParentCompany . 
            }}
            OPTIONAL {{ ?parentCompany dbo:foundingDate ?foundingdate . }}
            FILTER(REGEX(STR(?parentCompany), '{group}', 'i'))
            }}
            LIMIT 20
        """ 
    def search_founder(self , group):
        return f"""
            {self.prefix}
        SELECT DISTINCT ?parentCompany ?founder
        WHERE {{
            ?car rdf:type dbo:MeanOfTransportation ;
            rdf:type dbo:Automobile ;
            dbo:manufacturer ?manufacturer .
            OPTIONAL {{ ?manufacturer dbo:parentCompany ?parentCompany . }}
            FILTER NOT EXISTS {{
                ?parentCompany dbo:parentCompany ?grandParentCompany . 
            }}
            OPTIONAL {{ ?parentCompany dbo:foundedBy ?founder . }}
            FILTER(REGEX(STR(?parentCompany), '{group}', 'i'))
            }}
            LIMIT 20
        """ 
    def search_list_of_brands(self,group):
        return f"""
            {self.prefix}
        SELECT DISTINCT ?parentCompany ?founder ?brands
        WHERE {{
            ?car rdf:type dbo:MeanOfTransportation ;
            rdf:type dbo:Automobile ;
            dbo:manufacturer ?manufacturer .
            OPTIONAL {{ ?manufacturer dbo:parentCompany ?parentCompany . }}
            FILTER NOT EXISTS {{
                ?parentCompany dbo:parentCompany ?grandParentCompany . 
            }}
            OPTIONAL {{ ?parentCompany dbo:foundedBy ?founder . }}
            OPTIONAL {{ ?parentCompany dbp:brands ?brands . }}
            FILTER(REGEX(STR(?parentCompany), '{group}', 'i'))
            }}
            LIMIT 20
        """
        
    def search_revenue(self,group):
        return f"""
            {self.prefix}
        SELECT DISTINCT ?parentCompany ?founder ?revenue ?revenueCurrency
        WHERE {{
            ?car rdf:type dbo:MeanOfTransportation ;
            rdf:type dbo:Automobile ;
            dbo:manufacturer ?manufacturer .
            OPTIONAL {{ ?manufacturer dbo:parentCompany ?parentCompany . }}
            FILTER NOT EXISTS {{
                ?parentCompany dbo:parentCompany ?grandParentCompany . 
            }}
            OPTIONAL {{ ?parentCompany dbo:foundedBy ?founder . }}
            OPTIONAL {{ ?parentCompany dbo:revenue ?revenue . }}
            OPTIONAL {{ ?parentCompany dbo:revenueCurrency ?revenueCurrency . }}

            FILTER(REGEX(STR(?parentCompany), '{group}', 'i'))
            }}
            LIMIT 20
        """
    