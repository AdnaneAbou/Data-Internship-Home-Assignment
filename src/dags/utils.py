from src.exception import CustomException
from src.logger import logging

import pandas as pd
import os, json, html 
import pandas as pd
import html
import os
import json

def load_and_clean(path_to_data):
    """
    Load a CSV file from the specified path and perform data cleaning.

    Parameters:
    - path_to_data (str): Path to the CSV file.

    Returns:
    - pd.DataFrame: Cleaned DataFrame.
    """
    # Load CSV data into a DataFrame
    data = pd.read_csv(path_to_data)

    # Drop rows with missing values
    data.dropna(axis=0, inplace=True)

    return data

def text_decoder(text):
    """
    Decode HTML-escaped text and convert it to UTF-8.

    Parameters:
    - text (str): HTML-escaped text.

    Returns:
    - str: Decoded and UTF-8 converted text.
    """
    # Decode HTML-escaped text
    decoded_text = html.unescape(text)

    # Convert the text to UTF-8
    utf8_text = decoded_text.encode('utf-8')

    return utf8_text.decode('utf-8')

def get_data_as_json():
    """
    Load JSON data from text files in a specific directory, decode HTML-escaped text,
    and return the data as a list of dictionaries.

    Returns:
    - list: List of dictionaries containing JSON data.
    """
    # List all files in the 'staging/extracted' directory
    files = os.listdir(os.path.join('staging', 'extracted'))

    # Filter files to include only those with a '.txt' extension
    files = [file for file in files if file.split('.')[1] == 'txt']

    # Initialize an empty list to store JSON data
    data_as_json = []

    # Iterate through each file and load JSON data
    for file in files:
        with open(os.path.join('staging', 'extracted', file), 'r') as f:
            # Load the JSON data from the file
            data = json.load(f)

            # Decode HTML-escaped text in the JSON data
            for key in data.keys():
                if isinstance(data[key], str):
                    data[key] = text_decoder(data[key])

            # Append the modified data to the list
            data_as_json.append(data)

    return data_as_json



def get_values(data_as_json):
    """
    Transform JSON data into a structured format based on a predefined mapping.

    Parameters:
    - data_as_json (list): List of dictionaries containing JSON data.

    Returns:
    - list: Transformed data as a list of dictionaries.
    """
    # Mapping of JSON keys to structured format
    mapping = {
        'job': {
            'date_posted': 'datePosted',
            'description': 'description',
            'employment_type': 'employmentType',
            'industry': 'industry',
            'title': 'title',
        },
        'location': {
            'country': 'jobLocation.address.addressCountry',
            'latitude': 'jobLocation.latitude',
            'locality': 'jobLocation.address.addressLocality',
            'longitude': 'jobLocation.longitude',
            'postal_code': 'jobLocation.address.postalCode',
            'region': 'jobLocation.address.addressRegion',
            'street_address': 'jobLocation.address.streetAddress',
        },
        'company': {
            'link': 'hiringOrganization.sameAs',
            'name': 'hiringOrganization.name',
        },
        'salary': {
            'currency': 'estimatedSalary.currency',
            'max_value': 'estimatedSalary.value.maxValue',
            'min_value': 'estimatedSalary.value.minValue',
            'unit': 'estimatedSalary.value.unitText',
        },
        'education': {
            'required_credential': 'educationRequirements.credentialCategory',
        },
        'experience': {
            'months_of_experience': 'experienceRequirements.monthsOfExperience',
            'seniority_level': "I don't know",
        },
    }

    # Initialize an empty list to store transformed data
    transformed_data = []

    # Iterate through each JSON data entry
    for data in data_as_json:
        # Initialize a template for the structured data
        template = {
            "job": {
                "title": None,
                "industry": None,
                "description": None,
                "employment_type": None,
                "date_posted": None,
            },
            "company": {
                "name": None,
                "link": None,
            },
            "education": {
                "required_credential": None,
            },
            "experience": {
                "months_of_experience": None,
                "seniority_level": None,
            },
            "salary": {
                "currency": None,
                "min_value": None,
                "max_value": None,
                "unit": None,
            },
            "location": {
                "country": None,
                "locality": None,
                "region": None,
                "postal_code": None,
                "street_address": None,
                "latitude": None,
                "longitude": None,
            },
        }

        # Iterate through each section and mapping in the predefined mapping
        for section, section_mapping in mapping.items():
            for key_in_template, key_in_data in section_mapping.items():
                keys = key_in_data.split('.')
                value = data

                # Navigate through nested keys in the JSON data
                for key in keys:
                    if key in value:
                        value = value[key]
                    else:
                        break
                else:
                    # If all keys are found, update the template with the value
                    template[section][key_in_template] = value

        # Append the transformed data to the list
        transformed_data.append(template)

    return transformed_data

def get_transformed_data():
    """
    Retrieve transformed data from JSON files in the staging directory.

    Returns:
    - list: List of dictionaries containing transformed data.
    """
    # Initialize an empty list to store transformed data
    transformed_data = []

    # List files in the 'staging/transformed' directory
    files = os.listdir(os.path.join('staging', 'transformed'))

    # Filter files to include only those with '.json' extension
    files = [file for file in files if file.split('.')[1] == 'json']

    # Iterate through each JSON file
    for file in files:
        # Open the JSON file for reading
        with open(os.path.join('staging', 'transformed', file), 'r') as f:
            # Load the JSON data from the file
            data = json.load(f)

            # Append the loaded data to the list
            transformed_data.append(data)

        # Close the file
        f.close()

    # Return the list of transformed data
    return transformed_data
