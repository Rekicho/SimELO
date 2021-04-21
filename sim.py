import random
import time
import elo

from functools import cmp_to_key

random.seed(time.time())

def simulate_league(team_elo, table, schedule, hfa, h2h=None, temp_h2h=None):
    res = []

    for game in schedule:
        ordered = game['home'] + game['away'] if game['home'] <= game['away'] else game['away'] + game['home']


        (w,d,l) = elo.calculate_result_probs(team_elo[game['home']], team_elo[game['away']], HFA=hfa)
        result = random.choices(
            population=['w', 'd', 'l'],
            weights=[w,d,l],
            k=1
        )[0]
        if result == 'w':
            temp_h2h[ordered][game['home'] + '_points'] += 3
            table[game['home']] += 3
        elif result == 'd':
            temp_h2h[ordered][game['home'] + '_points'] += 1
            temp_h2h[ordered][game['away'] + '_points'] += 1
            table[game['home']] += 1
            table[game['away']] += 1
        else:
            temp_h2h[ordered][game['away'] + '_points'] += 3
            table[game['away']] += 3

    table = list(table.items())
    random.shuffle(table)

    def sort_h2h(teamA, teamB):
        if teamA[1] > teamB[1]:
            return -1

        if teamA[1] < teamB[1]:
            return 1

        ordered = teamA[0] + teamB[0] if teamA[0] <= teamB[0] else teamB[0] + teamA[0]

        if ordered in h2h:
            if h2h[ordered] == teamA[0]:
                return -1

            if h2h[ordered] == teamB[0]:
                return 1

        if ordered in temp_h2h:
            if temp_h2h[ordered][teamA[0] + '_points'] > temp_h2h[ordered][teamB[0] + '_points']:
                return -1

            if temp_h2h[ordered][teamA[0] + '_points'] < temp_h2h[ordered][teamB[0] + '_points']:
                return 1

        return 0

    table = list(sorted(table, key=cmp_to_key(sort_h2h)))

    for team in table:
        res.append(team[0])

    return res

def simulate_cup(team_elo, schedule):
    while(len(schedule) > 0):
        winners = []

        for game in schedule:
            (w,d,l) = elo.calculate_result_probs(team_elo[game['home']], team_elo[game['away']], draw_possible=False)
            result = random.choices(
                population=['w', 'l'],
                weights=[w,l],
                k=1
            )[0]
            if result == 'w':
                winners.append(game['home'])
            else:
                winners.append(game['away'])

        random.shuffle(winners)
        schedule = []

        for i, team in enumerate(winners):
            if i % 2 == 1:
                schedule.append({
                    'home': winners[i-1],
                    'away': winners[i]
                })

    return winners[0]