from Interface import Interface
from parser import Parser
from selenium import webdriver
from selenium.webdriver.common.by import By

def main():
    #check if data.csv file exists if not create it
    parser = Parser()
    parser.create_data_file()    
    interface = Interface()
    num_pages = int(input("Enter how many pages do you want to scrape: "))
    for page in range(1, num_pages + 1):
        #call navigate_jobs with the current page number
        interface.navigate_job_page(page)
        #todo:function that iterates over each job on the page and scrapes individual job descriptions   
        html = interface.scrape_page()
        data = parser.parse_page_html(html)
        job_number = parser.jobs_number
        print(f"Found {job_number} jobs on page {page}.")
        # inner for loop for each job on the page
        for job in range(job_number):
            print(f"Scraping page {page}, job {job + 1}...")
            job_details_html = interface.navigate_job_card(job)
            #parse the page html and save the data to data.csv


        
        parser.save_data(data)
        print(f"Page {page} scraped successfully.") 
        
        interface.human_sleep(2, 5)
    interface.close()



if __name__ == "__main__":
    main()