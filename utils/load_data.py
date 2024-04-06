import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import statsapi


# create df function
def create_df(teams, year='2021'):
    """Take all the teams and get all games in that season then concat into a df"""
    schedules = {}
    games = []

    for t in teams:
        schedules[t['name']] = statsapi.schedule(team=t['id'], start_date='01/01/{}'.format(year),
                                                 end_date='12/31/{}'.format(year))

    for t in teams:
        for i in schedules[t['name']]:
            games.append(i)

    games_df = pd.DataFrame(games)
    drop_cols = ['summary', 'national_broadcasts', 'venue_name', 'home_pitcher_note', 'away_pitcher_note',
                 'game_datetime', 'venue_id', 'inning_state']

    games_df = games_df.drop(drop_cols, axis=1)
    games_df = games_df[games_df['game_type'] != 'S'].copy()

    return games_df


# additional
def get_player_stats(df, previous=False):
    """Get some stats of interest. this is not an efficient function. Brute force looping. Refactor later"""

    if previous:
        for g, i, a, h in zip(df['game_id'], df.index,df['away_id'],df['home_id']):
            away = statsapi.last_game(a)
            home = statsapi.last_game(h)

            data_away = statsapi.boxscore_data(away)
            data_home = statsapi.boxscore_data(home)

            if data_away['away']['team']['id'] == a:
                awayBatters = data_away['awayBatters'][1:10]
                awayPitchers = data_away['awayPitchers'][1:5]
            else:
                awayBatters = data_away['homeBatters'][1:10]
                awayPitchers = data_away['homePitchers'][1:5]

            if data_home['home']['team']['id'] == h:
                homeBatters = data_home['homeBatters'][1:10]
                homePitchers = data_home['homePitchers'][1:5]
            else:
                homeBatters = data_home['awayBatters'][1:10]
                homePitchers = data_home['awayPitchers'][1:5]


            count = 1
            for b in awayBatters:
                df.loc[i, f'away_batter_{count}'] = b['obp']
                count += 1
            count = 1
            for b in homeBatters:
                df.loc[i, f'home_batter_{count}'] = b['obp']
                count += 1

            count = 1
            for p in awayPitchers:
                df.loc[i, f'away_pitcher_{count}'] = p['era']
                count += 1

            count = 1
            for p in homePitchers:
                df.loc[i, 'home_pitcher_{}'.format(count)] = p['era']
                count += 1
        return df

    for g, i in zip(df['game_id'], df.index):
        data = statsapi.boxscore_data(g)
        awayBatters = data['awayBatters'][1:10]
        homeBatters = data['homeBatters'][1:10]
        awayPitchers = data['awayPitchers'][1:5]
        homePitchers = data['homePitchers'][1:5]

        count = 1
        for b in awayBatters:
            df.loc[i, f'away_batter_{count}'] = b['obp']
            count += 1
        count = 1
        for b in homeBatters:
            df.loc[i, f'home_batter_{count}'] = b['obp']
            count += 1

        count = 1
        for p in awayPitchers:
            df.loc[i, f'away_pitcher_{count}'] = p['era']
            count += 1

        count = 1
        for p in homePitchers:
            df.loc[i, 'home_pitcher_{}'.format(count)] = p['era']
            count += 1

    return df

