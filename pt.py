import load
import sim
import copy
import elo
import random
import csv

N_SIMULATIONS = int(1e6)

parsed_data = load.load_leagues(['POR'])

full_results = {}
placements = {}

for team in parsed_data['POR']['team_elo'].keys():
    full_results[team] = [0] * len(parsed_data['POR']['team_elo'])
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
    if i % int(1e5) == 0:
        print(i)

    table = sim.simulate_league(parsed_data['POR']['team_elo'],
            copy.deepcopy(parsed_data['POR']['table']),
            parsed_data['POR']['schedule'],
            parsed_data['POR']['hfa'],
            h2h=parsed_data['POR']['h2h'],
            temp_h2h=copy.deepcopy(parsed_data['POR']['temp_h2h']))

    for j, team in enumerate(table):
        full_results[team][j] += 1

    cl = [table[0], table[1], table[2]]
    placements[cl[0]]['CL-G'] += 1
    placements[cl[1]]['CL-G'] += 1
    placements[cl[2]]['CL-3Q'] += 1

    table = table[3::]

    placements[table[0]]['EL-G'] += 1
    placements[table[1]]['ECL-Pl'] += 1
    placements[table[2]]['ECL-2Q'] += 1

    table = list(reversed(table))

    placements[table[0]]['D'] += 1
    placements[table[1]]['D'] += 1
    placements[table[2]]['D-P'] += 1

for team in full_results.keys():
    for i, times in enumerate(full_results[team]):
        full_results[team][i] = times / N_SIMULATIONS

    with open('res/POR.csv', 'w', newline='') as output_file:
        writer = csv.writer(output_file)
        row_names = ['Team']

        for i in range(len(parsed_data['POR']['team_elo'].keys())):
            row_names.append(str(i+1))

        writer.writerow(row_names)

        for team in full_results.keys():
            row = [team]
            row.extend(full_results[team])
            writer.writerow(row)

for team in placements.keys():
    for key in placements[team]:
        placements[team][key] /= N_SIMULATIONS

    with open('res/POR_qual.csv', 'w', newline='') as output_file:
        writer = csv.writer(output_file)
        row_names = ['Team', 'CL-G', 'CL-3Q', 'EL-G', 'ECL-Pl', 'ECL-2Q', 'D-P', 'D']

        writer.writerow(row_names)

        for team in placements.keys():
            row = [team]
            row.extend(placements[team].values())
            writer.writerow(row)