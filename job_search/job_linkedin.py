#!/usr/bin/env python
# coding: utf-8

from login import config
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import sys
import openai
import pandas as pd
params = config()
openai.api_key = params['api_key']

def search_job_in_page(job_list, cur_page_num, job_dict):
    job_name = job_list.find_all('li', {'class':'ember-view'})
    system_msg="You are a career coach who understands job requirements"
    user_msg="List 5 key skills to be a great fit with this job description: "
    for row in job_name:
        try:
            job_title = row.find('a').contents[0].strip()
            company = row.find('div', {'class':'job-card-container__company-name'}).contents[0].strip()
            rowid = row.get('id')
            print('Clicking job card ...')
            driver.find_element(By.XPATH, "//li[@id='"+rowid+"']").click()
            time.sleep(5)
            src = driver.page_source
            soup = BeautifulSoup(src, 'html5lib')
            job_card = soup.find('div', {'class':'scaffold-layout__list-detail-inner'})
            print('Extracting level ...')
            level = job_card.find('li', {'class':'jobs-unified-top-card__job-insight'}).find('span').contents[2]
            print('Extracting location ...')
            location = job_card.find('span', {'class':'jobs-unified-top-card__bullet'}).contents[0].strip()
            print('Extracting time_posted ...')
            time_posted = job_card.find('span', {'class':'jobs-unified-top-card__posted-date'}).contents[0].strip()
            print('Extracting job description ...')
            text = job_card.find('div', {'class':'jobs-description__content jobs-description-content'}).find('span').getText().strip()
            user_msg+=text
            print('Converting job description ...')
            response = openai.ChatCompletion.create(
                                                    model="gpt-3.5-turbo",
                                                    messages=[{"role": "system", "content": system_msg},
                                                              {"role": "user", "content": user_msg}]
                                                   )
            response = response["choices"][0]["message"]["content"]
            # print('Job Title: ',job_title)
            # print('Company: ', company)
            # print('Location: ', location)
            # print('Level: ',level)
            # print('Time posted: ', time_posted)
            # print('5 Key Skills Needed according to GPT: ')
            # print(text)
#             print()
            job_dict['job_title'].append(job_title)
            job_dict['company'].append(company)
            job_dict['location'].append(location)
            job_dict['level'].append(level)
            job_dict['time_posted'].append(time_posted)
            job_dict['skills'].append(response)
            # job_dict['skills'].append(text)
        except: 
            try:
                p_num = int(row.find('button').attrs.get('aria-label')[-1:])
                if cur_page_num<p_num:
                    cur_page_num=p_num
                    break
                elif cur_page_num>=p_num:
                    continue
            except:
                continue
    return cur_page_num

def get_job_titles_company(last_page, job_dict):
    for i in range(1, last_page+1):
        src = driver.page_source

        # Now using beautiful soup
        soup = BeautifulSoup(src, 'html5lib')

        job_list = soup.find('div', {'class':'scaffold-layout__list-detail-inner'})
        # print('||Listing all job lists in page ', str(i)+'||')
        next_page_num = search_job_in_page(job_list,i, job_dict)
        # print()
        driver.find_element(By.XPATH, "//button[@aria-label='Page "+str(next_page_num)+"']").click()
        time.sleep(6)
    return next_page_num

def input_rec_url():
    recomend_url = input("Please enter linkedin job search result page link: ")
    if not recomend_url.startswith('https://www.linkedin.com'):
        print("Job site is invalid")
        ans = input("would you like to use existing link? [y/n]")
        if ans.lower()=='y':
            recomend_url = "https://www.linkedin.com/jobs/collections/recommended?lipi=urn%3Ali%3Apage%3Ad_flagship3_job_home%3BobHSV5i9RA6yU%2F%2F5gLL1pQ%3D%3D"
        else:
            print("Exiting...")
            sys.exit(1)
    return recomend_url

def input_num_pages():
    num_pages = input("Please enter the number of pages you would like to search (1-9): ")
    if (not num_pages.isdigit()):
        ans = input("invalid number, would you like to try again? [y/n] ")
        error_handler(ans)
    else:
        print("Starting program ...")
        return num_pages
    
def error_handler(input_arg):
    if input_arg=='n':
        print("Exiting ...")
        sys.exit(1)
    else:
        input_num_pages()

if __name__ == "__main__":
    recomend_url = input_rec_url()
            
    num_pages = int(input_num_pages())
    
    print("Creating webdriver instance ...")
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=options)
    # This instance will be used to log into LinkedIn
    
    print("Opening linkedIn's login page ...")
    driver.get("https://linkedin.com/uas/login")

    print("waiting for the page to load ...")
    time.sleep(5)

    print("entering username ...")
    username = driver.find_element(By.ID, "username")
    # In case of an error, try changing the element tag used here.

    # Enter Your Email Address
    username.send_keys(params['user'])

    print("entering password ...")
    pword = driver.find_element(By.ID, "password")
    # In case of an error, try changing the element Wtag used here.

    # Enter Your Password
    pword.send_keys(params['password'])

    print("Clicking on the log in button ...")
    # Format (syntax) of writing XPath --> //tagname[@attribute='value']
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    # In case of an error, try changing the XPath used here.
    print("waiting for the page to load (please verify the human verification if exist) ...")
    time.sleep(15)
    
    print("Getting the recommended jobs page ...")
    driver.get(recomend_url)
    time.sleep(5)
    
    print("Getting the job lists ...")
    job_dict = {}
    job_dict['job_title'] = []
    job_dict['company'] = []
    job_dict['location'] = []
    job_dict['level'] = []
    job_dict['time_posted'] = []
    job_dict['skills'] = []
    get_job_titles_company(num_pages, job_dict)
    df = pd.DataFrame(job_dict)
    print("Creating text file ...")
    df.to_csv('result.txt', index=False)
    print("Text file created")
