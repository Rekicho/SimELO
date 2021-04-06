import random
import time
import elo

random.seed(time.time())

def simulate_league(team_elo, table, schedule, hfa):
    res = []

    for game in schedule:
        (w,d,l) = elo.calculate_result_probs(team_elo[game['home']], team_elo[game['away']], HFA=hfa)
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