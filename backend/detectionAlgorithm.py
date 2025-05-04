# Importing libraries
import pandas as pd
from urllib.parse import urlparse
from rapidfuzz import fuzz
from database import createDbConnection
import requests 
import re
import whois
from datetime import datetime
from urllib.parse import parse_qs
import ssl
import socket


# Step 1: Function to check if URL has been previously identified as a malicious URL by Phishing URL dataset (DOI: 10.17632/vfszbj9b36.1)
# def datasetCheck(url):
#     try:
#         # connect to the database
#         db = createDbConnection()
#         cursor = db.cursor(dictionary=True)
#         # attempt to find the URL in the database   
#         cursor.execute("USE Quishing")
#         cursor.execute("SELECT url FROM links WHERE url = %s AND userId IS NULL", (url,))
#         result = cursor.fetchall()
#         # close the cursor and database connection
#         cursor.close()
#         db.close()

#         # if the URL is found in the database then True is returned 
#         if result:
#             print("URL found in the database.")
#             return True
        
#         # if the URL is not found the phishing.csv is checked (True is returned if found)
#         df = pd.read_csv("phishingDataset.csv")
#         if url in df["url"].values:
#             print("URL found in phishing.csv.")
#             return True
        
#         # if the URL is not found in either the database or phishing.csv then False is returned
#         return False

#     except Exception as e:
#         print("Error querying phishing URLs:", e)
#         return False


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
    # extract the domain name from the URL 
    domain = findDomain(url)
    print(f"Extracted domain: {domain}")
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
        # Extract domain name and convert to lowercase
        domain = findDomain(url).lower()
        # csv of known impersonated domains is read and converted to a list of lowercase domain names
        df = pd.read_csv('backend/mostImpersonatedDomains.csv', header=None)
        impersonatedDomains = df[0].str.lower().tolist()
        # Each domain in the list is compared to the domain in the URL and if the similarity is greater than 80% then true is returned
        for knownDomain in impersonatedDomains:
            similarity = fuzz.token_sort_ratio(domain, knownDomain)
            if similarity >= 80 and similarity != 100:
                print(f"Domain {domain} is similar to {knownDomain} (with a {similarity}% match)")
                return True
        return False
    # Error handling
    except FileNotFoundError:
        print("Error: mostImpersonatedDomains.csv not found!")
        return False
    except Exception as e:
        print("Error reading mostImpersonatedDomains.csv:", e)
        return False

# Step 5: 4th Heuristic - URL contains IP address
# Function to check if URL contains an IP address (if so it is a likely indicator of a phishing URL)
def ipAddressCheck(url):
    # Typlical IP address format: xxx.xxx.xxx.xxx
    ipAddressPattern = r'(\d{1,3}\.){3}\d{1,3}'
    # Check if the URL contains an IP address (searching for ipAddressPattern) 
    # True is returned if the pattern is found
    if re.search(ipAddressPattern, url):
        print("IP address detected in URL.")
        return True
    return False

# Step 6: 5th Heuristic - URL contains too many dots
# Function to check if URL contains too many dots (more than 3 dots are often present in phishing URL)
def dotsCheck(url):
    domain = findDomain(url)
    count = domain.count('.')
    print(f"Domain has {count} dots.")
    return count > 3  

# Step 7: 6th Heuristic - URL contains an @ symbol
# Function to check if URL contains an @ symbol
def atSymbolCheck(url):
    if '@' in url:
        print("Found '@' symbol in URL.")
        return True
    return False

# Step 8: New Heuristic - Number of slashes in URL
# Function to check if URL contains too many slashes (more than 4 slashes are often present in phishing URL)
def slashesCheck(url):
    slash_count = url.count('/')
    print(f"URL has {slash_count} slashes.")
    return slash_count > 4

# Step 9: New Heuristic - Unicode characters in URL
# Function to check if URL contains unicode characters (non-ASCII characters) 
# unicode characters are often used in phishing URLs to obfuscate it making the user think it is a legitimate URL
def unicodeCharactersCheck(url):
    try:
        # Attempt to encode the URL as ASCII and if it fails then unicode characters are present and true is returned
        url.encode('utf-8').decode('ascii')
    except UnicodeDecodeError:
        print("Unicode characters detected in URL.")
        return True
    return False

# Step 10: New Heuristic - Subdomains
# Function to check if URL contains subdomains (more than 2 subdomains are often present in phishing URL)
def subdomainCountCheck(url):
    domain = findDomain(url)
    count = domain.count('.')
    print(f"Domain has {count} subdomains.")
    return count > 3

# Step 11: New Heuristic - Hyphen in the domain name
# Function to check if URL contains hyphen in the domain name (more than 1 hyphen is often present in phishing URL)
def hyphenInDomainCheck(url):
    domain = findDomain(url)
    if domain.count('-') > 1:
        print(f"Hyphen detected in the domain: {domain}")
        return True
    return False

# Step 12: New Heuristic - Suspicious keywords in the path portion of the URL can indicate phishing 
# Especially considering this is for quishing, a first scan for a non malicious URL would usually not require a login and/or payment)
def suspiciousWordsCheck(url):
    path = urlparse(url).path
    keywords = ['login', 'paypal', 'account', 'confirm', 'payment', 'id', 'verify', 'suspend', 'reset', 'password']
    if any(keyword in path.lower() for keyword in keywords):
        print(f"Suspicious keyword in path: {path}")
        return True
    return False

# Step 13: New Heuristic - Length of the URL
# Function to check if URL is too long (phishing URLs usually contain more a large number of characters)
def urlLengthCheck(url):
    if len(url) > 75:
        print(f"URL is longer than 75 characters: {url}")
        return True
    return False

# Step 14: New Heuristic - Top Level Domain Check
# Function to check if the URL has a valid top-level domain (TLD) e.g. .com, .net, .org, etc.
def topLevelDomainCheck(url):
    domain = findDomain(url)
    tlds = ['com', 'net', 'org', 'gov', 'edu', 'uk', 'eu', 'ca', 'us', 'au', 'de', 'fr', 'it', 'jp']
    domainParts = domain.split('.')
    if len(domainParts) > 1:
        lastTwoParts = '.'.join(domainParts[-2:])
    if lastTwoParts in tlds:
        return False
    if domainParts[-1] in tlds:
        return False
    print(f"Invalid top-level domain: {domain}")
    return True

# Step 15: New Heuristic - Check for redirects
# Function to check if the URL has too many redirects (more than 3 redirects are often present in phishing URL)
def redirectCheck(url):
    try:
        response = requests.get(url, allow_redirects=True, timeout=5)
        if len(response.history) > 3:
            print(f"URL has {len(response.history)} redirects.")
            return True
        return False
    except requests.RequestException as e:
        print(f"Error checking redirects: {e}")
        return False

# Step 16: New Heuristic - Check the url's path length
# Function to check the length of the url's path is not more than 50 as long paths like this can be strong indicators that the url is malicious
def pathLengthCheck(url):
    path = urlparse(url).path
    return len(path) > 50 

# Step 17: New Heuristic - Check the age of the domain
# Function to check if the domain is new (typical indicator)
def domainAgeCheck(url):
    # Try to get domain's creation date and then age and if domain is younger than 180 days (6 months), True is returned (as it is an indicator of phishing)
    try:
        domain = findDomain(url)
        domainInfo = whois.whois(domain)
        if isinstance(creationDate, list):
            creationDate = domainInfo.creation_date[0] if isinstance(domainInfo.creation_date, list) else domainInfo.creation_date
        domainAge = (datetime.now() - creationDate).days
        if domainAge < 180: 
            return True
        return False
    except Exception as e:
        print(f"Error checking domain age: {e}")
    return False

# Step 18: New Heuristic - Check if path contains suspicious port numbers 
# Function to check for suspicious port numbers (indicator of phishing)
def portNumberCheck(url):
    port = urlparse(url).port
    if port and port not in [80, 443]:  
        return True
    return False

# Step 19: New Heuristic - Check SSL certificate
# Function to check if the URL has a valid SSL certificate
def sslCheck(url):
    try:
        host = findDomain(url)
        sslContext = ssl.create_default_context()
        conn = sslContext.wrap_socket(socket.socket(socket.AF_INET), server_hostname=host)
        conn.connect((host, 443))
        cert = conn.getpeercert()
        if cert:
            return True
    except ssl.SSLError as e:
        print(f"SSL Error: {e}")
    return False

# Function to analyse the URL
def urlAnalyser(url):

    # DEBUGGING PRINT STATEMENT
    print(f"🔍 Analyzing URL: {url}")

    # Variable to store number of heuristics failed
    URLscore = 0
    
    # Calling function to check if URL is in the dataset
    # if datasetCheck(url):
    #     return {'result': 'bad'}
    
    # Calling function to check if URL contains HTTPS
    if not httpsCheck(url):
        return {'result': 'bad'}
    
    # Calling function to check if URL length is within average URL length
    if urlDomainLengthCheck(url):
        URLscore += 1

    # Calling function to check if URL is typosquatting
    if typosquattingCheck(url):
        URLscore += 1
    
    # Calling function to check if URL contains an IP address
    if ipAddressCheck(url):
        URLscore += 1
    
    # Calling function to check if URL contains too many dots
    if dotsCheck(url):
        URLscore += 1
    
    # Calling function to check if URL contains an @ symbol
    if atSymbolCheck(url):
        URLscore += 1
    
    # Calling function to check if URL contains too many slashes
    if slashesCheck(url):
        URLscore += 1
    
    # Calling function to check if URL contains unicode characters
    if unicodeCharactersCheck(url):
        URLscore += 1
    
    # Calling function to check if URL contains subdomains
    if subdomainCountCheck(url):
        URLscore += 1
    
    # Calling function to check if URL contains hyphen in hostname
    if hyphenInDomainCheck(url):
        URLscore += 1
    
    # Calling function to check if URL contains keywords in path
    if suspiciousWordsCheck(url):
        URLscore += 1
    
    # Calling function to check if URL is too long
    if urlLengthCheck(url):
        URLscore += 1

    # Calling function to check if URL has a valid top-level domain
    if topLevelDomainCheck(url):
        URLscore += 1
    
    # Calling function to check if URL has too many redirects
    if redirectCheck(url):
        URLscore += 1
    
    # Calling function to check if URL has a long path
    if pathLengthCheck(url):
        URLscore += 1
    
    # Calling function to check if URL has a new domain
    if domainAgeCheck(url):
        URLscore += 1
    
    # Calling function to check if URL has suspicious port numbers
    if portNumberCheck(url):
        URLscore += 1
    
    # Calling function to check if URL has a valid SSL certificate
    if not sslCheck(url):
        URLscore += 1

    # If more than 1 of the heuristics failed, return 'bad'
    if URLscore > 1:
        # DEBUGGING PRINT STATEMENT
        print("More than one heuristic failed, marking as 'bad'.")
        return {'result': 'bad'}

    # DEBUGGING PRINT STATEMENT
    print("URL is safe.")
    return {'result': 'safe'}
