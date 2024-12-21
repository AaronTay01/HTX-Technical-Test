import csv
import os
import requests

ELASTICSEARCH_URL = "http://localhost:9200"
INDEX_NAME = "cv-transcriptions"

def create_index():
    settings = {
        "settings": {"number_of_shards": 1, "number_of_replicas": 0},
        "mappings": {
            "properties": {
                "generated_text": {"type": "text"},
                "duration": {"type": "float"},
                "age": {"type": "integer"},
                "gender": {"type": "keyword"},
                "accent": {"type": "keyword"},
            }
        },
    }
    response = requests.put(f"{ELASTICSEARCH_URL}/{INDEX_NAME}", json=settings)
    print("Index created:", response.json())

def index_csv_data():
    file_path = r"elastic-backend\cv-valid-dev.csv"
    project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(project_path, file_path)  # Combine project path with the file name
    with open(file_path, mode="r") as file:
        reader = csv.DictReader(file)
        for i, row in enumerate(reader):
            response = requests.post(f"{ELASTICSEARCH_URL}/{INDEX_NAME}/_doc/{i}", json=row)
            print(f"Document {i} indexed:", response.status_code)

if __name__ == "__main__":
    create_index()
    index_csv_data()
    
