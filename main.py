import scrapy

class PokemonScrapper(scrapy.Spider):
    name = 'pokemon_scrapper'
    domain = "https://pokemondb.net"

    start_urls = ["https://pokemondb.net/pokedex/all"]


    def parse(self, response):
        pokemons = response.css('#pokedex > tbody > tr')
        # Por agora vamos só pegar o primeiro Pokémon para exemplo
        #pokemon = pokemons[0]
        for pokemon in pokemons:
            link = pokemon.css("td.cell-name > a::attr(href)").extract_first()
            yield response.follow(self.domain + link, self.parse_pokemon)


    def parse_pokemon(self, response):
        pokemon_number = response.css('.vitals-table > tbody > tr:nth-child(1) > td > strong::text').get()
        pokemon_name = response.css('#main > h1::text').get()
        pokemon_url = response.url
        pokemon_height = response.css('.vitals-table > tbody > tr:nth-child(4) > td::text').get()
        pokemon_weight = response.css('.vitals-table > tbody > tr:nth-child(5) > td::text').get()
        pokemon_types = response.css('.tabset-basics .vitals-table > tbody > tr:nth-child(2) > td > a::text').getall()

        pokemon_abilities_names = response.css('.vitals-table > tbody > tr:nth-child(6) > td a::text').getall()
        pokemon_abilities_hrefs = response.css('.vitals-table > tbody > tr:nth-child(6) > td a::attr(href)').getall()
        pokemon_abilities = []

       
        yield {
                'pokemon_number': pokemon_number,
                'pokemon_name': pokemon_name,
                'pokemon_url': pokemon_url,
                'pokemon_height': pokemon_height,
                'pokemon_weight': pokemon_weight,
                'pokemon_types': pokemon_types
                    
                
                #'pokemon_height': pokemon_height,
                #'pokemon_weight': pokemon_weight,
                #'pokemon_types': pokemon_types,
                #'pokemon_abilities': pokemon_abilities
            }
        
        


    def parse_ability(self, response):
        # Recebendo os dados do Pokémon através de 'meta'
        pokemon_number = response.meta['pokemon_number']
        pokemon_name = response.meta['pokemon_name']
        pokemon_height = response.meta['pokemon_height']
        pokemon_weight = response.meta['pokemon_weight']
        pokemon_types = response.meta['pokemon_types']
        ability_name = response.meta['ability_name']
        pokemon_abilities = response.meta['pokemon_abilities']
        abilities_len = response.meta['abilities_len']

        # Extraindo a descrição da habilidade
        ability_description = ''.join(response.css('main div:nth-child(1) > p *::text').getall())

        # Adicionando a habilidade ao nosso array de habilidades
        pokemon_abilities.append({
            'name': ability_name,
            'description': ability_description,
            'list': ['a', 'b']
        })

        # Verificando se coletamos todas as habilidades
        if abilities_len == len(pokemon_abilities):
            yield {
                'pokemon_number': pokemon_number,
                'pokemon_name': pokemon_name,
                
                #'pokemon_height': pokemon_height,
                #'pokemon_weight': pokemon_weight,
                #'pokemon_types': pokemon_types,
                #'pokemon_abilities': pokemon_abilities
            }