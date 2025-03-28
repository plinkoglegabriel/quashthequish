# Importing libraries
import pandas as pd
from urllib.parse import urlparse
from rapidfuzz import fuzz
from database import createDbConnection
import requests 


# Step 1: Function to check if URL has been previously identified as a malicious URL by Phishing URL dataset (DOI: 10.17632/vfszbj9b36.1)
def datasetCheck(url):
    try:
        # connect to the database
        db = createDbConnection()
        cursor = db.cursor(dictionary=True)
        # attempt to find the URL in the database   
        cursor.execute("USE Quishing")
        cursor.execute("SELECT url FROM links WHERE url = %s AND userId IS NULL", (url,))
        result = cursor.fetchall()
        # close the cursor and database connection
        cursor.close()
        db.close()

        # if the URL is found in the database then True is returned 
        if result:
            print("URL found in the database.")
            return True
        
        # if the URL is not found the phishing.csv is checked (True is returned if found)
        df = pd.read_csv("phishingDataset.csv")
        if url in df["url"].values:
            print("URL found in phishing.csv.")
            return True
        
        # if the URL is not found in either the database or phishing.csv then False is returned
        return False

    except Exception as e:
        print("Error querying phishing URLs:", e)
        return False


# Step 2: 1st Heuristic - HTTPS Protocol
# Function to check if URL contains HTTPS protocol at the beginning 
def httpsCheck(url):
    try:
        # Follow redirects to determine the final URL
        response = requests.head(url, allow_redirects=True, timeout=5)
        final_url = response.url
        # Check if the final URL starts with HTTPS
        if final_url.startswith('https://'):
            print(f"URL redirects to HTTPS: {final_url}")
            return True
        else:
            print(f"URL does not use HTTPS: {final_url}")
            return False
    except requests.RequestException as e:
        print(f"Error checking HTTPS: {e}")
        return False


# Function to extract the domain name from the URL
def findDomain(url):
    return urlparse(url).netloc

# Step 3: 2nd Heuristic - URL Length
# Function to check if URL length falls within average URL length
# Heuristic 1: length of the host URL
# Based on reseach done by Jeeva and Rajsingh, "the average length of the domain name in phishing URL is found to be greater than 25 characters"
# Use https://docs.python.org/3/library/urllib.parse.html to extract the domain name from the URL
def urlDomainLengthCheck(url):
    domain = findDomain(url)
    if len(domain) > 25:
        return True
    else:
        return False

# Step 4: 3rd Heuristic - Impersonated URL domain name (typosquatting)
# Function to find typosquatting attempts in the URL
# csv of most impersonated domain names: mostImpersonatedDomains.csv 
# several sources used including: https://blog.cloudflare.com/50-most-impersonated-brands-protect-phishing/#observations-in-the-wild-most-phished-brands & https://mailsuite.com/blog/the-brands-and-industries-that-phishing-scammers-impersonate-the-most/
def typosquattingCheck(url):
    try:
        domain = findDomain(url)
        df = pd.read_csv('mostImpersonatedDomains.csv')
        for domainName in df.iloc[:, 0]:  # Ensure correct column indexing
            similarity = fuzz.ratio(domain, domainName)
            if similarity >= 80:
                return True
        return False
    except FileNotFoundError:
        print("Error: mostImpersonatedDomains.csv not found!")
        return False
    except Exception as e:
        print("Error reading mostImpersonatedDomains.csv:", e)
        return False

# Function to analyse the URL
def urlAnalyser(url):

    # DEBUGGING PRINT STATEMENT
    print(f"🔍 Analyzing URL: {url}")

    # Variable to store number of heuristics failed
    URLscore = 0
    
    # Calling function to check if URL is in the dataset
    if datasetCheck(url):
        return {'result': 'bad'}
    
    # Calling function to check if URL contains HTTPS
    if not httpsCheck(url):
        return {'result': 'bad'}
    
    # Calling function to check if URL length is within average URL length
    if urlDomainLengthCheck(url):
        URLscore += 1

    # Calling function to check if URL is typosquatting
    if typosquattingCheck(url):
        URLscore += 1

    # If more than 1 of the heuristics failed, return 'bad'
    if URLscore > 1:
        # DEBUGGING PRINT STATEMENT
        print("More than one heuristic failed, marking as 'bad'.")
        return {'result': 'bad'}

    # DEBUGGING PRINT STATEMENT
    print("URL is safe.")
    return {'result': 'safe'}
