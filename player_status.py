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
        playerStatus['currentSector'] = int(currentSector)

    if debug:
        print('Querying current credits')
    money = bnw.textFromElement(xFunds)
    if money == "DONTEXIST":
        print("The current money xpath is incorrect")
        exit(1)
    else:
        playerStatus['credits'] = int(money.replace(',',''))

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

# convert string value to either INT or a Float
# taken from: http://stackoverflow.com/questions/379906/parse-string-to-float-or-int
def toNumber(aString):
    try:
        return int(aString)
    except ValueError:
        return float(aString)

# handle the 'current'/'max' values
def currentMax(xpath):
    rawValue = bnw.textFromElement(xpath)
    if rawValue == "DONTEXIST":
        print("currentMax was passed a bad xpath")
        exit(1)
    rawList = rawValue.replace(',','').split('/')
    return (toNumber(rawList[0]), toNumber(rawList[1]))

# handle the 'Yes' or 'No' values
def yesOrNo(xpath):
    rawValue = bnw.textFromElement(xpath)
    if rawValue == "Yes":
        return True
    else:
        return False

# Display and parse the ship status page
def getShipStatus():
    debug = False
    shipStatus = {}

    xBanner           = "html/body/h1"
    xCredits          = "html/body/div[1]/table[1]/tbody/tr/td[3]/strong"
    xHolds            = "html/body/div[1]/table[2]/tbody/tr/td[2]/table/tbody/tr[1]/td[2]/strong"
    xEnergy           = "html/body/div[1]/table[2]/tbody/tr/td[3]/table/tbody/tr[1]/td[2]/strong"
    xAverageTechLevel = "html/body/div[1]/table[2]/tbody/tr/td[1]/table/tbody/tr[12]/td[2]"
    xHull             = "html/body/div[1]/table[2]/tbody/tr/td[1]/table/tbody/tr[2]/td[2]"
    xEngines          = "html/body/div[1]/table[2]/tbody/tr/td[1]/table/tbody/tr[3]/td[2]"
    xPower            = "html/body/div[1]/table[2]/tbody/tr/td[1]/table/tbody/tr[3]/td[2]"
    xComputer         = "html/body/div[1]/table[2]/tbody/tr/td[1]/table/tbody/tr[5]/td[2]"
    xSensors          = "html/body/div[1]/table[2]/tbody/tr/td[1]/table/tbody/tr[6]/td[2]"
    xArmor            = "html/body/div[1]/table[2]/tbody/tr/td[1]/table/tbody/tr[7]/td[2]"
    xShields          = "html/body/div[1]/table[2]/tbody/tr/td[1]/table/tbody/tr[8]/td[2]"
    xBeamWeapons      = "html/body/div[1]/table[2]/tbody/tr/td[1]/table/tbody/tr[9]/td[2]"
    xTorpedoLaunchers = "html/body/div[1]/table[2]/tbody/tr/td[1]/table/tbody/tr[10]/td[2]"
    xCloak            = "html/body/div[1]/table[2]/tbody/tr/td[1]/table/tbody/tr[11]/td[2]"
    xOre              = "html/body/div[1]/table[2]/tbody/tr/td[2]/table/tbody/tr[2]/td[2]"
    xOrganics         = "html/body/div[1]/table[2]/tbody/tr/td[2]/table/tbody/tr[3]/td[2]"
    xGoods            = "html/body/div[1]/table[2]/tbody/tr/td[2]/table/tbody/tr[4]/td[2]"
    xColonists        = "html/body/div[1]/table[2]/tbody/tr/td[2]/table/tbody/tr[5]/td[2]"
    xSpaceBeacons     = "html/body/div[1]/table[2]/tbody/tr/td[3]/table/tbody/tr[4]/td[2]"
    xWarpEditors      = "html/body/div[1]/table[2]/tbody/tr/td[3]/table/tbody/tr[5]/td[2]"
    xGenesisTorpedoes = "html/body/div[1]/table[2]/tbody/tr/td[3]/table/tbody/tr[6]/td[2]"
    xMineDeflectors   = "html/body/div[1]/table[2]/tbody/tr/td[3]/table/tbody/tr[7]/td[2]"
    xEmergencyWarpDev = "html/body/div[1]/table[2]/tbody/tr/td[3]/table/tbody/tr[8]/td[2]"
    xArmorPoints      = "html/body/div[1]/table[2]/tbody/tr/td[2]/table/tbody/tr[8]/td[2]"
    xFighters         = "html/body/div[1]/table[2]/tbody/tr/td[2]/table/tbody/tr[9]/td[2]"
    xTorpedoes        = "html/body/div[1]/table[2]/tbody/tr/td[2]/table/tbody/tr[10]/td[2]"
    xEscapePod        = "html/body/div[1]/table[2]/tbody/tr/td[3]/table/tbody/tr[9]/td[2]"
    xFuelScoop        = "html/body/div[1]/table[2]/tbody/tr/td[3]/table/tbody/tr[10]/td[2]"
    xLastSeenShipDev  = "html/body/div[1]/table[2]/tbody/tr/td[3]/table/tbody/tr[11]/td[2]"

    simples = [
        ["Average tech level", xAverageTechLevel], ["Hull", xHull], ["Engines", xEngines], ["Power", xPower],
        ["Computer", xComputer], ["Sensors", xSensors], ["Armor", xArmor], ["Shields", xShields],
        ["Beam Weapons", xBeamWeapons], ["Torpedo launchers", xTorpedoLaunchers], ["Cloak", xCloak],
        ["Ore", xOre], ["Organics", xOrganics], ["Goods", xGoods], ["Colonists", xColonists],
        ["Space Beacons", xSpaceBeacons], ["Warp Editors", xWarpEditors], ["Genesis Torpedoes", xGenesisTorpedoes],
        ["Mine Deflectors", xMineDeflectors], ["Emergency Warp Device", xEmergencyWarpDev]
    ]
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

    for currentSimple in simples:
        itemName = currentSimple[0]
        itemXpath = currentSimple[1]
        rawValue = bnw.textFromElement(itemXpath)
        if debug:
            print("itemName: {}, rawValue: {}".format(itemName, rawValue))
        if rawValue == "DONTEXIST":
            print("xpath is incorrect for {}".format(itemName))
            exit(1)
        value = toNumber(rawValue.replace('Level ','').replace(',',''))
        shipStatus[itemName] = value

    # current / max handling
    shipStatus["Holds"],    shipStatus["HoldsMax"]     = currentMax(xHolds)
    shipStatus["Energy"],   shipStatus["EnergyMax"]    = currentMax(xEnergy)
    shipStatus["ArmorPts"], shipStatus["ArmorMax"]     = currentMax(xArmorPoints)
    shipStatus["Fighters"], shipStatus["FightersMax"]  = currentMax(xFighters)
    shipStatus["Torpedoes"],shipStatus["TorpedoesMax"] = currentMax(xTorpedoes)
    # Yes / No handling
    shipStatus["EscapePod"] = yesOrNo(xEscapePod)
    shipStatus["FuelScoop"] = yesOrNo(xFuelScoop)
    shipStatus["LastShipSeenDev"] = yesOrNo(xLastSeenShipDev)

    # finally, grab the credits also
    rawValue = bnw.textFromElement(xCredits)
    if rawValue == "DONTEXIST":
        print("xpath is incorrect for credits")
        exit(1)
    value = toNumber(rawValue.replace(',', '').replace('Credits:',''))
    shipStatus["Credits"] = value
    # return to the main page
    bnw.loadPage(mainPage)
    return shipStatus

# Display and parse the planet status page
def getPlanetStatus():
    debug = True
    xBanner  = "html/body/h1"
    xPlanetStatus = "html/body/div[1]"

    planetStatus = {}
    if debug:
        print("Attempting to extract the owned planet status")
    # retrieve the current page
    currentPage = bnw.getPage()
    baseURL = ('/').join(currentPage.split('/')[:-1])
    planetStatusPage = "{}/planet_report.php".format(baseURL)
    mainPage = "{}/main.php".format(baseURL)
    bnw.loadPage(planetStatusPage)
    time.sleep(2)
    bannerText = bnw.textFromElement(xBanner)
    if bannerText == "DONTEXIST":
        print("Unable to load planet status page")
        exit(1)
    if bannerText != "Planet Report: Status":
        print("Unexpected Banner Text: {}".format(bannerText))
        exit(1)
    # retrieve the planet stats
    if debug:
        print("Retrieving planet stats")
    planetBlob = bnw.textFromElement(xPlanetStatus)
    if "You have no planets so far" in planetBlob:
        bnw.loadPage(mainPage)
        return planetStatus

