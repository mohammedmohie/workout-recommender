"""
Utility functions for the Workout Recommender System
"""

import json
import os
from typing import Dict, Any, List, Union


def load_json_data(file_path: str) -> Union[Dict, List]:
    """Load JSON data from file with multiple fallback strategies"""
    try:
        # First try: Standard JSON loading
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read().strip()
            try:
                return json.loads(content)
            except json.JSONDecodeError as e:
                # If the main content has extra data, try cleaning it
                if "Extra data" in str(e):
                    # Find the last valid JSON bracket/brace
                    last_brace = content.rstrip().rfind(']')
                    if last_brace == -1:
                        last_brace = content.rstrip().rfind('}')
                    if last_brace != -1:
                        content = content[:last_brace+1]
                        return json.loads(content)
                
                # If that didn't work, try line-by-line loading
                file.seek(0)
                data = []
                for line in file:
                    line = line.strip()
                    if line and not line.startswith('//') and not line.startswith('#'):
                        try:
                            data.append(json.loads(line))
                        except json.JSONDecodeError:
                            continue
                if data:
                    return data
                raise

    except Exception as e:
        print(f"Error loading JSON from {os.path.basename(file_path)}: {str(e)}")
        # Return empty structure based on file content hint
        with open(file_path, 'r', encoding='utf-8') as file:
            first_char = file.read(1).strip()
            return [] if first_char == '[' else {}


def save_json_data(data: Union[Dict, List], file_path: str) -> None:
    """Save data to a JSON file"""
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=2)

def calculate_similarity(list1: list, list2: list) -> float:
    """Calculate similarity between two lists"""
    if not list1 or not list2:
        return 0.0

    set1, set2 = set(list1), set(list2)
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))

    return intersection / union if union > 0 else 0.0
