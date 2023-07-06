import sys
import time
import config
import utils
import scrap_functions

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

MAX_PAGE = 103

def scrap(url):
    driver = webdriver.Firefox()
    driver.maximize_window()
    driver.get(url)
    time.sleep(3)
    
    #find regular season stage
    regular_season_stage_element = driver.find_element(By.LINK_TEXT, "Regular Season").click()
    time.sleep(2)
    
    currentPage = 1
        
    #find matches
    while True:
        if currentPage > MAX_PAGE:
            break
        
        matches_element = driver.find_element(By.CLASS_NAME, "matches")
        matches = matches_element.find_elements(By.CLASS_NAME, "items")
        for match in matches:
            match_detail = scrap_functions.extract_overview_info(match, driver)
            match_filename = utils.info_to_filename(match_detail["homeTeam"], match_detail["awayTeam"], match_detail["match_time"])
            print(match_detail)
            
            #save json
            utils.save_data(f"aiscore_scraper/nba_2022_2023_overview_data/{match_filename}.json", match_detail)
        
        #next_pagination
        time.sleep(2)
        WebDriverWait(driver, 120).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn-next"))).click()
        currentPage += 1
        
if __name__ == '__main__':
    url = config.AISCORE_NBA_SUMMARY_URL if sys.argv[1] == "0" else config.AISCORE_WNBA_SUMMARY_URL
    print(f"Start scrapping prebet and score from {url}")
    
    #start scrapping
    scrap(url)