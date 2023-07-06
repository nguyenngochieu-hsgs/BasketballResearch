import json

def info_to_filename(home_team, away_team, match_time):
    _, month_date, year = match_time.split(',')
    year = year.strip()
    month, date = month_date.strip().split(' ')
    return f"{home_team}_{away_team}_{month}_{date}_{year}"

def save_data(loc, data):
    with open(loc, "w") as outfile:
        json.dump(data, outfile)