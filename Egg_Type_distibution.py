''' script for counting egg_group frequencies by type'''

import pandas as pd
import json

poke = pd.read_csv('Pokemon.csv')


def unique_from_lists(col):
    unqs_list = poke[col].unique().tolist()
    unqs_set = set()

    for unqs in unqs_list:
        unqs = unqs.strip("']['").split("', '")

        for u in unqs:
            unqs_set.add(u)

    return list(unqs_set)


p_types = unique_from_lists('type')
egg_groups = unique_from_lists('egg_groups')

type_eggs = {t: {e: 0 for e in egg_groups} for t in p_types}


for i, p in poke.iterrows():
    p_eggs = p['egg_groups'].strip("']['").split("', '")
    p_types = p['type'].strip("']['").split("', '")

    for t in p_types:
        for e in p_eggs:
            type_eggs[t][e] += 1


with open("type_egg.json", "w") as f:
    json.dump(type_eggs, f, indent=4)
