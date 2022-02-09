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

poke = pd.read_csv('Pokemon.csv', header=None, skiprows=152, nrows=100)
poke.columns = field_names = ['name', 'dex', 'type', 'color', 'shape',
                              'hp', 'attack', 'defense', 'sp_attack', 'sp_defense', 'speed']

# helper functions
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


def get_typed_dist(poke_spec: dict, k: int, measure_: str = 'euclidean') -> pd.DataFrame:
    measure = euclidean if measure_ == 'euclidean' else manhattan
    poke_typed = get_poke_type(poke_spec['type'])

    dists = []
    for i in range(len(poke_typed)):
        dists += [measure(poke_typed.iloc[i], poke_spec)]

    return poke_typed.assign(
        distance=dists).nsmallest(k, columns='distance')


# %%
# inputs
stats = ['hp', 'attack', 'defense', 'sp_attack', 'sp_defense', 'speed']
values = [80, 65, 35, 70, 80, 55]
target_type = 'fire'

target = {stat: values[i] for i, stat in enumerate(stats)}
target['type'] = target_type
k = 5

get_typed_dist(target, k)
