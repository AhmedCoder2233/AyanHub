import json

FILE_PATH = "data.json"

def load_data():
    with open(FILE_PATH, "r") as f:
        return json.load(f)

def save_data(data):
    with open(FILE_PATH, "w") as f:
        json.dump(data, f, indent=4)
