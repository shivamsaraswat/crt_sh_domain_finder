"""Get domains from crt.sh"""

import sys
import urllib3
import requests
import argparse
import logging
import logging.handlers

# Disable insecure https warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler = logging.handlers.RotatingFileHandler('crt_sh_domains.log', maxBytes=10000000, backupCount=5)
handler.setFormatter(formatter)
logger.addHandler(handler)

# Set up command line arguments
parser = argparse.ArgumentParser(description='Get domains from crt.sh', epilog='Example: python crt_sh_domains.py -d example.com -o domains.txt')
parser.add_argument('-d', '--domain', help='Domain to search for domains', required=True)
parser.add_argument('-o', '--output', help='Output file to write domains to')
args = parser.parse_args()

# Set up variables
domain = args.domain
OUTPUT_FILE = args.output
user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
headers = {"User-Agent": user_agent}

# Set up crt.sh URL
crt_sh_url = 'https://crt.sh/?q=%25.' + domain + '&output=json'

# Get domains from crt.sh
def get_domains() -> list:
    """
    Get domains from crt.sh

    Returns: list of domains"""
    try:
        session = requests.Session()
        response = session.get(crt_sh_url, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            print('Error getting domains from crt.sh, run again')
            logger.error('Error getting domains from crt.sh')
            sys.exit(1)

    except Exception as error:
        print('Error getting domains from crt.sh:', error)
        logger.error('Error getting domains from crt.sh:', error)
        sys.exit(1)

# Write domains to file
def write_domains(domains) -> None:
    """Write domains to file
    domains: list of domains

    Returns: None
    """
    try:
        with open(OUTPUT_FILE, 'w') as output_file:
            for domain in domains:
                output_file.write(domain + '\n')

    except Exception as error:
        print('Error writing domains to file:', error)
        logger.error('Error writing domains to file:', error)
        sys.exit(1)

# Filter domains to remove duplicates and unwanted domains
def filter_domains(domains) -> set:
    """
    Filter domains to remove duplicates and unwanted domains
    domains: list of domains

    Returns: set of domains
    """

    domain_collection = set()
    filters = ['*', '\\', '-', '@']

    for domain in domains:
        domain_split = domain['name_value'].split('\n')

        if len(domain_split) == 1 and all(f not in domain['name_value'] for f in filters):
            domain_collection.add(domain['name_value'])
        else:
            # handle case that have multiple domains
            for domain_2 in domain_split:
                if all(f not in domain_2 for f in filters):
                    domain_collection.add(domain_2)

    return domain_collection

# Main function
def main():
    """Main function"""

    domain_collection = filter_domains(get_domains())
    print(domain_collection)
    print("Total domains: " + str(len(domain_collection)))

    if OUTPUT_FILE:
        print("Writing domains to file: " + OUTPUT_FILE)
        write_domains(domain_collection)

if __name__ == '__main__':
    main()
