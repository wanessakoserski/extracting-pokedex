import os
import json
from neo4j import GraphDatabase 
    

class CreateDB:
    def __init__(self, url, user, pwd):
        self.driver = GraphDatabase.driver(url, auth=(user, pwd))

    def close(self):
        self.driver.close()

    def run_return_query(self, query, parameters=None):
        with self.driver.session() as session:
            result = session.run(query, parameters)
            return list(result)
        
    def run_write_query(self, query, parameters=None):
        def execute_transaction(tx, query, parameters):
            tx.run(query, parameters)
        
        with self.driver.session() as session:
            session.write_transaction(execute_transaction, query, parameters)

    def clean_base(self):
        query = """
            MATCH (n) 
            DETACH DELETE n
        """
        self.run_write_query(query)

    def create_type_graph(self):
        with open('pokemons.json', 'r') as file:
            data = json.load(file)
        
        for item in data:
            number = item['pokemon_number']
            print(number)
            types = item['pokemon_types']
            for type in types:
                if len(type) <= 1:
                    type = types

                query = f"""
                MATCH (t:TYPE {{type: '{type}'}})
                RETURN count(t) > 0 AS exists
                """

                results = self.run_return_query(query)
                exists = False
                for item in results:
                    if item["exists"]:
                        exists = True

                if not exists:
                    id = type.lower().replace(" ", "")
                    query = f"""
                        CREATE ({id}:TYPE {{type: '{type}'}})
                        """
                    self.run_write_query(query)

    def create_ability_graph(self):
        with open('pokemons.json', 'r') as file:
            data = json.load(file)
        
        for item in data:
            number = item['pokemon_number']
            print(number)
            abilities = item['pokemon_abilities']
            for ability in abilities:
                if len(ability) <= 1:
                    ability = abilities
                ability = ability.replace("'", "")
                query = f"""
                MATCH (a:ABILITY {{ability: "{ability}"}})
                RETURN count(a) > 0 AS exists
                """

                results = self.run_return_query(query)
                exists = False
                for item in results:
                    if item["exists"]:
                        exists = True

                if not exists:
                    id = ability.lower().replace(" ", "")
                    ability = ability.replace("'", "")
                    query = f"""
                        CREATE (:ABILITY {{ability: "{ability}"}})
                        """
                    self.run_write_query(query)

    def create_pokemon_graph(self):
        with open('pokemons.json', 'r') as file:
            data = json.load(file)
        
        for item in data:
            number = item['pokemon_number']
            name = item['pokemon_name']
            url = item['pokemon_url']
            height = item['pokemon_height']
            weight = item['pokemon_weight']
            
            rename = name.lower().replace(" ", "").replace(".", "").replace("-", "").replace("'", "").replace("\u2642", "").replace("\u2640", "")
            rename = rename.replace("(", "").replace(")", "")
            id_pokemon = f"{rename}{str(number)}"

            query = f"""
                CREATE ({id_pokemon}:POKEMON {{name: "{name}", number: {number}, url: "{url}", height: "{height}", weight: "{weight}"}})
            """
            self.run_write_query(query)

            print(f"{number} {name}")

            types = item['pokemon_types']
            if isinstance(types, str):
                types = [ types ]

            for type in types: 
                if len(type) <= 1:
                    type = types

                query = f"""
                    MATCH (p:POKEMON {{number: {number}}}), (t:TYPE {{type: "{type}"}})
                    CREATE (p)-[:IS]->(t)
                """
                self.run_write_query(query)

            abilities = item['pokemon_abilities']
            if isinstance(abilities, str):
                abilities = [ abilities ]

            for ability in abilities: 
                ability = ability.replace("'", "")
                query = f"""
                    MATCH (p:POKEMON {{number: {number}}}), (a:ABILITY {{ability: "{ability}"}})
                    CREATE (p)-[:HAS]->(a)
                """
                self.run_write_query(query)

    def create_evolution_relation(self):
        with open('pokemons.json', 'r') as file:
            data = json.load(file)
        
        for item in data:
            main_number = item['pokemon_number']
            evos = item['pokemon_evolution']
            print(number)

            for evo in evos:
                generation = evo['generation']
                number = evo['number']
                number = number.lstrip("#0") 

                query = f"""
                    MATCH (p1:POKEMON {{number: {main_number}}}), (p2:POKEMON {{number: {number}}})
                    CREATE (p1)-[:ENVOLVES {{generation: {generation}}}]->(p2)
                """

                self.run_write_query(query)

            

password = ""
url = "neo4j+s://c9b9faa6.databases.neo4j.io"
user = "neo4j"

db = CreateDB(url, user, password)
db.clean_base()
db.create_type_graph()
db.create_ability_graph()
db.create_pokemon_graph()
db.close()
