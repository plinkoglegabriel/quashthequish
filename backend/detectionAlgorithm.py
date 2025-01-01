# Function to analyse the URL
def urlAnalyser(url):

    # Variable to store the URL score
    URLscore = 0
    
     # Step 1: Function to check if URL has been previously identified as a malicious URL by Phishing URL dataset (DOI: 10.17632/vfszbj9b36.1)
    def datasetCheck(url):
        # Dataset has saved as csv file named 'phishingDataset.csv'
        # Import pandas library to read the csv file
        import pandas as pd
        # Read the csv file
        df = pd.read_csv('phishingDataset.csv')
        # Check if the url is in the dataset
        if url in df['url'].values:
            return True
        else:
            return False
    
    if datasetCheck(url):
        return {'result': 'Bad URL'}
    
    # Step 2: 1st Heuristic - HTTPS Protocol
    # Function to check if URL contains HTTPS protocol at the beginning 
    def httpsCheck(url):
        if url.startswith('https://'):
            return True
        else:
            return False
    
    if not httpsCheck(url):
        return {'result': 'Bad URL'}
    
    # Step 3: 2nd Heuristic - URL Length
    # Function to check if URL length falls within average URL length
    # Heuristic 1: length of the host URL
    # URL is a formatted text string utilized by internet users to recognize a network resource on the Internet. URL string consists of three elements such as network protocol, host name and path. For a given URL, the host name is extracted and host name length is examined. For the input data set (1200 phishing URLs and 200 legitimate URLs), domain
    # name length is analyzed for phishing and legitimate URLs. The distribution of the domain name length for phished URL is plotted in Fig. 2 and the average length of the domain name (ɭ) in phishing URL is found to be greater than 25 characters. The distribution of the domain name length for legitimate URL is plotted in Fig. 3 and the average length of the domain name (ɭ) in legitimate URL is found to be 20 characters. 
    # Use https://docs.python.org/3/library/urllib.parse.html to extract the domain name from the URL
    def urlDomainLengthCheck(url):
        from urllib.parse import urlparse
        domain = urlparse(url).netloc
        if len(domain) > 25:
            return False
        else:
            return True
    
    if not urlDomainLengthCheck(url):
        URLscore += 1  
        

    
        
