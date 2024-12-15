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
           SELECT ?car ?name ?year ?description ?image
            WHERE {{
            ?car dbo:manufacturer dbr:{brand} ;
                a dbo:Automobile ;
                rdfs:label ?name ;
                dbo:abstract ?description ;
                dbo:thumbnail ?image .         

            OPTIONAL {{
                ?car dbo:productionStartYear ?year .
                FILTER (YEAR(?year) > 1800)
            }}

            FILTER (lang(?name) = "en" && lang(?description) = "en")
            }}
            ORDER BY DESC(?year)
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
    
class BrandQueries:
    def __init__(self):
        self.prefix = """
            PREFIX dbo: <http://dbpedia.org/ontology/>
            PREFIX dbp: <http://dbpedia.org/property/>
            PREFIX dbr: <http://dbpedia.org/resource/>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX yago: <http://dbpedia.org/class/yago/>
        """

    def get_brand_details(self, brand):
        return f"""
                {self.prefix}
                SELECT ?company (STR(MIN(?name)) AS ?cleanName) (STR(?foundingDate) AS ?cleanFoundingDate) 
                (STR(?comment) AS ?description) (STR(?site) AS ?website) 
                (STR(?netIncome) AS ?netIncome) (STR(?operatingIncome) AS ?operatingIncome) 
                (STR(?revenue) AS ?revenue) (STR(?longDescription) AS ?longDescription) 
                WHERE {{
                    VALUES ?company {{ dbr:{brand} }}
                    ?company foaf:name ?name .
                    OPTIONAL {{ ?company dbo:foundingDate ?foundingDate . }}
                    OPTIONAL {{ ?company rdfs:comment ?comment .
                                FILTER(lang(?comment) = "en") }}
                    OPTIONAL {{ ?company foaf:homepage ?site . }}
                    OPTIONAL {{ ?company dbo:netIncome ?netIncome . }}
                    OPTIONAL {{ ?company dbo:operatingIncome ?operatingIncome . }}
                    OPTIONAL {{ ?company dbo:revenue ?revenue . }}
                    OPTIONAL {{ ?company dbo:abstract ?longDescription .
                                FILTER(lang(?longDescription) = "en")}}
                    }}
                GROUP BY ?company ?foundingDate ?comment ?site ?netIncome ?operatingIncome ?revenue ?longDescription
                """
    
    def get_brand_details_2(self, brand):
        return f"""
                {self.prefix}
                SELECT 
                ?company 
                (STR(MIN(?name)) AS ?cleanName) 
                (STR(?foundingDate) AS ?cleanFoundingDate)
                (GROUP_CONCAT(DISTINCT REPLACE(STR(?founder), "^.*[/#]", ""); separator=", ") AS ?cleanFounder)
                (GROUP_CONCAT(DISTINCT COALESCE(STR(?locationName), STR(?location)); separator=", ") AS ?cleanLocation)
                (STR(?comment) AS ?description) 
                (STR(?site) AS ?website) 
                (GROUP_CONCAT(DISTINCT REPLACE(STR(?product), "^.*[/#]", ""); separator=", ") AS ?cleanProduct)
                ?parentCompany
                (COALESCE(GROUP_CONCAT(DISTINCT REPLACE(STR(?childCompany), "^.*[/#]", ""); separator=", "), "") AS ?childCompanies)
                (STR(?netIncome) AS ?netIncome) 
                (STR(?operatingIncome) AS ?operatingIncome) 
                (STR(?revenue) AS ?revenue) 
                (STR(?longDescription) AS ?longDescription) 
                WHERE {{
                VALUES ?company {{ dbr:{brand} }}
                ?company foaf:name ?name .
                OPTIONAL {{ ?company dbo:foundingDate ?foundingDate . }}
                OPTIONAL {{ ?company rdfs:comment ?comment .
                            FILTER(lang(?comment) = "en") }}
                OPTIONAL {{ ?company foaf:homepage ?site . }}
                OPTIONAL {{ ?company dbo:netIncome ?netIncome . }}
                OPTIONAL {{ ?company dbo:operatingIncome ?operatingIncome . }}
                OPTIONAL {{ ?company dbo:revenue ?revenue . }}
                OPTIONAL {{ ?company dbo:abstract ?longDescription .
                    FILTER(lang(?longDescription) = "en")}}
                OPTIONAL {{ ?company dbo:foundedBy ?founder . }}
                OPTIONAL {{ ?company dbp:location ?location .
                            OPTIONAL {{ ?location foaf:name ?locationName . }}
                }}
                OPTIONAL {{ ?company dbo:product ?product . }}
                OPTIONAL {{ ?company dbo:parentCompany ?parentCompany . }}
                OPTIONAL {{
                    SELECT ?company (GROUP_CONCAT(DISTINCT REPLACE(STR(?childCompany), "^.*[/#]", ""); separator=", ") AS ?childCompany)
                    WHERE {{
                    ?childCompany dbo:parentCompany ?company .
                    }}
                    GROUP BY ?company
                }}
                }}
                GROUP BY ?company ?foundingDate ?comment ?site ?netIncome ?operatingIncome ?revenue ?longDescription ?parentCompany
                """

    
    def get_object_name(self, object):
        return f"""
        {self.prefix}
        SELECT (STR((?name)) AS ?cleanName)
        WHERE {{
            <http://dbpedia.org/resource/{object}> foaf:name ?name .
        }}
    """
