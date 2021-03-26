import json
import copy
import random
import time
import csv
import functools

random.seed(time.time())

N_SIMULATIONS = 1000000

@functools.cache
def calculate_result_probs(elo_A, elo_B, HFA=0, draw_possible=True):
    R = 0.4
    dr = elo_A - elo_B + HFA

    p = 1 / (10 ** (-dr / 400) + 1)

    if not draw_possible:
        return (p,0,1-p)

    w = p * (R + p - R * p)
    d = 2 * (p - w)
    l = 1 - w - d

    return (w,d,l)

full_results = {}
placements = {}

with open('por.json') as json_file:
    data = json.load(json_file)

hfa = data['HFA']
base_table = {}
team_elo = {}

for team in data['teams']:
    base_table[team['name']] = team['points']
    team_elo[team['name']] = team['elo']

for team in base_table.keys():
    full_results[team] = [0] * len(base_table)
    placements[team] = {
        'CL-G': 0,
        'CL-3Q': 0,
        'EL-G': 0,
        'ECL-Pl': 0,
        'ECL-2Q': 0,
        'D-P': 0,
        'D': 0
    }

for i in range(N_SIMULATIONS):
    table = copy.deepcopy(base_table)

    for game in data['schedule']:
        (w,d,l) = calculate_result_probs(team_elo[game['home']], team_elo[game['away']], HFA=hfa)
        result = random.choices(
            population=['w', 'd', 'l'],
            weights=[w,d,l],
            k=1
        )[0]
        if result == 'w':
            table[game['home']] += 3
        elif result == 'd':
            table[game['home']] += 1
            table[game['away']] += 1
        else:
            table[game['away']] += 3

    table = list(table.items())
    random.shuffle(table)
    table = list(reversed(sorted(table, key=lambda item: item[1])))

    for i, team in enumerate(table):
        full_results[team[0]][i] += 1

    (w,d,l) = calculate_result_probs(team_elo['Benfica'], team_elo['Braga'], draw_possible=False)

    result = random.choices(
            population=['w', 'l'],
            weights=[w,l],
            k=1
        )[0]

    if result == 'w':
        cup_winner = 'Benfica'
    else:
        cup_winner = 'Braga'

    cl = [table[0][0], table[1][0], table[2][0]]
    placements[cl[0]]['CL-G'] += 1
    placements[cl[1]]['CL-G'] += 1
    placements[cl[2]]['CL-3Q'] += 1

    table = table[3::]

    if cup_winner in cl:
        placements[table[0][0]]['EL-G'] += 1
        placements[table[1][0]]['ECL-Pl'] += 1
        placements[table[2][0]]['ECL-2Q'] += 1

    else:
        placements[cup_winner]['EL-G'] += 1

        for team in list(table):
            if cup_winner == team[0]:
                table.remove(team)

        placements[table[0][0]]['ECL-Pl'] += 1
        placements[table[1][0]]['ECL-2Q'] += 1

    table = list(reversed(table))

    placements[table[0][0]]['D'] += 1
    placements[table[1][0]]['D'] += 1
    placements[table[2][0]]['D-P'] += 1

for team in full_results.keys():
    for i, times in enumerate(full_results[team]):
        full_results[team][i] = times / N_SIMULATIONS

    with open('por.csv', 'w', newline='') as output_file:
        writer = csv.writer(output_file)
        row_names = ['Team']

        for i in range(len(base_table.keys())):
            row_names.append(str(i+1))

        writer.writerow(row_names)

        for team in full_results.keys():
            row = [team]
            row.extend(full_results[team])
            writer.writerow(row)

for team in placements.keys():
    for key in placements[team]:
        placements[team][key] /= N_SIMULATIONS

    with open('por_cl.csv', 'w', newline='') as output_file:
        writer = csv.writer(output_file)
        row_names = ['Team', 'CL-G', 'CL-3Q', 'EL-G', 'ECL-Pl', 'ECL-2Q', 'D-P', 'D']

        writer.writerow(row_names)

        for team in placements.keys():
            row = [team]
            row.extend(placements[team].values())
            writer.writerow(row)