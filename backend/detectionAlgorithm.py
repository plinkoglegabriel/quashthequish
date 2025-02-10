# Importing libraries
import pandas as pd
from urllib.parse import urlparse
from rapidfuzz import fuzz


# Step 1: Function to check if URL has been previously identified as a malicious URL by Phishing URL dataset (DOI: 10.17632/vfszbj9b36.1)
def datasetCheck(url):
    # Dataset has saved as csv file named 'phishingDataset.csv'
    # Read the csv file
    try:
        df = pd.read_csv('phishingDataset.csv')
        if url in df['url'].values:
            return True
    except FileNotFoundError:
        print("Error: phishingDataset.csv not found!")
        return False
    except Exception as e:
        print("Error reading phishingDataset.csv:", e)
        return False

# Step 2: 1st Heuristic - HTTPS Protocol
# Function to check if URL contains HTTPS protocol at the beginning 
def httpsCheck(url):
    if url.startswith('https://'):
        return True
    else:
        return False


# Function to extract the domain name from the URL
def findDomain(url):
    return urlparse(url).netloc

# Step 3: 2nd Heuristic - URL Length
# Function to check if URL length falls within average URL length
# Heuristic 1: length of the host URL
# URL is a formatted text string utilized by internet users to recognize a network resource on the Internet. URL string consists of three elements such as network protocol, host name and path. For a given URL, the host name is extracted and host name length is examined. For the input data set (1200 phishing URLs and 200 legitimate URLs), domain
# name length is analyzed for phishing and legitimate URLs. The distribution of the domain name length for phished URL is plotted in Fig. 2 and the average length of the domain name (ɭ) in phishing URL is found to be greater than 25 characters. The distribution of the domain name length for legitimate URL is plotted in Fig. 3 and the average length of the domain name (ɭ) in legitimate URL is found to be 20 characters. 
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
        print("🔴 More than one heuristic failed, marking as 'bad'.")
        return {'result': 'bad'}

    # DEBUGGING PRINT STATEMENT
    print("✅ URL is safe.")
    return {'result': 'safe'}
