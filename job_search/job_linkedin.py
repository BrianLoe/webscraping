#!/usr/bin/env python
# coding: utf-8

from login import config
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time

def search_job_in_page(job_list, cur_page_num):
    for row in job_list:
        try:
            job_title = row.find('a').contents[0].strip()
            company = row.find('div', {'class':'job-card-container__company-name'}).contents[0].strip()
            print('Job Title: ',job_title)
            print('Company: ', company)
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

def get_job_titles_company(last_page):
    for i in range(1, last_page+1):
        src = driver.page_source

        # Now using beautiful soup
        soup = BeautifulSoup(src, 'html5')

        job_list = soup.find_all('li', {'class':'ember-view'})
        print('Listing all job lists in page ', i)
        next_page_num = search_job_in_page(job_list,i)
        print('\n')
        driver.find_element(By.XPATH, "//button[@aria-label='Page "+str(next_page_num)+"']").click()
    return next_page_num

if __name__ == "__main__":
    params = config()

    # Creating a webdriver instance
    driver = webdriver.Chrome()
    # This instance will be used to log into LinkedIn

    # Opening linkedIn's login page
    driver.get("https://linkedin.com/uas/login")

    # waiting for the page to load
    time.sleep(5)

    # entering username
    username = driver.find_element(By.ID, "username")
    # In case of an error, try changing the element tag used here.

    # Enter Your Email Address
    username.send_keys(params['user'])

    # entering password
    pword = driver.find_element(By.ID, "password")
    # In case of an error, try changing the elementtag used here.

    # Enter Your Password
    pword.send_keys(params['password'])

    # Clicking on the log in button
    # Format (syntax) of writing XPath --> //tagname[@attribute='value']
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    # In case of an error, try changing the XPath used here.
        
    recomend_url = "https://www.linkedin.com/jobs/collections/recommendedlipi=urn%3Ali%3Apage%3Ad_flagship3_job_home%3BobHSV5i9RA6yU%2F%2F5gLL1pQ%3D%3D"
    jobs_url = "https://www.linkedin.com/jobs/"

    driver.get(jobs_url)

    driver.get(recomend_url)
    get_job_titles_company(5)
