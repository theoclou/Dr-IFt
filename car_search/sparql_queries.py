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
# ---------------------------------------------------------------    
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
            SELECT DISTINCT ?car ?name ?year ?typeNames ?description ?image
            WHERE {{
                ?car dbo:manufacturer <http://dbpedia.org/resource/{brand}> ;
                    a dbo:Automobile ;
                    rdfs:label ?name .
                
                OPTIONAL {{ 
                    ?car dbo:abstract ?description 
                    FILTER(lang(?description) = "en")
                }}
                
                OPTIONAL {{ 
                    ?car dbo:thumbnail ?image 
                }}
                
                OPTIONAL {{
                    ?car dbo:productionStartYear ?year .
                    FILTER (YEAR(?year) > 1940)
                }}
                
                OPTIONAL {{
                    SELECT ?car (GROUP_CONCAT(DISTINCT ?typeName ;
                    separator=",") as ?typeNames)
                    WHERE {{
                        ?car dbo:class ?type .
                        ?type rdfs:label ?typeName .
                        FILTER(lang(?typeName) = "en")
                    }}
                    GROUP BY ?car
                }}
                
                FILTER(lang(?name) = "en")
            }}
            ORDER BY DESC(?year)
            LIMIT 30
        """
        return query


    def get_car_related(self, typeRelated):
        return f"""
            {self.prefix}
            SELECT DISTINCT ?car ?name ?year ?description ?image
            WHERE {{
                ?car a dbo:Automobile ;
                    dbo:class ?type ;
                    rdfs:label ?name .
                
                ?type rdfs:label ?typeName .
                
                OPTIONAL {{ 
                    ?car dbo:abstract ?description 
                    FILTER(lang(?description) = "en")
                }}
                
                OPTIONAL {{ 
                    ?car dbo:thumbnail ?image 
                }}
                
                OPTIONAL {{
                    ?car dbo:productionStartYear ?year .
                    FILTER (YEAR(?year) > 1800)
                }}
                
                FILTER(lang(?typeName) = "en" && str(?typeName) = "{typeRelated}" && lang(?name) = "en")
            }}
            LIMIT 4
        """

    def get_car_details(self, car_uri):
        return f"""
            {self.prefix}
            SELECT DISTINCT ?name ?manufacturerName ?year ?description ?image
            WHERE {{
                dbr:{car_uri} rdfs:label ?name ;
                            a dbo:Automobile .
                
                OPTIONAL {{ 
                    dbr:{car_uri} dbo:abstract ?description 
                    FILTER(lang(?description) = "en")
                }}
                
                OPTIONAL {{ 
                    dbr:{car_uri} dbo:thumbnail ?image 
                }}
                
                OPTIONAL {{
                    dbr:{car_uri} dbo:productionStartYear ?year .
                    FILTER (YEAR(?year) > 1800)
                }}
                
                OPTIONAL {{
                    dbr:{car_uri} dbo:manufacturer ?manufacturer .
                    ?manufacturer rdfs:label ?manufacturerName .
                    FILTER(lang(?manufacturerName) = "en")
                }}
                
                FILTER(lang(?name) = "en")
            }}
        """
    def get_car_models_with_broad_query(self, brand):
        return f"""
        {self.prefix}
        SELECT DISTINCT ?car ?name ?year ?description ?image
        WHERE {{
            ?car dbo:manufacturer <http://dbpedia.org/resource/{brand}> ;
                a dbo:Automobile ;
                rdfs:label ?name .
            
            OPTIONAL {{ 
                ?car dbo:abstract ?description 
                FILTER(lang(?description) = "en")
            }}
            
            OPTIONAL {{ 
                ?car dbo:thumbnail ?image 
            }}
            
            OPTIONAL {{
                ?car dbo:productionStartYear ?year .
                FILTER (YEAR(?year) > 1800)
            }}
            
            FILTER(lang(?name) = "en")
        }}
        ORDER BY DESC(?year)
        LIMIT 50
        """

    def get_related_cars_by_class(self, car_uri):
        return f"""
        {self.prefix}
        SELECT DISTINCT ?relatedCar ?name ?year ?description ?image
        WHERE {{
            <{car_uri}> dbo:class ?carClass .
            ?relatedCar a dbo:Automobile ;
                        dbo:class ?carClass ;
                        rdfs:label ?name .
            
            OPTIONAL {{ 
                ?relatedCar dbo:abstract ?description 
                FILTER(lang(?description) = "en")
            }}
            
            OPTIONAL {{ 
                ?relatedCar dbo:thumbnail ?image 
            }}
            
            OPTIONAL {{
                ?relatedCar dbo:productionStartYear ?year .
                FILTER (YEAR(?year) > 1800)
            }}
            
            FILTER(?relatedCar != <{car_uri}>)
            FILTER(lang(?name) = "en")
        }}
        LIMIT 4
        """

    def get_general_related_cars(self, car_uri):
        return f"""
        {self.prefix}
        SELECT DISTINCT ?car ?name
        WHERE {{
            ?car a dbo:Automobile ;
                rdfs:label ?name .
            FILTER(LANG(?name) = "en")
            FILTER(?car != <{car_uri}>)
        }}
        LIMIT 5
        """
# ---------------------------------------------------------------    
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
                    ?car rdf:type dbo:Automobile .
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
    
    def get_top_engine_types(self):
        return f"""
            {self.prefix}
            SELECT ?engineType (COUNT(?car) AS ?count)
            WHERE {{
                ?car rdf:type dbo:Automobile ;
                     dbo:engine ?engine .
                ?engine rdfs:label ?engineType .
                FILTER(LANG(?engineType) = 'en')
            }}
            GROUP BY ?engineType
            ORDER BY DESC(?count)
            LIMIT 5
        """
    
    def get_car_by_production_year(self):
        return f"""
            {self.prefix}
            SELECT ?yearnum (COUNT(?car) AS ?count)
            WHERE {{
                ?car rdf:type dbo:Automobile ;
                    dbo:productionStartYear ?year .
            
                BIND(year(?year) AS ?yearnum)
                FILTER(?yearnum >= 1950 and ?yearnum <= 2022)
            }}
            GROUP BY ?yearnum
            ORDER BY ?yearnum
        """
    
    def get_manufacturers_by_country(self):
        return f"""
            {self.prefix}
            SELECT ?country ?count
            WHERE {{
            {{
                SELECT ?country (COUNT(DISTINCT ?manufacturer) AS ?count)
                WHERE {{
                ?manufacturer rdf:type dbo:Company ;
                                dbo:industry dbr:Automotive_industry ;
                                dbp:locationCountry ?country.
                FILTER (lang(?country) = "en")
                }}
                GROUP BY ?country
                ORDER BY DESC(?count)
                LIMIT 10
            }}
            UNION
            {{
                SELECT ("Others" AS ?country) (SUM(?count) AS ?count)
                WHERE {{
                {{
                    SELECT ?country (COUNT(DISTINCT ?manufacturer) AS ?count)
                    WHERE {{
                    ?manufacturer rdf:type dbo:Company ;
                                    dbo:industry dbr:Automotive_industry ;
                                    dbp:locationCountry ?country.
                    FILTER (lang(?country) = "en")
                    }}
                    GROUP BY ?country
                    ORDER BY DESC(?count)
                    OFFSET 10
                }}
                }}
            }}
            }}
            ORDER BY DESC(?count)

        """
    
    def get_best_carrosserie(self):
        return f"""
            {self.prefix}
            SELECT ?name (COUNT(?car) AS ?count)
            WHERE {{
                ?car rdf:type dbo:Automobile ;
                    dbo:bodyStyle ?bodyStyle .
                ?bodyStyle rdfs:label ?name .
                FILTER(LANG(?name) = "en")
            }}
            GROUP BY ?name
            ORDER BY DESC(?count)
            LIMIT 5
        """

    def get_class_car(self):
        return f"""
            {self.prefix}
            SELECT ?carClass (COUNT(?car) AS ?count)
            WHERE {{
                ?car rdf:type dbo:Automobile ;
                    dbo:class ?carclass .
                ?carclass rdfs:label ?carClass .
                FILTER(LANG(?carClass) = "en")
            }}
            GROUP BY ?carClass
            ORDER BY DESC(?count)
            LIMIT 5
        """
    
    def get_company_turnover(self):
        return f"""
            {self.prefix}
            SELECT ?manufacturer ?salary
            WHERE {{
                ?manufacturer rdf:type dbo:Company ;
                            dbo:industry dbr:Automotive_industry ;
                            dbo:netIncome ?salary .

                FILTER(datatype(?salary)=dbd:euro)    
            }}
            ORDER BY DESC(xsd:integer(?salary))
            LIMIT 5
        """
# ---------------------------------------------------------------        
# Autres
    
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
    
##########################################################
#################### Group functions #####################
##########################################################
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

    def search_investors_of_group(self, group):
        return f"""
            {self.prefix}
        SELECT DISTINCT ?parentCompany ?owner
        WHERE {{
        ?car rdf:type dbo:MeanOfTransportation ;
            rdf:type dbo:Automobile ;
            dbo:manufacturer ?manufacturer .
                            
        OPTIONAL {{ 
            ?manufacturer dbo:parentCompany ?parentCompany . 
        }}
                        
        FILTER NOT EXISTS {{
            ?parentCompany dbo:parentCompany ?grandParentCompany . 
        }}
                        
        OPTIONAL {{
            ?parentCompany dbp:owners ?owner . 
            # Alternatively, if 'dbp:owners' is correct:
            # ?parentCompany dbp:owners ?owner . 
        }}
                        
        FILTER(REGEX(STR(?parentCompany), '{group}', "i"))
        }}
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
