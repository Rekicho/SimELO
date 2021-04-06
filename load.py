import json

def load_leagues(leagues):
    parsed_data = {}

    for league in leagues:
        with open('data/{league}.json'.format(league=league)) as json_file:
            data = json.load(json_file)
            hfa = data['HFA']
            schedule = data['schedule']
            table = {}
            team_elo = {}

            for team in data['teams']:
                table[team['name']] = team['points']
                team_elo[team['name']] = team['elo']

            parsed_data[league] = {
                'team_elo': team_elo,
                'table': table,
                'schedule': schedule,
                'hfa': hfa,
            }

            json_file.close()

    return parsed_data

def load_cups(cups):
    parsed_data = {}

    for cup in cups:
        with open('data/{cup}.json'.format(cup=cup)) as json_file:
            data = json.load(json_file)
            schedule = data['schedule']
            team_elo = {}

            for team in data['teams']:
                team_elo[team['name']] = team['elo']

            parsed_data[cup] = {
                'team_elo': team_elo,
                'schedule': schedule,
            }

            json_file.close()

    return parsed_data