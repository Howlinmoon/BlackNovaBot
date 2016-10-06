import support_lib as bnw

# This module retrieves the players current status


# XPaths
xTurnsLeft     = "html/body/table[1]/tbody/tr[1]/td[1]/span"
xInSector      = "html/body/table[1]/tbody/tr[3]/td[1]/span"
xFunds         = "html/body/table[1]/tbody/tr[2]/td/span"
xScore         = "html/body/table[1]/tbody/tr[1]/td[3]/span"
xSectorType    = "html/body/table[1]/tbody/tr[3]/td[3]/a"
xSectorPort  = "html/body/table[2]/tbody/tr/td[2]/div[1]"
xOreCargo      = "html/body/table[2]/tbody/tr/td[3]/table[2]/tbody/tr/td/table/tbody/tr[2]/td/span"
xOrganicCargo  = "html/body/table[2]/tbody/tr/td[3]/table[2]/tbody/tr/td/table/tbody/tr[4]/td/span"
xGoodsCargo    = "html/body/table[2]/tbody/tr/td[3]/table[2]/tbody/tr/td/table/tbody/tr[6]/td/span"
xEnergy        = "html/body/table[2]/tbody/tr/td[3]/table[2]/tbody/tr/td/table/tbody/tr[8]/td/span"
xColonists     = "html/body/table[2]/tbody/tr/td[3]/table[2]/tbody/tr/td/table/tbody/tr[10]/td/span"

# sectors
# html/body/table[2]/tbody/tr/td[3]/table[6]/tbody/tr[1]/td/div/table/tbody/tr/td[1]/a

# html/body/table[2]/tbody/tr/td[3]/table[6]/tbody/tr[1]/td/div/table/tbody/tr[1]/td[1]/a
# html/body/table[2]/tbody/tr/td[3]/table[6]/tbody/tr[1]/td/div/table/tbody/tr[2]/td[1]/a
# html/body/table[2]/tbody/tr/td[3]/table[6]/tbody/tr[1]/td/div/table/tbody/tr[3]/td[1]/a

def getStatus():
    debug = False
    playerStatus = {}
    if debug:
        print('Querying turns left')
    turnsLeft = bnw.textFromElement(xTurnsLeft)
    if turnsLeft == "DONTEXIST":
        print("The turns remaining xpath is incorrect")
        exit(1)
    else:
        playerStatus['turnsLeft'] = int(turnsLeft.replace(',',''))

    if debug:
        print('Querying current sector')
    currentSector = bnw.textFromElement(xInSector)
    if currentSector == "DONTEXIST":
        print("The current sector xpath is incorrect")
        exit(1)
    else:
        playerStatus['currentSector'] = currentSector

    if debug:
        print('Querying current credits')
    money = bnw.textFromElement(xFunds)
    if money == "DONTEXIST":
        print("The current money xpath is incorrect")
        exit(1)
    else:
        playerStatus['money'] = int(money.replace(',',''))

    if debug:
        print('Querying current score')
    score = bnw.textFromElement(xScore)
    if score == "DONTEXIST":
        print("The current score xpath is incorrect")
        exit(1)
    else:
        playerStatus['score'] = int(score.replace(',',''))

    if debug:
        print('Querying sector type')
    sectorType = bnw.textFromElement(xSectorType)
    if sectorType == "DONTEXIST":
        print("The current sector type xpath doesn't exist")
        exit(1)
    else:
        playerStatus['sectorType'] = sectorType

    if debug:
        print('Querying sector port')
    # Sector Port needs special handling
    sectorPort = bnw.textFromElement(xSectorPort)
    if sectorPort == "DONTEXIST":
        print('xSectorPort did not exist')
        exit(1)
    else:
        fixedPort = sectorPort.replace('Trading port: ','')
    playerStatus['sectorPort'] = fixedPort

    # Cargoes
    if debug:
        print('Querying Ore Cargo')
    oreCargo = bnw.textFromElement(xOreCargo)
    if score == "DONTEXIST":
        print("The current Ore xpath is incorrect")
        exit(1)
    else:
        playerStatus['ore'] = int(oreCargo.replace(',',''))

    if debug:
        print('Querying Organics Cargo')
    organicCargo = bnw.textFromElement(xOrganicCargo)
    if score == "DONTEXIST":
        print("The current Organics xpath is incorrect")
        exit(1)
    else:
        playerStatus['organics'] = int(organicCargo.replace(',',''))

    if debug:
        print('Querying Goods Cargo')
    goodsCargo = bnw.textFromElement(xGoodsCargo)
    if score == "DONTEXIST":
        print("The current Goods xpath is incorrect")
        exit(1)
    else:
        playerStatus['goods'] = int(goodsCargo.replace(',',''))

    if debug:
        print('Querying Energy Cargo')
    energy = bnw.textFromElement(xEnergy)
    if score == "DONTEXIST":
        print("The current Energy xpath is incorrect")
        exit(1)
    else:
        playerStatus['energy'] = int(energy.replace(',',''))

    if debug:
        print('Querying colonists')
    colonists = bnw.textFromElement(xColonists)
    if score == "DONTEXIST":
        print("The current Colonists xpath is incorrect")
        exit(1)
    else:
        playerStatus['colonists'] = int(colonists.replace(',',''))

    # Determine the available warps
    warpNumber = 1
    warps = []
    while True:
        currentWarp = bnw.textFromElement("html/body/table[2]/tbody/tr/td[3]/table[6]/tbody/tr[1]/td/div/table/tbody/tr[{}]/td[1]/a".format(warpNumber))
        if debug:
            print('Querying Current Warp')

        if currentWarp == "DONTEXIST":
            break
        else:
            # => 0
            warps.append(currentWarp.replace('=> ',''))
            warpNumber += 1

    playerStatus['warps'] = warps

    return playerStatus

# Display and parse the ship status page
def getShipStatus():
    # /report.php
    debug = True
    xBanner = "html/body/h1"
    xCredits = "html/body/div[1]/table[1]/tbody/tr/td[3]/strong"
    xHolds = "html/body/div[1]/table[2]/tbody/tr/td[2]/table/tbody/tr[1]/td[2]/strong"
    xEnergy = "html/body/div[1]/table[2]/tbody/tr/td[3]/table/tbody/tr[1]/td[2]/strong"

    xHullLevelName    = "html/body/div[1]/table[2]/tbody/tr/td[1]/table/tbody/tr[2]/td[1]"
    xHullLevelValue   = "html/body/div[1]/table[2]/tbody/tr/td[1]/table/tbody/tr[2]/td[2]"
    xEngineLevelName  = "html/body/div[1]/table[2]/tbody/tr/td[1]/table/tbody/tr[3]/td[1]"
    xEngineLevelValue = "html/body/div[1]/table[2]/tbody/tr/td[1]/table/tbody/tr[3]/td[2]"
    #...
    xAverageTechName  = "html/body/div[1]/table[2]/tbody/tr/td[1]/table/tbody/tr[12]/td[1]/i"
    xAverageTechLevel = "html/body/div[1]/table[2]/tbody/tr/td[1]/table/tbody/tr[12]/td[2]"
    #...
    xOreName       = "html/body/div[1]/table[2]/tbody/tr/td[2]/table/tbody/tr[2]/td[1]"
    xOreValue      = "html/body/div[1]/table[2]/tbody/tr/td[2]/table/tbody/tr[2]/td[2]"
    #...
    xColonistsName = "html/body/div[1]/table[2]/tbody/tr/td[2]/table/tbody/tr[5]/td[1]"
    xColonistsQty  = "html/body/div[1]/table[2]/tbody/tr/td[2]/table/tbody/tr[5]/td[2]"
    # armor and weapons
    xArmorName     = "html/body/div[1]/table[2]/tbody/tr/td[2]/table/tbody/tr[8]/td[1]"
    xArmorAmount   = "html/body/div[1]/table[2]/tbody/tr/td[2]/table/tbody/tr[8]/td[2]"
    xFightersName  = "html/body/div[1]/table[2]/tbody/tr/td[2]/table/tbody/tr[9]/td[1]"
    xFightersQty   = ""


    xWholePage = "html/body"
    if debug:
        print("Attempting to execute trade route Id: {}".format(routeId))
    # retrieve the current page
    currentPage = bnw.getPage()
    baseURL = ('/').join(currentPage.split('/')[:-1])
    executePage = "{}/traderoute.php?engage={}".format(baseURL, routeId)
    mainPage = "{}/main.php".format(baseURL)
    bnw.loadPage(executePage)
    time.sleep(2)
    bannerText = bnw.textFromElement(xBanner)
    if bannerText == "DONTEXIST":
        print("Unable to load trade route execute page")
        exit(1)
    if bannerText != "Trade Route Results":
        print("Unexpected Banner Text: {}".format(bannerText))
        exit(1)
    # retrieve the stats from the sale
    if debug:
        print("Retrieving trade stats")

    profit = bnw.textFromElement(xTotalProfit)


