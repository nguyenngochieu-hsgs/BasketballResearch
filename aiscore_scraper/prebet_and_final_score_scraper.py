import sys
import time
import config
import scrap_functions

from selenium import webdriver
from selenium.webdriver.common.by import By

def scrap(url):
    driver = webdriver.Firefox()
    driver.get(url)
    time.sleep(3)
    
    #find regular season stage
    regular_season_stage_element = driver.find_element(By.LINK_TEXT, "Regular Season").click()
    time.sleep(1)
    
    #find matches
    matches_element = driver.find_element(By.CLASS_NAME, "matches")
    matches = matches_element.find_elements(By.CLASS_NAME, "items")
    for match in matches:
        match_detail = scrap_functions.extract_overview_info(match, driver)
        print(match_detail)
        break

if __name__ == '__main__':
    url = config.AISCORE_NBA_SUMMARY_URL if sys.argv[1] == "0" else config.AISCORE_WNBA_SUMMARY_URL
    print(f"Start scrapping prebet and score from {url}")
    
    #start scrapping
    scrap(url)