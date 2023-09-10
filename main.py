import pandas as pd


def read_season_grid():
    season_grid = pd.read_csv("season23.csv")
    season = {}

    # create dict with matchdays
    teams = season_grid["TEAM"].values
    weeks = season_grid.columns[1:]
    for week in weeks:
        week_opponents = season_grid[week].values
        week_matchups = [f"{teams[i].upper()}{week_opponents[i].upper()}" for i in range(len(teams))]
        away_perspective_matchups = [matchup.replace("@", " @ ") for matchup in week_matchups if "@" in matchup]
        season[week] = away_perspective_matchups
    return season


def print_week_matchups(season, week):
    print(week)
    print("[Name]")
    for matchup in season[week]:
        print(f"{matchup}: ")


def read_predictions_from_file(week, name):
    predictions = {}

    with open("predictions23.txt", "r") as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        line = line.replace("\n", "")
        # search for name and week
        if line == week and lines[i + 1].replace("\n", "") == name:

            # get predictions for matchups
            j = 1
            while i + j < len(lines) - 1 and "@" in lines[i + 1 + j]:
                matchup = lines[i + 1 + j].replace("\n", "").split(":")[0]
                prediction = lines[i + 1 + j].replace("\n", "").split(":")[1][1:]
                predictions[matchup] = prediction
                j += 1
    return predictions


def read_results_from_file(week):
    results = {}

    with open("results23.txt", "r") as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        line = line.replace("\n", "")
        # search for name and week
        if line == week:
            # get predictions for matchups
            j = 1
            while i + j < len(lines) and "@" in lines[i + j]:
                matchup = lines[i + j].replace("\n", "").split(":")[0]
                result = lines[i + j].replace("\n", "").split(":")[1][1:]
                results[matchup] = result
                j += 1
            break
    return results


def get_points(results, predictions):
    points = 0
    for matchup in results:
        if results[matchup] == predictions[matchup]:
            points += 1
    return points


# run script
season = read_season_grid()
curr_week = "W01"
print_week_matchups(season, curr_week)
week_results = read_results_from_file(curr_week)
player_points = {}
player_predictions = {}
for player in ["Luke"]:
    player_predictions[player] = read_predictions_from_file(curr_week, player)
    player_points[player] = get_points(week_results, player_predictions[player])
