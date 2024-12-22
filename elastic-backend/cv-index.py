import csv
import os
import requests

# Define multiple node URLs for Elasticsearch cluster
ELASTICSEARCH_NODES = [
    "http://localhost:9200",  # First node
    "http://localhost:9201",  # Second node (replace with actual second node address)
]

INDEX_NAME = "cv-transcriptions"

def create_index():
    settings = {
        "settings": {"number_of_shards": 1, "number_of_replicas": 0},
        "mappings": {
            "properties": {
                "generated_text": {"type": "text"},
                "duration": {"type": "keyword"},
                "age": {"type": "keyword"},
                "gender": {"type": "keyword"},
                "accent": {"type": "keyword"},
            }
        },
    }

    # Send the index creation request to all nodes
    for node in ELASTICSEARCH_NODES:
        response = requests.put(f"{node}/{INDEX_NAME}", json=settings)
        print(f"Index creation response from {node}: {response.json()}")

def is_valid_age(age_value):
    # Check if age is a valid integer or convertible to an integer
    try:
        # If the age is in words (e.g., "forties"), convert it to the corresponding integer
        age_mapping = {
            "seventies": 70,
            "sixties": 60,
            "fourties": 50,
            "fourties": 40,
            "thirties": 30,
            "twenties": 20,
            "teens": 10
        }
        if age_value.lower() in age_mapping:
            return age_mapping[age_value.lower()]
        # Attempt to convert age to integer
        return int(age_value)
    except ValueError:
        return None  # Return None if it's not a valid integer or recognized word

def index_csv_data():
    file_path = r"elastic-backend\cv-valid-dev.csv"
    project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(project_path, file_path)  # Combine project path with the file name

    with open(file_path, mode="r") as file:
        reader = csv.DictReader(file)
        for i, row in enumerate(reader):
            # Validate and convert the 'age' field if necessary
            # age_value = row.get('age', '').strip()
            # valid_age = is_valid_age(age_value)
            # if valid_age is not None:
            #     row['age'] = valid_age
            # else:
            #     # Set age to -1 or None if invalid
            #     row['age'] = -1  # Or use `None` if you prefer
            
            # Send the data to all nodes
            for node in ELASTICSEARCH_NODES:
                response = requests.post(f"{node}/{INDEX_NAME}/_doc/{i}", json=row)
                if response.status_code == 200 or response.status_code == 201:
                    print(f"Document {i} indexed to {node}: {response.status_code}")
                else:
                    print(f"Document {i} failed on {node} with status code {response.status_code}: {response.text}")

if __name__ == "__main__":
    create_index()
    index_csv_data()
