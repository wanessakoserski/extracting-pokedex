import pandas as pd
import json


# Fazer o conversor entender a estrutura json já montada
def convert_to_list(json_structure):
    if isinstance(json_structure, str):
        try:
            return json.loads(json_structure.replace("'", '"'))
        
        except json.JSONDecodeError:
            # Em caso de erro no JSON, retorna o valor original
            return json_structure
        
    # Retorna o valor original se não for uma string   
    return json_structure  


data = pd.read_csv('file.csv')

# Pegar apenas os primeiros caracteres
data['pokemon_height'] = data['pokemon_height'].str.split('\u00a0').str[0]
data['pokemon_weight'] = data['pokemon_weight'].str.split('\u00a0').str[0]

# Formatar para lista quando necessário para o conversor de json entender
data['pokemon_types'] = data['pokemon_types'].apply(lambda x: list(set(x.split(','))) if ',' in x else x)
data['pokemon_abilities'] = data['pokemon_abilities'].apply(lambda x: list(set(x.split(','))) if ',' in x else x)

# Fazer o conversor entender a estrutura json já montada
data['pokemon_evolution'] = data['pokemon_evolution'].apply(convert_to_list)

# Convertendo para json
data.to_json('pokemons.json', orient='records', lines=False, indent=4)

print(data)