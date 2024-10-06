"""
Extract a dataset from a URL
"""

import requests
import os


def extract(
    url="https://raw.githubusercontent.com/fivethirtyeight/data/refs/heads/master/alcohol-consumption/drinks.csv",
    file_path="data/drinks.csv",
):
    """ "Extract a url to a file path"""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    response = requests.get(url)

    # Check if response status is valid
    if response.status_code == 200:
        # Save the content to the specified file path
        with open(file_path, "wb") as f:
            f.write(response.content)
        print(f"File successfully downloaded to {file_path}")
    else:
        print(f"Failed to retrieve the file. Status Code: {response.status_code}")

    return file_path
