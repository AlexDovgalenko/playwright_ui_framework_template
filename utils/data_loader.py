import csv
import json
from typing import Any, Dict, List, Union

import yaml

from utils.constants import DATA_DIR


def load_json(filename: str) -> Union[Dict[str, Any], List[Any]]:
    """Load data from a JSON file.

    Args:
        filename: Name of the JSON file in the test_data directory

    Returns:
        Loaded JSON data as dict or list
    """
    filepath = DATA_DIR / filename
    if not filepath.exists():
        raise FileNotFoundError(f"Test data file not found: {filepath}")

    with open(file=filepath, mode="r", encoding="utf-8") as file:
        return json.load(fp=file)


def load_yaml(filename: str) -> Union[Dict[str, Any], List[Any]]:
    """Load data from a YAML file.

    Args:
        filename: Name of the YAML file in the test_data directory

    Returns:
        Loaded YAML data as dict or list
    """
    filepath = DATA_DIR / filename
    if not filepath.exists():
        raise FileNotFoundError(f"Test data file not found: {filepath}")

    with open(file=filepath, mode="r", encoding="utf-8") as file:
        return yaml.safe_load(stream=file)


def load_csv(
    filename: str, as_dict: bool = True
) -> List[Union[Dict[str, str], List[str]]]:
    """Load data from a CSV file.

    Args:
        filename: Name of the CSV file in the test_data directory
        as_dict: If True, returns each row as a dictionary with column headers as keys
                 If False, returns each row as a list of values

    Returns:
        List of rows from the CSV file
    """
    filepath = DATA_DIR / filename
    if not filepath.exists():
        raise FileNotFoundError(f"Test data file not found: {filepath}")

    with open(file=filepath, mode="r", encoding="utf-8", newline="") as file:
        if as_dict:
            reader = csv.DictReader(file)
            return list(reader)
        else:
            reader = csv.reader(csvfile=file)
            return list(reader)
