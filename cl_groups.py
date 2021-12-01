import elo
import itertools
import random
import csv

teams = ['City', 'PSG', 'Leipzig', 'Brugge', 'Atletico', 'Liverpool', 'Porto', 'Milan',
        'Sporting', 'Dortmund', 'Ajax', 'Besiktas', 'Inter', 'Real', 'Shaktar', 'Sheriff',
        'Bayern', 'Barcelona', 'Benfica', 'Dynamo Kyiv', 'Villarreal', 'United', 'Atalanta', 'Young Boys',
        'Lille', 'Sevilla', 'Salzburg', 'Wolfsburg', 'Chelsea', 'Juventus', 'Zenit', 'Malmo']

full_results = {}

for team in teams:
    full_results[team] = {
        '1st': 0,
        '2nd': 0,
        '3rd': 0,
        '4th': 0,
        'Ro16': 0,
        'QF': 0,
        'SF': 0,
        'F': 0,
        'W': 0
    }


for i in range(int(1e6)):
    if i % int(1e5) == 0:
        print(i)

    groups = [
        [
            ('City', 'A', 'ENG', 1997),
            ('PSG', 'A', 'FRA', 1866),
            ('Leipzig', 'A', 'GER', 1815),
            ('Brugge', 'A', 'BEL', 1623)
        ],
        [
            ('Atletico', 'B', 'ESP', 1900),
            ('Liverpool', 'B', 'ENG', 1942),
            ('Porto', 'B', 'POR', 1797),
            ('Milan', 'B', 'ITA', 1805)
        ],
        [
            ('Sporting', 'C', 'POR', 1735),
            ('Dortmund', 'C', 'GER', 1842),
            ('Ajax', 'C', 'NED', 1813),
            ('Besiktas', 'C', 'TUR', 1560)
        ],
        [
            ('Inter', 'D', 'ITA', 1901),
            ('Real', 'D', 'ESP', 1934),
            ('Shaktar', 'D', 'UKR', 1697),
            ('Sheriff', 'D', 'MOL', 1401)
        ],
        [
            ('Bayern', 'E', 'GER', 2000),
            ('Barcelona', 'E', 'ESP', 1912),
            ('Benfica', 'E', 'POR', 1768),
            ('Dynamo Kyiv', 'E', 'UKR', 1668)
        ],
        [
            ('Villarreal', 'F', 'ESP', 1811),
            ('United', 'F', 'ENG', 1923),
            ('Atalanta', 'F', 'ITA', 1840),
            ('Young Boys', 'F', 'SUI', 1692)
        ],
        [
            ('Lille', 'G', 'FRA', 1714),
            ('Sevilla', 'G', 'ESP', 1853),
            ('Salzburg', 'G', 'AUT', 1757),
            ('Wolfsburg', 'G', 'GER', 1779)
        ],
        [
            ('Chelsea', 'H', 'ENG', 1929),
            ('Juventus', 'H', 'ITA', 1850),
            ('Zenit', 'H', 'RUS', 1666),
            ('Malmo', 'H', 'SWE', 1598)
        ],
    ]

    first = []
    second = []

    for group in groups:
        points = [0] * 4
        schedule = itertools.permutations(range(4), 2)

        for game in schedule:
            (w,d,l) = elo.calculate_result_probs(group[game[0]][3], group[game[1]][3], 74.4)
            res = random.choices(
                population=['w', 'd', 'l'],
                weights=[w,d,l],
                k=1
            )[0]
            if res == 'w':
                points[game[0]] += 3
            elif res == 'd':
                points[game[0]] += 1
                points[game[1]] += 1
            else:
                points[game[1]] += 3

        team_points = list(enumerate(points))
        random.shuffle(team_points)
        team_points.sort(key=lambda x: -x[1])

        first.append(group[team_points[0][0]])
        second.append(group[team_points[1][0]])

        full_results[group[team_points[0][0]][0]]['1st'] += 1
        full_results[group[team_points[1][0]][0]]['2nd'] += 1
        full_results[group[team_points[1][0]][0]]['Ro16'] += 1
        full_results[group[team_points[0][0]][0]]['Ro16'] += 1
        full_results[group[team_points[2][0]][0]]['3rd'] += 1
        full_results[group[team_points[3][0]][0]]['4th'] += 1

    ro16 = []

    while len(second) != 0:
        pick1 = random.choice(first)
        pick2 = random.choice(second)

        if pick1[1] == pick2[1] or pick1[2] == pick2[2]:
            pass

        first.remove(pick1)
        second.remove(pick2)
        ro16.append((pick1,pick2))

    advance = []

    for game in ro16:
        (w,_,l) = elo.calculate_result_probs(game[0][3], game[1][3], 0, False)
        res = random.choices(
            population=['w', 'l'],
            weights=[w,l],
            k=1
            )[0]
        if res == 'w':
            advance.append(game[0])
        else:
            advance.append(game[1])

    j = 0

    while len(advance) != 1:
        for team in advance:
            if j == 0:
                full_results[team[0]]['QF'] += 1

            elif j == 1:
                full_results[team[0]]['SF'] += 1

            else:
                full_results[team[0]]['F'] += 1

        new_advance = []

        while len(advance) != 0:
            (w,_,l) = elo.calculate_result_probs(advance[0][3], advance[1][3], 0, False)
            res = random.choices(
                population=['w', 'l'],
                weights=[w,l],
                k=1
                )[0]
            if res == 'w':
                new_advance.append(advance[0])
            else:
                new_advance.append(advance[1])
            
            advance = advance[2:]

        advance = new_advance
        j += 1

    full_results[advance[0][0]]['W'] += 1

for team in full_results.keys():
    for key in full_results[team]:
        full_results[team][key] /= int(1e6)

    with open('res/groups.csv', 'w', newline='') as output_file:
        writer = csv.writer(output_file)
        row_names = ['Team', '1st', '2nd', '3rd', '4th', 'Ro16', 'QF', 'SF', 'F', 'W']

        writer.writerow(row_names)

        for team in full_results.keys():
            row = [team]
            row.extend(full_results[team].values())
            writer.writerow(row)