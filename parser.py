from msilib.schema import Error
import json
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from os.path import exists


def gameParser(url):
    isValidUrl = url.startswith("http://www.sajl.org/images/tilastot")
    if (isValidUrl == False):
        raise Error(url + "is not a valid url.")
    start_time = time.time()
    #init parser
    options = Options()
    options.headless = True
    path_to_chromedriver = 'C:/chromedriver' # change path as needed
    browser = webdriver.Chrome(path_to_chromedriver, options=options)
    browser.get(url)

    jsonName = str(browser.find_element("xpath", '/html/body/center/font/h3/font').text)

    file_exists = exists(jsonName)

    #TODO: make some kind of cache that knows if we generated this file not too long ago so we dont have to
    #generate it every time somebody asks for the data
    if file_exists:
        with open(jsonName) as f:
            data = json.load(f)
            quarters = json.dumps(data)
            quarters = json.loads(quarters)
            for qrt in quarters:
                for down in qrt:
                    return quarters
                    # if down.get('description') == 'FINAL SCORE':

    # get and set team names 
    homeTeamName = browser.find_element("xpath",'/html/body/center/font/font[1]/center/p[3]/table/tbody/tr[3]/td[1]/font/b').text
    awayTeamName = browser.find_element("xpath",'/html/body/center/font/font[1]/center/p[3]/table/tbody/tr[2]/td[1]/font/b').text
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
        drives = []
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
            
            playType = {
                "playType": GetPlayType(description),
                "direction": GetDirection(description),
                "result": GetPlayResult(description)
            }

            parsedDownAndDistance = downAndDistance.split("-")
            down = ""
            distance = ""
            if (len(parsedDownAndDistance) > 1):
                down = parsedDownAndDistance[0]
                distance = parsedDownAndDistance[1]
         
            if (description.startswith("Drive:")):
                drive = {
                    "summary": description,
                    "downs": downs
                }
                drives.append(drive)
                downs = []
            elif  (False):
                #figure out here how to manage PAT etc
                return ""
            else:
                down = {
                    "id": downId,
                    "qrt": currentQuarter,
                    "homeScore": "",
                    "awayScore": "",
                    "team": team,
                    "downAndDistance": downAndDistance,
                    "down": down,
                    "distance": distance,
                    "ballPosition": ballPosition,
                    "description": description,
                    "playType": playType,
                    "penalty": penalty,
                    "clock": ""
                }
                downs.append(down)

        quarters.append(drives)
        if (gameOver):
            break

    print("Runtime %s seconds" % (time.time() - start_time))
    browser.quit()

    gameObject = {
            "home": homeTeamName,
            "away": awayTeamName,
            "quarters": quarters
        }
    

    gameObjectJson = json.dumps(gameObject)
    jsonFile = open(jsonName, "w")
    jsonFile.write(json.dumps(gameObjectJson))
    jsonFile.close()

    return gameObjectJson

# run this separately if needed
if __name__ == '__main__':
    gameParser()

def GetPlayResult(description):
    if "incomplete" in description:
        return "incomplete"
    if "downed" in description:
        return "downed"
    if "complete" in description:
        return "complete"
    if "MISSED" in description:
        return "MISSED"

    return ""

def GetPlayType(description):
    if "punt" in description:
        return "punt"
    if "kickoff" in description:
        return "kickoff"
    if "pass" in description:
        return "pass"
    if "rush" in description:
        return "rush"
    if "field goal" in description:
        return "field goal"
    if "Timeout" in description:
        return "timeout"
        
    return ""

def GetDirection(description):
    if "left" in description:
       return  "left"
    if "right" in description:
       return  "right"
    if "middle" in description:
       return  "middle"
       
    return ""

def GetPassLenght(description):
    if "short" in description:
       return  "short"
    if "deep" in description:
       return  "deep"
    if "middle" in description:
       return  "middle"
       
    return ""