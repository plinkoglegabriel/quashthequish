# Old test file moved into new __tests__ directory
# Importing libraries
import pandas as pd
import sys
# Adding the parent directory to the system path so that urlAnalyser function can be imported
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from detectionAlgorithm import urlAnalyser
from concurrent.futures import ThreadPoolExecutor, as_completed

# Load phishing URLs from the CSV file
def loadPhishingURLs(csv_file_path):
    try:
        df = pd.read_csv(csv_file_path)
        urls = df['url'].tolist()
        return urls
    except Exception as e:
        print(f"Error loading phishing URLs from CSV: {e}")
        return []
    
# Function to test the detection algorithm on the phishing dataset
def testDetection(urls):
    numOfDetections = 0

    # Check if the CSV file is empty or not
    total = len(urls)
    if total == 0:
        print("No URLs loaded. Please check the CSV file path or content.")
        return

    # Print statement to make terminal output more readable
    print(f"\nStarting test on {total} phishing URLs...\n")

    # List to store results
    results = []

    # Function to check a single URL against the detection algorithm
    def analyseURL(url):
        result = urlAnalyser(url)
        return (url, result['result'])

    # Number of threads based on my cpu
    maxThreads = 500

    # Using ThreadPoolExecutor to process URLs concurrently (speed up testing)
    with ThreadPoolExecutor(max_workers=maxThreads) as executor:
        # Submit tasks to the executor and the future objects associated with each URL
        futureObjectsOfURL = {executor.submit(analyseURL, url): url for url in urls}
        # Iterate over the completed futures and get the results as they finish
        for future in as_completed(futureObjectsOfURL):
            url = futureObjectsOfURL[future]
            # Try to get the result of the future
            # If the future raises an exception, handle it
            try:
                url, result = future.result()
                print(f"Tested {url}: {result}")

                results.append((url, result))

                if result == 'bad':
                    numOfDetections += 1

            except Exception as e:
                print(f"Error testing URL {url}: {e}")

    # Print the results formatted to be more readable (the accuracy as a percentage)
    print("\n============================")
    print(f"Detection Summary:")
    print(f"Detected: {numOfDetections}/{total} phishing URLs")
    print(f"Accuracy: {numOfDetections / total * 100:.2f}%")
    print("============================\n")


if __name__ == "__main__":
    phishingURLs = loadPhishingURLs('../phishingDataset.csv')
    testDetection(phishingURLs)
