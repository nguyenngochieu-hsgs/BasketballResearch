import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

def extract_overview_info(match_element, driver):
    match_detail = {}
    teams_element = match_element.find_element(By.CLASS_NAME, "team").find_elements(By.CLASS_NAME, "flex")
    for team_element in teams_element:
        # home / away
        field_team = team_element.get_attribute("itemprop")
        team_name = team_element.find_element(By.TAG_NAME, "a").get_attribute("innerHTML")
        match_detail[field_team] = team_name.replace(" ", "")
        
    # access match overview
    match_overview_href = match_element.find_element(By.LINK_TEXT, "Overview").get_attribute("href")
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])
    time.sleep(2)
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
    match_detail["prebets"] = get_prebet(driver)
    
    #Back to match page
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    time.sleep(1)
    
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

def get_prebet(driver):
    prebets = {}
    odd_content_element = driver.find_element(By.CLASS_NAME, "innerMatchInfo").find_elements(By.CLASS_NAME, "content")[1]
    odd_box_elements = odd_content_element.find_elements(By.XPATH, "//div[@class='w100 flex-1 brb brr flex']")
    for odd_box_element in odd_box_elements:
        
        #three odd boxes: moneyline, handicap, total
        prebet_boxes_elements = odd_box_element.find_elements(By.CLASS_NAME, "flex-col")
        
        #get prebet moneyline
        prebets["moneyline"] = extract_prebet_moneyline_and_hdc(prebet_boxes_elements[0], 1) if extract_prebet_moneyline_and_hdc(prebet_boxes_elements[0], 1) else None
        
        #get prebet handicap
        prebets["handicap"] = extract_prebet_moneyline_and_hdc(prebet_boxes_elements[1], 2) if extract_prebet_moneyline_and_hdc(prebet_boxes_elements[1], 2) else None
        
        #get prebet total (over, under)
        prebets["overunder"] = extract_prebet_overunder(prebet_boxes_elements[2]) if extract_prebet_overunder(prebet_boxes_elements[2]) else None
        
        if prebets["moneyline"] and prebets["handicap"] and prebets["overunder"]:
            break  
        
    return prebets

def extract_prebet_moneyline_and_hdc(prebet_boxes_elements, prebet_type_bg_pos):
    # opening_box = prebet_boxes_elements.find_element(By.CLASS_NAME, f"openingBg{prebet_type_bg_pos}")
    # opening_home = float(opening_box.find_elements(By.CLASS_NAME, "oddItems")[0].find_element(By.TAG_NAME, "span").find_element(By.TAG_NAME, "span").get_attribute("innerHTML"))
    # opening_away = float(opening_box.find_elements(By.CLASS_NAME, "oddItems")[1].find_element(By.TAG_NAME, "span").find_element(By.TAG_NAME, "span").get_attribute("innerHTML"))
    
    prebet_box = prebet_boxes_elements.find_element(By.CLASS_NAME, f"preMatchBg{prebet_type_bg_pos}") 
    
    #Check if contain prebet
    try:
        prebet_home = float(prebet_box.find_elements(By.CLASS_NAME, "oddItems")[0].find_element(By.TAG_NAME, "span").find_element(By.TAG_NAME, "span").get_attribute("innerHTML"))
        prebet_away = float(prebet_box.find_elements(By.CLASS_NAME, "oddItems")[1].find_element(By.TAG_NAME, "span").find_element(By.TAG_NAME, "span").get_attribute("innerHTML"))
    
    except: 
        return None
    
    return {"homeTeam": prebet_home, "awayTeam": prebet_away}


def extract_prebet_overunder(prebet_boxes_elements):
    # opening_box = prebet_boxes_elements.find_element(By.CLASS_NAME, "openingBg1")
    # opening_ou = float(opening_box.find_elements(By.CLASS_NAME, "oddItems")[0].find_element(By.TAG_NAME, "span").get_attribute("innerHTML"))
    
    prebet_box = prebet_boxes_elements.find_element(By.CLASS_NAME, "preMatchBg1") 
    
    #Check if contain prebet
    try:
        prebet_ou = float(prebet_box.find_elements(By.CLASS_NAME, "oddItems")[0].find_element(By.TAG_NAME, "span").get_attribute("innerHTML"))
    
    except:
        return None
        
    return prebet_ou
            
    