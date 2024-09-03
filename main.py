import scrapy
import csv

class PokemonScrapper(scrapy.Spider):
    name = 'pokemon_scrapper'
    domain = "https://pokemondb.net"

    start_urls = ["https://pokemondb.net/pokedex/all"]


    def parse(self, response):
        pokemons = response.css('#pokedex > tbody > tr')
        for pokemon in pokemons:
            link = pokemon.css("td.cell-name > a::attr(href)").extract_first()
            yield scrapy.Request(self.domain + link, callback=self.parse_pokemon)


    def parse_pokemon(self, response):
        pokemon_number = response.css('.vitals-table > tbody > tr:nth-child(1) > td > strong::text').get()
        pokemon_name = response.css('#main > h1::text').get()
        pokemon_url = response.url
        pokemon_height = response.css('.vitals-table > tbody > tr:nth-child(4) > td::text').get()
        pokemon_weight = response.css('.vitals-table > tbody > tr:nth-child(5) > td::text').get()
        pokemon_types = response.css('.tabset-basics .vitals-table > tbody > tr:nth-child(2) > td > a::text').getall()

        pokemon_evolution = []
        
        # Seleciona todas as seções de evolução
        evolution_sections = response.css('#main > .infocard-list-evo')
        
        generation = 1
        for section in evolution_sections:
            elements = section.xpath('./*')
            
            for element in elements:
                # Verifica a classe do elemento
                classes = element.xpath('./@class').get().split()

                # Faz uma ação dependendo da classe do elemento
                if 'infocard' in classes:
                    # Elemento que contém informações do Pokémon
                    if element.css('.ent-name::text').get():
                        evolution_name = element.css('.ent-name::text').get()
                        evolution_href = element.css('.ent-name::attr(href)').get()
                        evolution_number = element.css('span.infocard-lg-data.text-muted > small::text').get()
                        evolution_pokemon = {
                            'generation': generation,
                            'number': evolution_number,
                            'name': evolution_name,
                            'url': self.domain + evolution_href
                        }
                        
                        existing_pokemon_generation = None
                        if pokemon_evolution != []:
                            for p in pokemon_evolution:
                                if p['name'] == evolution_pokemon['name'] :
                                    existing_pokemon_generation = p['generation']
                                    break

                        if existing_pokemon_generation is not None:
                            generation = existing_pokemon_generation
                        else:
                            pokemon_evolution.append(evolution_pokemon)
                            #print(generation, evolution_name)

                        generation = generation + 1
                
                elif 'infocard-evo-split' in classes:
                    for sub_element in element.css('div.infocard-list-evo > div.infocard'):
                        evolution_name = sub_element.css('.ent-name::text').get()
                        evolution_href = element.css('.ent-name::attr(href)').get()
                        evolution_number = element.css('.infocard-lg-data.text-muted > small:nth-child(1)::text').get()
                        evolution_pokemon = {
                            'generation': generation,
                            'number': evolution_number,
                            'name': evolution_name,
                            'url': self.domain + evolution_href
                        }
                        
                        existing_pokemon_generation = None
                        if pokemon_evolution != []:
                            for p in pokemon_evolution:
                                if p['name'] == evolution_pokemon['name']:
                                    existing_pokemon_generation = p['generation']
                                    break

                        if existing_pokemon_generation is not None:
                            generation = existing_pokemon_generation
                        else:
                            pokemon_evolution.append(evolution_pokemon)
                            #print(generation, evolution_name)
                    
                    generation = generation + 1

                # Adicione outras verificações conforme necessário
        pokemon_abilities = []

        pokemon_abilities_names = response.css('.vitals-table > tbody > tr:nth-child(6) > td > span > a::text').getall()
        # pokemon_abilities_hrefs = response.css('.vitals-table > tbody > tr:nth-child(6) > td > span > a::attr(href)').getall()
        
        
        yield {
                'pokemon_number': pokemon_number,
                'pokemon_name': pokemon_name,
                'pokemon_height': pokemon_height,
                'pokemon_weight': pokemon_weight,
                'pokemon_types': pokemon_types,
                'pokemon_evolution': pokemon_evolution,
                'pokemon_abilities': pokemon_abilities_names
            }
        