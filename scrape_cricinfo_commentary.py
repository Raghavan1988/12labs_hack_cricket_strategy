import requests
import time
import json
import sys

def read_input_file(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        return [line.strip().split(',') for line in lines]

def fetch_data(series_id, match_id, inning_number, over_number):
    url = f"https://hs-consumer-api.espncricinfo.com/v1/pages/match/comments"
    params = {
        "seriesId": series_id,
        "matchId": match_id,
        "inningNumber": inning_number,
        "commentType": "ALL",
        "fromInningOver": over_number
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return e

def write_json_to_file(team, series_id, match_id, data):
    filename = f"{team}_{series_id}_{match_id}.json"
    with open(filename, "w") as file:
        json.dump(data, file)

    with open(team+"matches.txt", "a") as file:
        file.write(filename.strip() + "\n")

def log_error(error_message):
    with open("log.txt", "a") as log_file:
        log_file.write(error_message + "\n")

def main():
    match_series_list = read_input_file(sys.argv[1])
    team = sys.argv[1].split(".")[0]
    data = []
    for series_id, match_id in match_series_list:
        data = []
        for inning in [1, 2]:
            for over in range(1, 51):
                error_count = 0
                while error_count < 3:
                    result = fetch_data(series_id, match_id, inning, over)
                    if isinstance(result, Exception):
                        error_count += 1
                        time.sleep(1)  # Wait for a second before retrying
                    else:
                        data.append(result)
                        print(f"Match ID: {match_id}, Series ID: {series_id}, Inning: {inning}, Over: {over} - Data fetched successfully")

                        break
                if isinstance(result, Exception):
                    log_error(f"Error fetching data for Match ID: {match_id}, Series ID: {series_id}, Inning: {inning}, Over: {over} - {result}")

        write_json_to_file(team, series_id, match_id, data)
        print(f"===============================================Match ID: {match_id}, Series ID: {series_id} - Data written to file===============================================")


if __name__ == "__main__":
    main()
