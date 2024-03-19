# ==================================================================================================================================
# PURPOSE: RETURN THE BEST CONFIGURATION FOR CHUNKS AND OVERLAP GIVEN THE SAMPLE DATA. 
# ==================================================================================================================================
# DESCRIPTION: THIS SCRIPT IS USED TO TEST THE PERFORMANCE OF CHROMA'S DATA EMBEDDING AND QUERYING CAPABILITIES WITH 
# DIFFERENT CHUNK SIZES AND OVERLAPS. IT LOADS DATA FROM A JSON FILE, EMBEDS IT IN CHUNKS WITH OVERLAP, QUERIES THE DATABASE, 
# AND CALCULATES ACCURACY. THE BEST CONFIGURATION IS REPORTED AT THE END. THE SCRIPT ALSO INCLUDES A FUNCTION TO TEST EMBEDDING 
# A SINGLE TEXT OBJECT. THE SCRIPT IS INTENDED TO BE USED AS A STARTING POINT AND SHOULD BE CUSTOMIZED TO FIT YOUR SPECIFIC USE CASE.
# ==================================================================================================================================
# USAGE: python VDB_Chroma_TestChunks.py
# ==================================================================================================================================
# REQUIRES: !pip install chromadb 
# ==================================================================================================================================

import json
from chromadb.client import Client

def load_data(filename):
  """Loads data from a JSON file."""
  with open(filename, 'r') as f:
    return json.load(f)

def embed_data(client, data, chunk_size, overlap):
  """Embeds data in chunks with overlap, handling potential errors."""
  start = 0
  while start < len(data):
    end = min(start + chunk_size, len(data))
    try:
      # ChromaDB uses insert instead of create_many
      client.embeddings.insert(data[start:end])
    except Exception as e:
      print(f"Error embedding chunk {start}-{end}: {e}")
    start += chunk_size - overlap

def query_and_evaluate(client, questions):
  """Queries the database and calculates accuracy."""
  correct = 0
  total = len(questions)
  for question, answer in questions.items():
    # Implement your specific query logic here with ChromaDB syntax
    results = client.query(query=question)  # Replace with actual query
    # Check if the expected answer is present in the top 5 results (modify as needed)
    if any(answer_item['text'] == answer for answer_item in results[:5]):
      correct += 1
  return correct / total

def test_embedding(client, text_data):
  """Tests embedding a single text object and returns success status."""
  data_object = {"text": text_data}
  try:
    # ChromaDB uses insert instead of create
    client.embeddings.insert(data_object)
    return True
  except Exception as e:
    print(f"Error during test embedding: {e}")
    return False

def main():
  # Load data and questions from your files
  data = load_data("TestData.json")
  questions = load_data("TestQA.json")

  # Connect to ChromaDB
  client = Client("http://localhost:8500")  # Replace with your ChromaDB URL

  # Test embedding a single object
  continue_test = test_embedding(client, data[0]['text'])
  if not continue_test:
    return  # Stop if test embedding failed

  # Define chunk sizes and overlaps
  chunk_sizes = [5, 10, 15, 20, 25, 30, 40, 50, 60, 80, 100, 120, 150, 180, 200, 400, 600, 1000, 5000]
  overlaps = [0, 3, 5, 10, 20, 50, 100, 600]

  # Run tests and store results
  best_accuracy = 0
  best_config = None
  for chunk_size in chunk_sizes:
    for overlap in overlaps:
      if overlap > chunk_size:
        continue  # Skip invalid configurations
      client.clear()  # Clear data before each test (ChromaDB doesn't have built-in clear)
      embed_data(client, data, chunk_size, overlap)
      accuracy = query_and_evaluate(client, questions)
      if accuracy > best_accuracy:
        best_accuracy = accuracy
        best_config = (chunk_size, overlap)
      print(f"Chunk size: {chunk_size}, Overlap: {overlap}, Accuracy: {accuracy:.2f}")

  # Report best configuration
  print(f"\nBest configuration: Chunk size: {best_config[0]}, Overlap: {best_config[1]}, Accuracy: {best_accuracy:.2f}")

if __name__ == "__main__":
  main()
