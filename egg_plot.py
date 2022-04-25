import matplotlib.pyplot as plt


water = {

    "Fairy": 2,
    "No Eggs": 2,
    "Bug": 1,
    "Grass": 3,
    "Monster": 13,

    "Field": 12,
    "Dragon": 7,
    "Flying": 2,
    "Water 2": 17,
    "Water 3": 15,

    "Water 1": 53
}

'''
"mineral": 0,
"ditto": 0,
"human-like": 0,
"amorphous": 0,
'''

fire = {
    "No Eggs": 4,
    "Monster": 3,
    "Human-Like": 1,
    "Amorphous": 2,
    "Field": 18,
    "Dragon": 3,
}

'''
"ditto": 0,
"fairy": 0,
"flying": 0,
"water2": 0,
"water3": 0,
"mineral": 0,
"water1": 0,
"bug": 0,
"plant": 0,
'''


plt.pie(fire.values(), labels=fire.keys(), autopct='%1.0f%%', pctdistance=1.1,
        labeldistance=1.2)

# Plot
plt.axis('equal')
plt.show()
