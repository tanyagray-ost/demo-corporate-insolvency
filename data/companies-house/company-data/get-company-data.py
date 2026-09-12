import csv
import os 
import time 
import requests
import json
from dotenv import load_dotenv

load_dotenv()



API_KEY = os.environ.get('COMPANIES_HOUSE_API_KEY')
if not API_KEY:
    raise ValueError("COMPANIES_HOUSE_API_KEY is not set in the environment variables")

URL = "https://api.company-information.service.gov.uk/company/{}"

with open('../psc/company-number-list/carillion-psc-company-number-list.txt', 'r') as f:
    company_numbers = [line.strip() for line in f if line.strip()]

with open("ch-companies.csv", "w", newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["company_number", "company_name"])  # Write header row

    for company_number in company_numbers:
        response = requests.get(URL.format(company_number), auth=(API_KEY, ''))
        
        print(URL.format(company_number));
        if response.status_code == 200:
            company_data = response.json()
            writer.writerow([
                company_data.get("company_number", ""),
                company_data.get("company_name", ""),
                
            ])
            csvfile.flush()  # Ensure data is written to the file immediately
        else:
            print(f"Failed to fetch data for company number {company_number}")
        time.sleep(1)  # To avoid hitting the API rate limit
