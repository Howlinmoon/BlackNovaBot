import support_lib as bnw
import time
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
    debug = True
    xBanner  = "html/body/h1"
    xCredits = "html/body/div[1]/table[1]/tbody/tr/td[3]/strong"
    xHolds   = "html/body/div[1]/table[2]/tbody/tr/td[2]/table/tbody/tr[1]/td[2]/strong"
    xEnergy  = "html/body/div[1]/table[2]/tbody/tr/td[3]/table/tbody/tr[1]/td[2]/strong"
    xAverageTechLevel = "html/body/div[1]/table[2]/tbody/tr/td[1]/table/tbody/tr[12]/td[2]"

    shipStatus = {}
    if debug:
        print("Attempting to extract the ship tech levels and other status")
    # retrieve the current page
    currentPage = bnw.getPage()
    baseURL = ('/').join(currentPage.split('/')[:-1])
    shipStatusPage = "{}/report.php".format(baseURL)
    mainPage = "{}/main.php".format(baseURL)
    bnw.loadPage(shipStatusPage)
    time.sleep(2)
    bannerText = bnw.textFromElement(xBanner)
    if bannerText == "DONTEXIST":
        print("Unable to load player ship status page")
        exit(1)
    if bannerText != "Ship Report":
        print("Unexpected Banner Text: {}".format(bannerText))
        exit(1)
    # retrieve the ship stats
    if debug:
        print("Retrieving ship stats")

    itemList = []
    for tr in range(2, 12):
        xItem = "html/body/div[1]/table[2]/tbody/tr/td[1]/table/tbody/tr[{}]".format(tr)
        itemList.append(xItem)

    for tr in range(2, 6):
        xItem = "html/body/div[1]/table[2]/tbody/tr/td[2]/table/tbody/tr[{}]".format(tr)
        itemList.append(xItem)

    for tr in range(8, 11):
        xItem = "html/body/div[1]/table[2]/tbody/tr/td[2]/table/tbody/tr[{}]".format(tr)
        itemList.append(xItem)

    for tr in range(4, 12):
        xItem = "html/body/div[1]/table[2]/tbody/tr/td[3]/table/tbody/tr[{}]".format(tr)
        itemList.append(xItem)

    for currentItem in itemList:
        xItemName = currentItem + "/td[1]"
        xItemValue = currentItem + "/td[2]"
        itemName = bnw.textFromElement(xItemName)
        itemValue = bnw.textFromElement(xItemValue)
        if itemName == "DONTEXIST" or itemValue == "DONTEXIST":
            print("ERROR extracting currentItem: {}".format(currentItem))
            print("itemName: {}, itemValue: {}".format(itemName, itemValue))
            exit(1)
        if debug:
            print("itemName: {}, itemValue: {}".format(itemName, itemValue))
        if "Level " in itemValue:
            itemValue = itemValue.replace('Level ','')
        shipStatus[itemName] = itemValue

    # grab non-conformance stats
    averageTechLevel = bnw.textFromElement(xAverageTechLevel)
    if averageTechLevel == "DONTEXIST":
        print("Unable to extract average tech level")
        exit(1)
    shipStatus["Average tech level"] = averageTechLevel


    shipCredits = bnw.textFromElement(xCredits)
    if shipCredits == "DONTEXIST":
        print("Unable to extract credits")
        exit(1)
    shipStatus["Credits"] = shipCredits

    shipHolds = bnw.textFromElement(xHolds)
    if shipHolds == "DONTEXIST":
        print("Unable to extract holds")
        exit(1)
    shipStatus["Holds"] = shipHolds

    shipEnergy = bnw.textFromElement(xEnergy)
    if shipEnergy == "DONTEXIST":
        print("Unable to extract energy")
        exit(1)
    shipStatus["Energy"] = shipEnergy

    # return to the main page
    bnw.loadPage(mainPage)

    return shipStatus
