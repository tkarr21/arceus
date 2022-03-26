'''

choose and apply color scheme (pillow)

'''

# imports and reading csv
# %%
import pandas as pd
import random
import math
import json
import os
from collage import collage

poke = pd.read_csv('Pokemon.csv', header=None, skiprows=1)
poke.columns = field_names = ['name', 'dex', 'type', 'egg_groups', 'color', 'shape',
                              'hp', 'attack', 'defense', 'sp_attack', 'sp_defense', 'speed']

body_json = None
with open('body.json') as f:
    body_json = json.load(f)


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


def get_poke_egg(egg_group: str) -> pd.DataFrame:
    # get all pokemon of specified egg_group
    return poke.loc[poke['egg_groups'].str.contains(egg_group)]


def get_dist(poke_spec: dict, k: int, p_type: str = 'none', poke_to_distance: pd.DataFrame = poke, measure_: str = 'euclidean') -> pd.DataFrame:
    measure = euclidean if measure_ == 'euclidean' else manhattan

    dists = []
    for i in range(len(poke_to_distance)):
        dists += [measure(poke_to_distance.iloc[i], poke_spec)]

    return poke_to_distance.assign(
        distance=dists).nsmallest(k, columns='distance')


# Shape and asset selection
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
    # defualting to upright if not quadruped
    if shape != 'quadruped':
        return 'upright'

    return shape


def sample_freq_dict(distrib) -> str:

    marbles = []
    for k, v in distrib.items():
        for i in range(v):
            marbles += [k]

    selection = random.randint(0, len(marbles) - 1)

    return marbles[selection]


def get_egg_group(p_type):
    with open('type_egg.json') as f:
        type_egg_json = json.load(f)

    egg_distrib = type_egg_json[p_type]

    return sample_freq_dict(egg_distrib)


def get_head(target, egg_group):
    egg_df = get_poke_egg(egg_group)

    elected = get_dist(target, 1, poke_to_distance=egg_df)
    return int(elected["dex"])


def get_tail(target, egg_group):
    # available tails assets
    tails = [int(x[:-4]) if '-' not in x else int(x[:-6])
             for x in os.listdir('assets/tail')]
    tails_df = poke.loc[poke['dex'].isin(tails)]
    tail_egg_df = tails_df.loc[poke['egg_groups'].str.contains(egg_group)]

    # check if available tails in egg group
    to_distance_df = tails_df if tail_egg_df.empty else tail_egg_df
    elected = get_dist(target, 1, poke_to_distance=to_distance_df)

    return int(elected['dex'])


def select_limb_donor(target, egg_group, num_limbs, limb):
    # available arms
    limbs = [x[:-6]
             for x in os.listdir(f'assets/{limb}') if str(num_limbs) == x[-5]]
    limbs_df = poke.loc[poke['dex'].isin([int(l) for l in limbs])]
    limbs_egg_df = limbs_df.loc[poke['egg_groups'].str.contains(egg_group)]

    # check if available arms in egg group
    to_distance_df = limbs_df if limbs_egg_df.empty else limbs_egg_df
    elected = get_dist(target, 1, poke_to_distance=to_distance_df)

    return int(elected['dex'])


def get_appendages(target, parts):
    appendages = {}

    num_arms = 0
    num_legs = 0
    num_wings = 0
    num_fins = 0

    for part in parts:
        if part == 'head':
            egg_group = get_egg_group(target['type'])
            appendages[part] = f'assets/head/{get_head(target, egg_group)}.png'
        if part == 'tail':
            egg_group = get_egg_group(target['type'])
            appendages[part] = f'assets/tail/{get_tail(target, egg_group)}.png'
        if 'arm' in part:
            num_arms += 1
        if 'leg' in part:
            num_legs += 1
        if 'wing' in part:
            num_wings += 1
        if 'fin' in part:
            num_fins += 1

    if num_arms:
        egg_group = get_egg_group(target['type'])
        arm_donor = select_limb_donor(target, egg_group, num_arms, limb='arm')

        count = 1
        for part in parts:
            if 'arm' in part:
                appendages[part] = f'assets/arm/{arm_donor}-{count}.png'
                count += 1

    if num_legs:
        egg_group = get_egg_group(target['type'])
        leg_donor = select_limb_donor(target, egg_group, num_legs, limb='leg')

        # FIXME its gonna put leg-1.png as the back leg if back leg is the
        # first leg entry in the template json
        count = 1
        for part in parts:
            if 'leg' in part:
                appendages[part] = f'assets/leg/{leg_donor}-{count}.png'
                count += 1

    if num_wings:
        egg_group = get_egg_group(target['type'])
        wing_donor = select_limb_donor(
            target, egg_group, num_wings, limb='wing')

        count = 1
        for part in parts:
            if 'wing' in part:
                appendages[part] = f'assets/wing/{wing_donor}-{count}.png'
                count += 1

    if num_fins:
        egg_group = get_egg_group(target['type'])
        fin_donor = select_limb_donor(target, egg_group, num_fins, limb='fin')

        count = 1
        for part in parts:
            if 'fin' in part:
                appendages[part] = f'assets/fin/{fin_donor}-{count}.png'
                count += 1

    return appendages


def get_body_template(target, shape):
    candidates = None
    if shape == 'upright':
        candidates = body_json[shape]
    elif shape == 'quadruped':
        candidates = body_json[shape]
    else:
        return

    candidates_df = poke.loc[poke['dex'].isin([int(c) for c in candidates])]
    elected = get_dist(target, 1, poke_to_distance=candidates_df)

    return str(int(elected["dex"]))


# %%
# inputs
stats = ['hp', 'attack', 'defense', 'sp_attack', 'sp_defense', 'speed']
values = [75, 86, 68, 31, 42, 91]
target_type = 'normal'
###


target = {stat: values[i] for i, stat in enumerate(stats)}
target['type'] = target_type
k = 5

typed_distance = get_dist(
    target, k, poke_to_distance=get_poke_type(target['type']))
all_distance = get_dist(target, k)

# %%
shape = get_shape(typed_distance)
body_template = get_body_template(target, shape)

required_parts = list(body_json[shape][body_template].keys())
appendage_assets = get_appendages(target, required_parts)

print(f'assets/body/{body_template}.png')
print(json.dumps(appendage_assets, indent=4))

collage(f'assets/body/{body_template}.png',
        body_json[shape][str(body_template)], appendage_assets)

# %%
