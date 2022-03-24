'''
input: hp (int), att (int), sp att (int), def (int), sp def(int), speed(int), element TYPE

step 1:
grab k nearest (euclidean distance) pokemon from dataframe -> [pokemonIDs]

step 2:
Decide on a shape (grammar of construction) -> mode shape of [pokemonIDs]??
["ball", "squiggle", "fish", "arms", "blob", "upright", "legs", "quadruped", "wings", "tentacles", "heads", "humanoid", "bug-wings", "armor"]

based off shape grab required body parts from assets of [pokemonIDs] -> random??

layer body parts according to shape

choose and apply color scheme (pillow)

'''

# imports and reading csv
# %%
from numpy import double
import pandas as pd
import random
import math
import json

from collage import collage

poke = pd.read_csv('Pokemon.csv', header=None, skiprows=1)
poke.columns = field_names = ['name', 'dex', 'type', 'color', 'shape',
                              'hp', 'attack', 'defense', 'sp_attack', 'sp_defense', 'speed']

data = None
with open('body.json') as f:
    data = json.load(f)

# %%
# distance functions


def euclidean(poke1, poke2) -> float:
    stats = ['hp', 'attack', 'defense', 'sp_attack', 'sp_defense', 'speed']
    dist = 0
    for stat in stats:

        dist += (poke1[stat] - poke2[stat])**2

    return math.sqrt(dist)


def manhattan(poke1, poke2) -> int:
    stats = ['hp', 'attack', 'defense', 'sp_attack', 'sp_defense', 'speed']
    dist = 0
    for stat in stats:

        dist += abs(poke1[stat] - poke2[stat])

    return dist


def get_poke_type(type: str) -> pd.DataFrame:
    # get all pokemon of specified type (includes hybrid typed pokemon)
    return poke.loc[poke['type'].str.contains(type)]


def get_dist(poke_spec: dict, k: int, p_type: str = 'none', poke_to_distance: pd.DataFrame = poke, measure_: str = 'euclidean') -> pd.DataFrame:
    measure = euclidean if measure_ == 'euclidean' else manhattan

    dists = []
    for i in range(len(poke_to_distance)):
        dists += [measure(poke_to_distance.iloc[i], poke_spec)]

    return poke_to_distance.assign(
        distance=dists).nsmallest(k, columns='distance')


def get_shape(neighbors_df):
    # count freq of each shape in nearest neighbors
    shape_freq = {}
    for i, poke in neighbors_df.iterrows():
        if poke['shape'] in shape_freq:
            shape_freq[poke['shape']] += 1
        else:
            shape_freq[poke['shape']] = 1

    # order common neighbors
    ordered = sorted(shape_freq.values(), reverse=True)

    shape = 'upright'

    for k, v in shape_freq.items():
        if v == ordered[0]:
            shape = k

    # FIXME we only support upright and quadruped rn
    # defualting to upright if not quadreped
    if shape != 'quadruped':
        return 'upright'

    return shape


def get_egg_group(p_type):
    pass


def get_assets(target, shape):

    get_egg_group(target['type'])
    pass


def get_body_template(shape, target):
    candidates = None
    if shape == 'upright':
        candidates = data[shape]
    elif shape == 'quadruped':
        candidates = data[shape]
    else:
        return

    candidates_df = poke.loc[poke['dex'].isin([int(c) for c in candidates])]
    elected = get_dist(target, 1, poke_to_distance=candidates_df)

    return f'assets/body/{int(elected["dex"])}.png'


# %%
# inputs
stats = ['hp', 'attack', 'defense', 'sp_attack', 'sp_defense', 'speed']
values = [80, 65, 35, 70, 80, 55]
target_type = 'fire'
###

target = {stat: values[i] for i, stat in enumerate(stats)}
target['type'] = target_type
k = 5

typed_distance = get_dist(
    target, k, poke_to_distance=get_poke_type(target['type']))
all_distance = get_dist(target, k)

# %%
shape = get_shape(typed_distance)
body_template = get_body_template(shape, target)

appendage_assets = get_assets(target, shape)


# %%
