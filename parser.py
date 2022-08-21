import pandas as pd
import time
import json
import datetime

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from os.path import exists


def gameParser():
    start_time = time.time()
    jsonName = str("gameIdOrSomething.json")
    file_exists = exists(jsonName)

    #TODO: make some kind of cache that knows if we generated this file not too long ago so we dont have to
    #generate it every time somebody asks for the data
    if file_exists:
        with open(jsonName) as f:
            data = json.load(f)
            data = json.dumps(data)
            quarters = json.loads(data)
            for qrt in quarters:
                for down in qrt:
                    if down.get('description') == 'FINAL SCORE':
                        return data

    #init parser
    options = Options()
    options.headless = True
    path_to_chromedriver = 'C:/chromedriver' # change path as needed
    browser = webdriver.Chrome(path_to_chromedriver, options=options)

    url = 'http://www.sajl.org/images/tilastot/roosters-crocodiles-20-08-2022.shtml'


    
    browser.get(url)

    # get and set team names 
    # homeTeamName = browser.find_element("xpath",'/html/body/center/font/font[1]/center/p[3]/table/tbody/tr[3]/td[1]/font/b').text
    # awayTeamName = browser.find_element("xpath",'/html/body/center/font/font[1]/center/p[3]/table/tbody/tr[2]/td[1]/font/b').text
    # meta = {
    #     "created": datetime.datetime.now()
    # }

    quarters = []
    gameOver = False
    # overTime = False

    for b in range(5):
        currentQuarter = str(b + 1)
        
        # something to do with ot
        # if currentQuarter == 5:
            # overTime = True
        
        rowString = str('/html/body/center/font/font[7]/center/table[' + currentQuarter + ']/tbody/tr')
        rows = browser.find_elements("xpath", rowString)
        rowCount = len(rows)
        downs = []
        for x in range(rowCount):
            # get down data
            downId = str(x+1)
            downXpath = '/html/body/center/font/font[7]/center/table[' + currentQuarter + ']/tbody/tr[' + downId + ']'
            team = browser.find_element("xpath", downXpath+'/td[1]').text
            downAndDistance = browser.find_element("xpath", downXpath + '/td[2]').text
            ballPosition = browser.find_element("xpath",downXpath + '/td[3]').text
            description = browser.find_element("xpath",downXpath + '/td[4]').text
            penalty = False

            if description == 'FINAL SCORE':
                gameOver = True
            
            if "PENALTY" in description:
                penalty = True

            down = {
                "id": downId,
                "qrt": currentQuarter,
                "team": team,
                "downAndDistance": downAndDistance,
                "bassPos": ballPosition,
                "description": description,
                "penalty": penalty
            }
            downs.append(down)

        quarters.append(downs)
        if (gameOver):
            break

    print("Runtime %s seconds" % (time.time() - start_time))
    browser.quit()

    # df = pd.DataFrame(quarters)
    # print(df)

    quartersJson = json.dumps(quarters)

    jsonFile = open(jsonName, "w")
    jsonFile.write(quartersJson)
    jsonFile.close()

    return quartersJson

# run this separately if needed
if __name__ == '__main__':
    gameParser()