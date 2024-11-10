import os
from neo4j import GraphDatabase

class ConsultDB:
    def __init__(self, url, user, pwd):
        self.driver = GraphDatabase.driver(url, auth=(user, pwd))

    def close(self):
        self.driver.close()

    def run_query(self, query, parameters=None):
        with self.driver.session() as session:
            result = session.run(query, parameters)
            return [record for record in result]

    def get_pokemon_by_name(self, name):
        query = """
            MATCH (p:POKEMON {name: $name})
            OPTIONAL MATCH (p)-[:IS]->(t:TYPE)
            OPTIONAL MATCH (p)-[:HAS]->(a:ABILITY)
            RETURN p.name AS name, p.number AS number, p.url AS url, 
                   p.height AS height, p.weight AS weight, 
                   collect(t.type) AS types, 
                   collect(a.ability) AS abilities
        """
        result = self.run_query(query, {"name": name})
        return result

    def get_pokemon_by_type(self, pokemon_type):
        query = """
            MATCH (p:POKEMON)-[:IS]->(t:TYPE {type: $pokemon_type})
            RETURN p.name AS name, p.number AS number, p.url AS url, 
                   p.height AS height, p.weight AS weight
        """
        result = self.run_query(query, {"pokemon_type": pokemon_type})
        return result

    def get_pokemon_by_ability(self, ability):
        query = """
            MATCH (p:POKEMON)-[:HAS]->(a:ABILITY {ability: $ability})
            RETURN p.name AS name, p.number AS number, p.url AS url, 
                   p.height AS height, p.weight AS weight
        """
        result = self.run_query(query, {"ability": ability})
        return result

    def get_pokemon_evolutions(self, name):
        query = """
            MATCH (p1:POKEMON {name: $name})-[:ENVOLVES]->(p2:POKEMON)
            RETURN p1.name AS pokemon, p2.name AS evolves_to, p2.number AS evolves_to_number
        """
        result = self.run_query(query, {"name": name})
        return result

    def get_pokemon_with_evolution_chain(self, name):
        query = """
            MATCH (p1:POKEMON {name: $name})
            OPTIONAL MATCH (p1)-[:ENVOLVES*]->(p2:POKEMON)
            RETURN p1.name AS pokemon, 
                   collect(p2.name) AS evolution_chain
        """
        result = self.run_query(query, {"name": name})
        return result

if __name__ == "__main__":
    password = ""
    url = "neo4j+s://c9b9faa6.databases.neo4j.io"
    user = "neo4j"

    db = ConsultDB(url, user, password)

    # Example Queries
    print("Pokémon Details by Name:")
    print(db.get_pokemon_by_name("Pikachu"))

    print("\nPokémon by Type 'Electric':")
    print(db.get_pokemon_by_type("Electric"))

    print("\nPokémon by Ability 'Static':")
    print(db.get_pokemon_by_ability("Static"))

    print("\nEvolution Chain for 'Bulbasaur':")
    print(db.get_pokemon_with_evolution_chain("Bulbasaur"))

    db.close()
