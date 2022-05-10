import json
import os
from random import randrange
from dash import Dash, html, dcc, callback, Output, Input, State
import pandas as pd

app = Dash(__name__)

app.layout = html.Div(children=html.Center(children=[
    html.H1(children='June is Smelly'),
    html.H3(children='''
        Get your pokemans
    '''),
    html.Div(children=[
        html.H5('''Step 1: Input Pokeman Name'''),
        dcc.Textarea(
            id='pokeman-search',
            style={
                'width': '400px',
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                'margin': '10px'
            },
        ),
        html.H5('''Step 2: Choose Pokeman file'''),
        dcc.Dropdown(options=[], id="fileSelect", style={'color':'black', 'textAlign':'center'}),
        html.H5('''Step 3: Generate Input And Name Pokemon'''),
dcc.Textarea(
            id='pokeman-name',
            style={
                'width': '400px',
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                'margin': '10px'
            },
        ),
dcc.Textarea(
        id='textarea',
        value='Hit Submit',
        style={'width': '100%', 'height': 300},
    ),html.Div(children=[dcc.Clipboard(
        target_id="textarea",
        title="copy",
        style={
            "display": "inline-block",
            "fontSize": 50,
            "verticalAlign": "top",
        },
    ),
        html.Button('Submit', id='submit-val', n_clicks=0, style={'margin-top': '25px'})]),

    ])
], style={'max-width': '85%',
          'margin': 'auto'}))
server = app.server
def find_files(filename):
    path = os.path.dirname(os.path.realpath(__file__))
    files = []
    for f_name in os.listdir(f'{path}/Pokedex'):
        if f_name.endswith('.json'):
            if filename.lower() in f_name.lower():
                files.append(f'Pokedex/{f_name}')
    return files

def build_pokemon(copyFromPokemon, name):

    template = open('template.json')
    templatePokemon = json.load(template)
    natures = [
        "adamant",
        "bashful",
        "bold",
        "brave",
        "calm",
        "careful",
        "docile",
        "gentle",
        "hardy",
        "hasty",
        "impish",
        "jolly",
        "lax",
        "lonely",
        "mild",
        "modest",
        "naive",
        "naughty",
        "quiet",
        "quirky",
        "rash",
        "relaxed",
        "sassy",
        "serious",
        "timid"
    ]
    # stuff to be generated
    # species
    templatePokemon['species'] = copyFromPokemon['character']['name']
    # name
    templatePokemon['character_name'] = name
    # random nature type
    randomNature = int(randrange(0, 24))
    templatePokemon['nature-type'] = natures[randomNature]
    # random sex
    randomSex = int(randrange(1, 2))
    if randomSex == 1:
        templatePokemon['pokemon_sex'] = 'Male'
    else:
        templatePokemon['pokemon_sex'] = 'Female'
    #origin
    templatePokemon['origin'] = copyFromPokemon['character']['name']
    # get rest of the info from here
    pokemon = attribute_format(copyFromPokemon['character']['attribs'], templatePokemon)
    return pokemon

def attribute_format(data, template):
    moves = {}
    for attr in data:
        attribute = list(attr.values())
        if attribute[0] == "type1":
            template['type1'] = attribute[1]
        if attribute[0] == "type2":
            template['type2'] = attribute[1]
        if attribute[0] == "size":
            template['size'] = attribute[1]
        if attribute[0] == "weight":
            template['weight'] = attribute[1]
        if attribute[0] == "egg_group":
            template['egg_group'] = attribute[1]
        if attribute[0] == "diet":
            template['diet'] = attribute[1]
        if attribute[0] == "HP":
            template['HP'] = attribute[1]
        if attribute[0] == "HP_max":
            template['HP'] = attribute[1]
        if attribute[0] == "atkbase":
            template['atkbase'] = attribute[2]
        if attribute[0] == "defbase":
            template['defbase'] = attribute[1]
        if attribute[0] == "spatkbase":
            template['spatkbase'] = attribute[1]
        if attribute[0] == "spdefbase":
            template['spdefbase'] = attribute[1]
        if attribute[0] == "spdbase":
            template['spdbase'] = attribute[1]
        if attribute[0] == "spdbase":
            template['spdbase'] = attribute[1]
        if attribute[0] == "pokemonskills":
            template['pokemonskills'] = attribute[1]
        if attribute[0] == "statpassives":
            template['statpassives'] = attribute[1]
        if attribute[0] == "otherpassives":
            template['otherpassives'] = attribute[1]

        if attribute[0].startswith("repeating_moves"):
            parsed_move = "_".join(attribute[0].split("_", 3)[:3])
            if parsed_move not in moves:
                if attribute[0] == f'{parsed_move}_move_name':
                    moves[parsed_move] = {
                    "move_name": attribute[1],
                    "move_range": "",
                    "move_type": "",
                    "move_category": "",
                    "move_frequency": "",
                    "move_dicenumber": "0",
                    "damage_dice": "0",
                    "move_acmod": "0",
                    "move_damagebonus": "0",
                    "move_template": "move-roll",
                    "move_effect1_threshold": "0",
                    "move_effect1_name": "",
                    "move_effect2_threshold": "0",
                    "move_effect2_name": "",
                    "move_effect": ""
                }
                if attribute[0] == f'{parsed_move}_move_effect':
                    moves[parsed_move] = {
                    "move_name": "",
                    "move_range": "",
                    "move_type": "",
                    "move_category": "",
                    "move_frequency": "",
                    "move_dicenumber": "0",
                    "damage_dice": "0",
                    "move_acmod": "0",
                    "move_damagebonus": "0",
                    "move_template": "move-roll",
                    "move_effect1_threshold": "0",
                    "move_effect1_name": "",
                    "move_effect2_threshold": "0",
                    "move_effect2_name": "",
                    "move_effect": attribute[1]
                }
                if attribute[0] == f'{parsed_move}_move_range':
                    moves[parsed_move] = {
                    "move_name": "",
                    "move_range": attribute[1],
                    "move_type": "",
                    "move_category": "",
                    "move_frequency": "",
                    "move_dicenumber": "0",
                    "damage_dice": "0",
                    "move_acmod": "0",
                    "move_damagebonus": "0",
                    "move_template": "move-roll",
                    "move_effect1_threshold": "0",
                    "move_effect1_name": "",
                    "move_effect2_threshold": "0",
                    "move_effect2_name": "",
                    "move_effect": ""
                }
                if attribute[0] == f'{parsed_move}_move_type':
                    moves[parsed_move] = {
                    "move_name": "",
                    "move_range": "",
                    "move_type": attribute[1],
                    "move_category": "",
                    "move_frequency": "",
                    "move_dicenumber": "0",
                    "damage_dice": "0",
                    "move_acmod": "0",
                    "move_damagebonus": "0",
                    "move_template": "move-roll",
                    "move_effect1_threshold": "0",
                    "move_effect1_name": "",
                    "move_effect2_threshold": "0",
                    "move_effect2_name": "",
                    "move_effect": ""
                }
                if attribute[0] == f'{parsed_move}_move_category':
                    moves[parsed_move] = {
                    "move_name": "",
                    "move_range": "",
                    "move_type": "",
                    "move_category": attribute[1],
                    "move_frequency": "",
                    "move_dicenumber": "0",
                    "damage_dice": "0",
                    "move_acmod": "0",
                    "move_damagebonus": "0",
                    "move_template": "move-roll",
                    "move_effect1_threshold": "0",
                    "move_effect1_name": "",
                    "move_effect2_threshold": "0",
                    "move_effect2_name": "",
                    "move_effect": ""
                }
                if attribute[0] == f'{parsed_move}_move_frequency':
                    moves[parsed_move] = {
                    "move_name": "",
                    "move_range": "",
                    "move_type": "",
                    "move_category": "",
                    "move_frequency": attribute[1],
                    "move_dicenumber": "0",
                    "damage_dice": "0",
                    "move_acmod": "0",
                    "move_damagebonus": "0",
                    "move_template": "move-roll",
                    "move_effect1_threshold": "0",
                    "move_effect1_name": "",
                    "move_effect2_threshold": "0",
                    "move_effect2_name": "",
                    "move_effect": ""
                }
                if attribute[0] == f'{parsed_move}_move_dicenumber':
                    moves[parsed_move] = {
                    "move_name": "",
                    "move_range": "",
                    "move_type": "",
                    "move_category": "",
                    "move_frequency": "",
                    "move_dicenumber": attribute[1],
                    "damage_dice": "0",
                    "move_acmod": "0",
                    "move_damagebonus": "0",
                    "move_template": "move-roll",
                    "move_effect1_threshold": "0",
                    "move_effect1_name": "",
                    "move_effect2_threshold": "0",
                    "move_effect2_name": "",
                    "move_effect": ""
                }
                if attribute[0] == f'{parsed_move}_move_damage_dice':
                    moves[parsed_move] = {
                    "move_name": "",
                    "move_range": "",
                    "move_type": "",
                    "move_category": "",
                    "move_frequency": "",
                    "move_dicenumber": "0",
                    "damage_dice": attribute[1],
                    "move_acmod": "0",
                    "move_damagebonus": "0",
                    "move_template": "move-roll",
                    "move_effect1_threshold": "0",
                    "move_effect1_name": "",
                    "move_effect2_threshold": "0",
                    "move_effect2_name": "",
                    "move_effect": ""
                }
                if attribute[0] == f'{parsed_move}_move_effect1_threshold':
                    moves[parsed_move] = {
                    "move_name": "",
                    "move_range": "",
                    "move_type": "",
                    "move_category": "",
                    "move_frequency": "",
                    "move_dicenumber": "0",
                    "damage_dice": "",
                    "move_acmod": "0",
                    "move_damagebonus": "0",
                    "move_template": "move-roll",
                    "move_effect1_threshold": attribute[1],
                    "move_effect1_name": "",
                    "move_effect2_threshold": "0",
                    "move_effect2_name": "",
                    "move_effect": ""
                }
                if attribute[0] == f'{parsed_move}_move_effect1_name':
                    moves[parsed_move] = {
                    "move_name": "",
                    "move_range": "",
                    "move_type": "",
                    "move_category": "",
                    "move_frequency": "",
                    "move_dicenumber": "0",
                    "damage_dice": "",
                    "move_acmod": "0",
                    "move_damagebonus": "0",
                    "move_template": "move-roll",
                    "move_effect1_threshold": "0",
                    "move_effect1_name": attribute[1],
                    "move_effect2_threshold": "0",
                    "move_effect2_name": "",
                    "move_effect": ""
                }
                if attribute[0] == f'{parsed_move}_move_effect2_threshold':
                    moves[parsed_move] = {
                    "move_name": "",
                    "move_range": "",
                    "move_type": "",
                    "move_category": "",
                    "move_frequency": "",
                    "move_dicenumber": "0",
                    "damage_dice": "",
                    "move_acmod": "0",
                    "move_damagebonus": "0",
                    "move_template": "move-roll",
                    "move_effect1_threshold": "0",
                    "move_effect1_name": "",
                    "move_effect2_threshold": attribute[1],
                    "move_effect2_name": "",
                    "move_effect": ""
                }
                if attribute[0] == f'{parsed_move}_move_effect2_name':
                    moves[parsed_move] = {
                    "move_name": "",
                    "move_range": "",
                    "move_type": "",
                    "move_category": "",
                    "move_frequency": "",
                    "move_dicenumber": "0",
                    "damage_dice": "",
                    "move_acmod": "0",
                    "move_damagebonus": "0",
                    "move_template": "move-roll",
                    "move_effect1_threshold": "0",
                    "move_effect1_name": "",
                    "move_effect2_threshold": "0",
                    "move_effect2_name": attribute[1],
                    "move_effect": ""
                }
            else:
                if attribute[0] == f'{parsed_move}_move_name':
                    moves[parsed_move]["move_name"] = attribute[1]
                if attribute[0] == f'{parsed_move}_move_range':
                    moves[parsed_move]["move_range"] = attribute[1]
                if attribute[0] == f'{parsed_move}_move_type':
                    moves[parsed_move]["move_type"] = attribute[1]
                if attribute[0] == f'{parsed_move}_move_category':
                    moves[parsed_move]["move_category"] = attribute[1]
                if attribute[0] == f'{parsed_move}_move_frequency':
                    moves[parsed_move]["move_frequency"] = attribute[1]
                if attribute[0] == f'{parsed_move}_move_dicenumber':
                    moves[parsed_move]["move_dicenumber"] = attribute[1]
                if attribute[0] == f'{parsed_move}_damage_dice':
                    moves[parsed_move]["damage_dice"] = attribute[1]
                if attribute[0] == f'{parsed_move}_move_effect':
                    moves[parsed_move]["move_effect"] = attribute[1]
                if attribute[0] == f'{parsed_move}_move_effect1_threshold':
                    moves[parsed_move]["move_effect1_threshold"] = attribute[1]
                if attribute[0] == f'{parsed_move}_move_effect1_name':
                    moves[parsed_move]["move_effect1_name"] = attribute[1]
                if attribute[0] == f'{parsed_move}_move_effect2_threshold':
                    moves[parsed_move]["move_effect1_threshold"] = attribute[1]
                if attribute[0] == f'{parsed_move}_move_effect2_name':
                    moves[parsed_move]["move_effect1_name"] = attribute[1]

    moves_to_template = []
    movesT = list(moves.values())
    template['exportmoves'] = movesT
    return template

@callback(Output('fileSelect', 'options'),
          [Input('pokeman-search', 'value')])
def display_page(value):
    files_found = find_files(value)
    return files_found

@app.callback(
    Output('textarea', 'value'),
    Input('submit-val', 'n_clicks'),
    Input('fileSelect', 'value'),
    Input('pokeman-name', 'value')
)
def update_output(n_clicks, value, name):
    if n_clicks:
        f = open(f'{value}')
        data = json.load(f)
        finalEncoded = (json.dumps((build_pokemon(data, name)), ensure_ascii=False).encode('utf8'))
        return finalEncoded.decode()

if __name__ == "__main__":
    app.run_server(debug=True)

