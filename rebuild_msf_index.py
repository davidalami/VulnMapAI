"""
This module provides functionality to build an index of exploits found in the specified directory.
It will search for Ruby files, parse the exploit's name and description, and save the data to a JSON index file.
"""

import os
import re
import json

from config import EXPLOITS_DIR, MSF_INDEX_FILE


def build_index(exploits_dir=EXPLOITS_DIR):
    """
    Parses and indexes the Name and Description from Ruby (.rb) exploit files located in the specified directory.
    
    Parameters:
        - exploits_dir (str): The path to the directory containing the Ruby exploit files. Defaults to `EXPLOITS_DIR` from config.

    Saves the indexed data as a JSON file (`MSF_INDEX_FILE`).

    The indexing will go through each Ruby file, extract the exploit's name and description, and add this information 
    to the index, along with the relative path to the exploit.
    """
    index = []
    name_pattern = re.compile(r"'Name'\s*=>\s*'([^']*)'", re.IGNORECASE)
    description_pattern = re.compile(r"'Description'\s*=>\s*%q\{([^\}]*)\}", re.IGNORECASE | re.DOTALL)

    for foldername, _, filenames in os.walk(exploits_dir):
        for filename in filenames:
            if filename.endswith('.rb'):
                filepath = os.path.join(foldername, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as file:
                        content = file.read()
                        name_match = name_pattern.search(content)
                        description_match = description_pattern.search(content)
                        if name_match and description_match:
                            index.append({
                                'name': name_match.group(1),
                                'description': description_match.group(1),
                                'path': os.path.relpath(filepath, exploits_dir).replace(os.path.sep, '/')[:-3] #remove extension
                            })
                except Exception as e:
                    print(f"Error reading {filepath}: {e}")

    with open(MSF_INDEX_FILE, 'w') as f:
        json.dump(index, f)


if __name__=='__main__':
    build_index()

