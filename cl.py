import load
import sim
import copy

N_SIMULATIONS = 1000000
leagues = ['ESP', 'ENG', 'GER', 'ITA', 'FRA', 'POR', 'RUS', 'BEL', 'UKR', 'NED', 'TUR']
group_places = {
    'ESP': 4,
    'ENG': 4,
    'GER': 4,
    'ITA': 4,
    'FRA': 2,
    'POR': 2,
    'RUS': 1,
    'BEL': 1,
    'UKR': 1,
    'NED': 1,
    'TUR': 0
}

full_results = {}
six_teams = 0
parsed_data = load.load_cups(['CL', 'EL'])
parsed_data.update(load.load_leagues(leagues))

def run_iteration():
    six_team_exception = False
    groups = []

    cl_winner = sim.simulate_cup(parsed_data['CL']['team_elo'],
                copy.deepcopy(parsed_data['CL']['schedule']))

    el_winner = sim.simulate_cup(parsed_data['EL']['team_elo'],
                copy.deepcopy(parsed_data['EL']['schedule']))
                
    for i, league in enumerate(leagues):
        table = sim.simulate_league(parsed_data[league]['team_elo'],
                copy.deepcopy(parsed_data[league]['table']),
                parsed_data[league]['schedule'],
                parsed_data[league]['hfa'])

        if cl_winner in table[group_places[league]:]\
        and el_winner in table[group_places[league]:]:
            six_team_exception = True

        if league == 'FRA':
            third_french = table[2]

        if league == 'TUR':
            first_turkish = table[0]

        groups.extend(table[:group_places[league]])

    if cl_winner in groups:
        groups.append(first_turkish)

    else:
        groups.append(cl_winner)

    if el_winner in groups:
        groups.append(third_french)
    
    else:
        groups.append(el_winner)

    return (groups,six_team_exception)


for i in range(N_SIMULATIONS):
    if i % 10000 == 0:
        print('{0}%'.format(i / 10000))

    (groups, six_team_exception) = run_iteration()

    for team in groups:
        if team in full_results.keys():
            full_results[team] += 1

        else:
            full_results[team] = 1

    if six_team_exception:
        six_teams += 1

    
full_results = dict(reversed(sorted(full_results.items(), key=lambda item: item[1])))
print(full_results)
print(six_teams)