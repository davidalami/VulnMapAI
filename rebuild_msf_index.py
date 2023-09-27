import os
import re
import json

from config import EXPLOITS_DIR, MSF_INDEX_FILE

def build_index(exploits_dir=EXPLOITS_DIR):
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

