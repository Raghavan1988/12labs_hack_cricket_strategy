import os
import json
import sys
from espncricinfo.match import Match
from collections.abc import Mapping, Iterable


def read_input_file(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        return [line.strip() for line in lines]

def load_json_file(file_name):
    try:
        with open(file_name, 'r') as file:
            # Parse the file content as JSON
            data = json.load(file)
            return data
    except json.JSONDecodeError:
        print("Error: The file does not contain valid JSON.")
    except FileNotFoundError:
        print("Error: The file was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def get_schema(obj, path=""):
    """ Recursively finds the schema of the given JSON object. """
    schema = {}

    if isinstance(obj, Mapping):
        for k, v in obj.items():
            new_path = f"{path}/{k}" if path else k
            schema[new_path] = get_schema(v, new_path)
    elif isinstance(obj, Iterable) and not isinstance(obj, str):
        item_schemas = [get_schema(item, path) for item in obj]
        schema[path] = item_schemas[0] if item_schemas else "Empty List"
    else:
        schema[path] = type(obj).__name__

    return schema

def print_schema(json_obj):
    """ Prints the schema of the JSON object. """
    schema = get_schema(json_obj)
    #print(json.dumps(schema, indent=4))

    #for path, data_type in schema.items():
    #    print(f"{path}: {data_type}")

def convert_tuples_to_string(tuples):
    """
    Convert a list of tuples to a concatenated string.
    If a tuple is None, it is replaced with an empty string.

    :param tuples: List of tuples
    :return: Concatenated string
    """
    # Initialize an empty string for the result
    result = ""

    # Iterate over each tuple in the list
    for tup in tuples:
        # If the tuple is None, replace it with an empty string
        if tup is None:
            tup = ("",)

        # Concatenate each element of the tuple to the result string
        for element in tup:
            # If the element is None, replace it with an empty string
            if element is None:
                element = ""
            result += str(element)

    return result

# Example usage
example_tuples = [(None, "Hello", None), ("World",), None, ("!",)]
converted_string = convert_tuples_to_string(example_tuples)
print(converted_string)



if __name__ == "__main__":
    match_series_list = read_input_file(sys.argv[1])
    print(match_series_list)
    player_data = {}
    for match in match_series_list:

        json_data = load_json_file(match)
        ### Resetting balls faced at the beginning of the match
        balls_faced = {}
        for over in json_data:
            comments = over['comments']
            for comment in comments:
                title = comment['title']
                pretext = comment['commentPreTextItems']
                dismissalText = comment["dismissalText"]
                commentTextItems = comment['commentTextItems']
                commentPostTextItems = comment['commentPostTextItems']
                shotType = comment['shotType']

                if shotType is None:
                    shotType = "No Shot"
                else:
                    shotType = "Shot: " + shotType.strip()

                player_name = title.split("to")[1].strip()
                if player_name not in balls_faced:
                    balls_faced[player_name] = 0
                if player_name not in player_data:
                    player_data[player_name] = []
                st_pretext = ""
                st_dismissalText = ""
                st_commentTextItems = ""
                st_commentPostTextItems = ""

                overNumber = comment['overNumber']
                bowler_name = title.split("to")[0].strip()
                runs_scored = comment['batsmanRuns']
                dismissalType = comment['dismissalType']

                wide = comment['wides']
                noballs = comment['noballs']
                byes = comment['byes']
                legbyes = comment['legbyes']


                extras = ""
                if wide > 0 or noballs > 0 or byes > 0 or legbyes > 0:
                    if wide > 0:
                        extras += "Wide: " + str(wide) + " "
                    if noballs > 0:
                        extras += "No Balls: " + str(noballs) + " "
                    if byes > 0:
                        extras += "Byes: " + str(byes) + " "
                    if legbyes > 0:
                        extras += "Legbyes: " + str(legbyes) + " "

                if pretext is not None:
                    st_pretext = json.dumps(pretext)
                    for item in pretext:
                        try:
                            st_pretext += item["html"].strip() + " "
                        except Exception as e:
                            continue
                        ###
                   
                if dismissalText is not None:
                    st_dismissalText = json.dumps(dismissalText)
                    st_dismissalText = "OUT! "+  st_dismissalText.strip()

                if commentTextItems is not None:
                    for item in commentTextItems:
                        print(item)
                        try:
                            st_commentTextItems += item["html"] + " "
                        except Exception as e:
                            continue
                    
                if commentPostTextItems is not None:
                    for item in commentPostTextItems:
                        try:
                            st_commentPostTextItems += item["html"] + " "
                        except:
                            continue
                                                ###
                    print(st_commentPostTextItems)

                
                

                ball_faced = balls_faced[player_name] + 1
                balls_faced[player_name] = ball_faced
                if dismissalType is not None:
                    player_data[player_name].append([ "\nBalls faced: " + str(balls_faced[player_name]).strip(), "Bowler: " + bowler_name, "Over:" + str(overNumber),  shotType.strip(), "run scored: " + str(runs_scored),  st_pretext.strip(), st_dismissalText.strip(), st_commentTextItems.strip(), st_commentPostTextItems.strip(), extras])
                #if (ball_faced == 1):
                #    player_data[player_name].append([ "\n Match: " + match, "Balls faced: " + str(balls_faced[player_name]).strip(), "Bowler: " + bowler_name, "Over:" + str(overNumber),  shotType.strip(), "run scored: " + str(runs_scored),  st_pretext.strip(), st_dismissalText.strip(), st_commentTextItems.strip(), st_commentPostTextItems.strip(), extras])

                #else:
                 #   player_data[player_name].append([ "Balls faced: " + str(balls_faced[player_name]).strip(), "Bowler: " + bowler_name, "Over:" + str(overNumber),  shotType.strip(), "run scored: " + str(runs_scored),  st_pretext.strip(), st_dismissalText.strip(), st_commentTextItems.strip(), st_commentPostTextItems.strip(), extras])


    for player in player_data:
        with open(player +".txt", "w") as w:
            to_write = ""
            for data in player_data[player]:
                for i in range(0,len(data)):
                    if data[i] is not None:
                        content = str(data[i]) 
                        if content.strip() != "":
                            to_write += content.strip() + "\n"

            w.write(to_write.strip())
            print("Written to file: " + player + ".txt")
    

    


