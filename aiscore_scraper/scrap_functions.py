import time

from selenium.webdriver.common.by import By


def extract_overview_info(match_element, driver):
    match_detail = {}
    teams_element = match_element.find_element(By.CLASS_NAME, "team").find_elements(By.CLASS_NAME, "flex")
    for team_element in teams_element:
        # home / away
        field_team = team_element.get_attribute("itemprop")
        team_name = team_element.find_element(By.TAG_NAME, "a").get_attribute("innerHTML")
        match_detail[field_team] = team_name
        
    # access match overview
    match_overview_href = match_element.find_element(By.LINK_TEXT, "Overview").get_attribute("href")
    driver.get(match_overview_href)
    time.sleep(2)
    
    #Get match time
    match_time = driver.find_element(By.CLASS_NAME, "matchTop").find_element(By.CSS_SELECTOR, "span[itemprop='startDate']").get_attribute("innerHTML")
    match_detail["match_time"] = match_time
    
    # Get score based on quarter
    score_detail_box_element = driver.find_element(By.CLASS_NAME, "detailLive").find_element(By.CLASS_NAME, "left-box").find_element(By.CLASS_NAME, "scoresDetails")
    score_row_elements = score_detail_box_element.find_elements(By.CLASS_NAME, "content")
    scores = {}
    for row_element in score_row_elements:
        team_name = row_element.find_element(By.CLASS_NAME, "nameOver").find_element(By.TAG_NAME, "span").get_attribute("innerHTML")
        score_elements = row_element.find_elements(By.CLASS_NAME, "flex-1")
        ot_included = False
        
        #get scores : q1, q2, q3, q4, (ot), final
        if len(score_elements) > 5:
            ot_included = True
            
        match_detail["ot_included"] = ot_included
        score_detail = get_quarter_score(score_elements)
        scores[team_name] = score_detail
    
    match_detail["overview_scores"] = scores
    
    #GET prebet (get from bet365)
    odd_href = driver.find_element(By.LINK_TEXT, "Odds").get_attribute("href")
    driver.get(odd_href)
    prebet_odds = get_prebet_odds(driver)
    match_detail["prebet_moneyline"] = prebet_odds["moneyline"]
    match_detail["prebet_hdc"] = prebet_odds["hdc"]
    match_detail["prebet_ou"] = prebet_odds["ou"]
    
    return match_detail

def get_quarter_score(score_elements):
    score_detail = {}
    for i, score_element in enumerate(score_elements):
        score = score_element.get_attribute("innerHTML")
        #regular time score
        if i < 4:
            score_detail[f"q_{i+1}"] = score
        
        #OT included
        elif i >=4 and i < len(score_elements)-1:
            score_detail[f"ot_{i-3}"] = score
        
        #final score
        else:
            score_detail["Final Score"] = score
    
    return score_detail

def get_prebet_odds(driver):
    pass