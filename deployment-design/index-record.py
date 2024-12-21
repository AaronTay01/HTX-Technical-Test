import csv
import requests
import os

# Elasticsearch URL
ELASTICSEARCH_URL = "http://localhost:9200"
INDEX_NAME = "cs-valid-dev"

# Create Index
# def create_index():
#     index_settings = {
#         "settings": {
#             "number_of_shards": 1,
#             "number_of_replicas": 0
#         },
#         "mappings": {
#             "properties": {
#                 "id": {"type": "integer"},
#                 "name": {"type": "text"},
#                 "value": {"type": "keyword"}
#             }
#         }
#     }
#     response = requests.put(f"{ELASTICSEARCH_URL}/{INDEX_NAME}", json=index_settings)
#     print("Index creation response:", response.json())

# Index CSV Data
def index_csv_data(file_name):
    project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(project_path, file_name)  # Combine project path with the file name
    print(f"Looking for file at: {file_path}")
    
    # Check if file exists
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return
    with open(file_path, mode="r") as csv_file:
        reader = csv.DictReader(csv_file)
        for i, row in enumerate(reader):
            doc_id = row.get("id") or i
            response = requests.post(f"{ELASTICSEARCH_URL}/{INDEX_NAME}/_doc/{doc_id}", json=row)
            print(f"Indexed record {i+1}: {response.status_code}")

if __name__ == "__main__":
    # create_index()
    index_csv_data(r"elastic-backend\cv-valid-dev.csv")
