import os
import csv
import re
from bs4 import BeautifulSoup
class Parser:
    def __init__(self):
        self.data_file = 'data.csv'
        self.jobs_number = 0
        self.max_pages = 1

    def create_data_file(self):
        """Check if the data file exists, if not create it."""
        if not os.path.exists(self.data_file):
            with open(self.data_file, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Job Title', 'Company','Salary Range', 'Date Posted','Easy Apply','Job Type','Job Description'])
                file.close()

    def parse_page_html(self, html):#POTENTIAL REWRITE TO HAVE THIS PARSE ALL THE JOBS ON A PAGE AND A SECOND FUNCTION TO PARSE THE MAIN CARD CONTENT FOR EACH
        """Parse the HTML content and extract job data."""
        self.jobs_number = 0
        soup = BeautifulSoup(html, 'html.parser')
        html_pretty = soup.prettify() 

        # Save the modified HTML
        with open("parsed_page.html", "w", encoding="utf-8") as f:
            f.write(html_pretty)
        jobs = soup.find_all('li', class_='job-result-card')
        self.jobs_data = []

        # Find the main list container
        job_list_div = soup.find('div', class_='scaffold-layout__list')
        
            
        # Get the <ul> inside it
        ul = job_list_div.find('ul') if job_list_div else print("No job list found.")

        # Iterate through all <li> elements
        if ul:
            job_items = ul.find_all('li', recursive=False)
            self.jobs_number = len(job_items)
            for job in job_items:#title, company, salary range, date posted, easy apply, job type
                raw_text = job.get_text(separator="|").strip().split('|')
                text = [line.strip() for line in raw_text if line.strip()]
                try:
                    title = text[0]
                    company = text[1]
                    #extract job type by getting everything inside the parentheses
                    easy_apply = 'Yes' if 'Easy Apply' in text else 'No'
                    parse_job_type = re.search(r'\((.*?)\)', text[2])
                    job_type = parse_job_type.group(1) if parse_job_type else 'N/A'
                    if '$' in text[4]:
                        salary_range = text[4]
                    else:
                        salary_range = 'N/A'
                    if 'ago' in text[-1]:
                        date_posted = text[-1]
                    else:
                        date_posted = 'N/A'
                    print(f"Title: {title}, Company: {company}, Job Type: {job_type}, Salary Range: {salary_range}, Date Posted: {date_posted}, Easy Apply: {easy_apply}")
                    self.jobs_data.append([title, company, salary_range, date_posted, easy_apply, job_type])
                except IndexError as e:
                    print(f"Error parsing job item: {e}")
                    continue
        else:
            print("No job items found.")
        return self.jobs_data
    def parse_job_card_html(self, html):
        return 
    def save_data(self, jobs_data):
        """Save the extracted job data to a CSV file."""
        with open(self.data_file, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(jobs_data)
            file.close()