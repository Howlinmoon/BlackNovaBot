import support_lib as bnw
import scan_sector as scanner
import player_status as status
import time
import re
# This module manages trade routes


def createRoute(port1, port2, bidir=True , warp=True):
    debug = True
    # XPaths
    xBanner = "html/body/h1"
    xPort1 = "html/body/form/table/tbody/tr[2]/td[3]/input"
    xPort2 = "html/body/form/table/tbody/tr[7]/td[3]/input"
    xWarp = "html/body/form/table/tbody/tr[11]/td[2]/font/font/input"
    xRealSpace = "html/body/form/table/tbody/tr[11]/td[2]/font/input"
    xOneWay = "html/body/form/table/tbody/tr[12]/td[2]/font/input[1]"
    xBothWays = "html/body/form/table/tbody/tr[12]/td[2]/font/input[2]"
    xCreateBtn = "html/body/form/table/tbody/tr[14]/td[3]/input"
    xResults = "html/body/p[1]"

    allPaths = [xPort1, xPort2, xWarp, xRealSpace, xOneWay, xBothWays, xCreateBtn]
    if debug:
        print("createRoute called with: port1: {}, port2: {}, BiDir: {}, Warp: {}".format(port1, port2, bidir, warp))
    # retrieve the current page
    currentPage = bnw.getPage()
    baseURL = ('/').join(currentPage.split('/')[:-1])
    newRouteURL = "{}/traderoute.php?command=new".format(baseURL)

    # load the page
    scanResult = {}
    bnw.loadPage(newRouteURL)
    verifyText = bnw.textFromElement(xBanner)
    if not "Trade Routes" in verifyText:
        print("Unable to load Trade Route creation page")
        exit(1)

    # verify required xpaths exist
    for testXPath in allPaths:
        if not bnw.elementExists(testXPath):
            print("Unable to find xpath: {}".format(testXPath))
            exit(1)

    # fill in the details
    if not bnw.fillTextBox(xPort1, port1):
        print("Unable to fill in port1")
        exit(1)

    if not bnw.fillTextBox(xPort2, port2):
        print("Unable to fill in port2")
        exit(1)

    # select the radio buttons
    if warp:
        if not bnw.clickButton(xWarp):
            print('Unable to click the "Warp" radio button')
            exit(1)
    else:
        if not bnw.clickButton(xRealSpace):
            print('Unable to click the "Real Space" radio button')
            exit(1)


    if bidir:
        if not bnw.clickButton(xBothWays):
            print('Unable to click the "Both Ways" radio button')
            exit(1)
    else:
        if not bnw.clickButton(xOneWay):
            print('Unable to click the "One Way" radio button')
            exit(1)

    # push the button, and stand back!
    if not bnw.clickButton(xCreateBtn):
        print("Unable to click the 'Create' button")
        exit(1)

    time.sleep(2)
    if bnw.elementExists(xResults):
        resultText = bnw.textFromElement(xResults)
        if "New trade route created" in resultText:
            return True
        else:
            return False
    else:
        print("Unable to query the results of the trade route creation attempt")
        return False


def routeOptions(colonists = True, fighters = False, torpedoes = False, keepEnergy = False):
    debug = True
    # xpaths
    xColonistsCheckBox = "html/body/form/table/tbody/tr[2]/td[2]/input"
    xFightersCheckBox  = "html/body/form/table/tbody/tr[3]/td[2]/input"
    xTorpedoesCheckBox = "html/body/form/table/tbody/tr[4]/td[2]/input"
    xEnergyTradeButton = "html/body/form/table[2]/tbody/tr[1]/td[2]/input"
    xEnergyKeepButton  = "html/body/form/table[2]/tbody/tr[2]/td[2]/input"
    xSaveButton        = "html/body/form/table[2]/tbody/tr[4]/td[2]/input"
    xWholePage         = "html/body"
    xBanner            = "html/body/h1"

    # retrieve the current page
    currentPage = bnw.getPage()
    baseURL = ('/').join(currentPage.split('/')[:-1])
    optionPage = "{}/traderoute.php?command=settings".format(baseURL)
    bnw.loadPage(optionPage)
    time.sleep(2)
    bannerText = bnw.textFromElement(xBanner)
    if bannerText == "DONTEXIST":
        print("Unable to load the trade options page")
        exit(1)
    elif not bannerText == "Trade Routes":
        print("Unexpected banner text: {}, was looking for 'Trade Routes'".format(bannerText))
        exit(1)
    if debug:
        print("Trade Route option page successfully loaded")

    print("Attempting to change the special port trade settings")
    # check all of the xpaths
    if not bnw.elementExists(xColonistsCheckBox):
        print("Unable to find the Colonists check box")
        exit(1)
    if not bnw.elementExists(xFightersCheckBox):
        print("Unable to find the Fighters check box")
        exit(1)
    if not bnw.elementExists(xTorpedoesCheckBox):
        print("Unable to find the Torpedoes check box")
        exit(1)
    if not bnw.elementExists(xEnergyKeepButton):
        print("Unable to find the Energy Keep button")
        exit(1)
    if not bnw.elementExists(xEnergyTradeButton):
        print("Unable to find the Energy Trade button")
        exit(1)
    if not bnw.elementExists(xSaveButton):
        print("Unable to find the Save button")
        exit(1)

    if bnw.checkBox(xColonistsCheckBox, colonists):
        print("Colonists checkbox should be properly set")
    else:
        print("Was unable to set the Colonists checkbox...")
        exit(1)


    if bnw.checkBox(xFightersCheckBox, fighters):
        print("Fighters checkbox should be properly set")
    else:
        print("Was unable to set the Fighters checkbox...")
        exit(1)


    if bnw.checkBox(xTorpedoesCheckBox, torpedoes):
        print("Torpedoes checkbox should be properly set")
    else:
        print("Was unable to set the Torpedoes checkbox...")
        exit(1)

    if not keepEnergy:
        if not bnw.clickButton(xEnergyKeepButton):
            print("Was unable to select the Keep Energy button")
    else:
        if not bnw.clickButton(xEnergyTradeButton):
            print("Was unable to select the Trade Energy button")

    if not bnw.clickButton(xSaveButton):
        print("Was unable to update the trade route options")
        exit(1)

    time.sleep(3)
    wholePageText = bnw.textFromElement(xWholePage)
    if not "Global trade route settings saved" in wholePageText:
        print("Was unable to save the Trade Route settings")
        exit(1)

    # return to main page
    mainPage = "http://{}/main.php".format(baseURL)
    bnw.loadPage(mainPage)

# retrieve the currently configured trade routes (if any)
def retrieveRoutes():
    debug = False
    # XPaths
    xBanner = "html/body/h1"
    routeList = []
    xAnyPorts = "html/body/table/tbody/tr[3]/td[1]/font"

    # retrieve the current page
    currentPage = bnw.getPage()
    print('currentPage: {}'.format(currentPage))
    baseURL = ('/').join(currentPage.split('/')[:-1])
    routePage = "{}/traderoute.php".format(baseURL)
    mainPage = "{}/main.php".format(baseURL)

    print('attempting to load routePage: {}'.format(routePage))
    bnw.loadPage(routePage)
    time.sleep(2)
    bannerText = bnw.textFromElement(xBanner)
    if bannerText == "DONTEXIST":
        print("Unable to load the trade routes page")
        exit(1)
    elif not bannerText == "Trade Routes":
        print("Unexpected banner text: {}, was looking for 'Trade Routes'".format(bannerText))
        exit(1)
    if debug:
        print("Trade Routes page successfully loaded")

    # check and see if there are any routes to retrieve
    checkText = bnw.textFromElement(xAnyPorts)
    if not "Port" in checkText and not "Planet" in checkText:
        if debug:
            print("There are currently no established trade routes")
        # reload the main page
        bnw.loadPage(mainPage)
        return routeList
    if debug:
        print("There are one or more trade routes to retrieve")

    routeIndex = 2
    routeNumber = 0
    while True:
        routeNumber += 1
        routeIndex += 1
        xSource      = "html/body/table/tbody/tr[{}]/td[1]/font/a".format(routeIndex)
        xSourceType  = "html/body/table/tbody/tr[{}]/td[2]/font".format(routeIndex)
        xDestination = "html/body/table/tbody/tr[{}]/td[3]/font/a".format(routeIndex)
        xDestType    = "html/body/table/tbody/tr[{}]/td[4]/font".format(routeIndex)
        xDistance    = "html/body/table/tbody/tr[{}]/td[5]/font".format(routeIndex)
        xCircuit     = "html/body/table/tbody/tr[{}]/td[6]/font".format(routeIndex)
        xEdit        = "html/body/table/tbody/tr[{}]/td[7]/font/a[1]".format(routeIndex)

        sourcePort = bnw.textFromElement(xSource)
        if sourcePort == "DONTEXIST":
            if debug:
                print('Done retrieving trade routes')

            # reload the main page
            bnw.loadPage(mainPage)
            return routeList
        sourcePort = int(sourcePort)
        sourceType = bnw.textFromElement(xSourceType).strip()
        destPort = int(bnw.textFromElement(xDestination))
        destType = bnw.textFromElement(xDestType).strip()

        distance = bnw.textFromElement(xDistance)
        if "Warp" in distance:
            movementType = "Warp"
        else:
            movementType = "RS"
        m = re.search("(\d+) turn", distance)
        if not m:
            print("Unable to regex the distance in turns when parsing trade route distance: {}".format(distance))
            exit(1)
        distance = int(m.group(1))
        circuit  = bnw.textFromElement(xCircuit).strip()
        if "2 ways" in circuit:
            circuitType = "BiDirectional"
        else:
            circuitType = "UniDirectional"
        editLink = bnw.linkFromElement(xEdit)
        routeId = editLink.split('=')[-1]

        print('Route #{} From: {} (type: {}) To: {} (type: {})'.format(routeNumber, sourcePort, sourceType, destPort, destType))
        print("Distance: {}, Circuit Type: {}, Movement Type: {}, Route Id: {}".format(distance, circuitType, movementType, routeId))
        newRoute = [sourcePort, sourceType, destPort, destType, distance, movementType, circuitType, routeId]
        routeList.append(newRoute)

# checks to see if the specified sector is in the passed trade route db
def tradeDbSearch(sectorNumber, tradeRouteDb):
    print("tradeDbSearch is looking for sector number {} in the DB".format(sectorNumber))
    for eachEntry in tradeRouteDb:
        port1 = int(eachEntry[0])
        port2 = int(eachEntry[2])
        print("searching against port1: {} and port2: {}".format(port1, port2))
        if int(sectorNumber) == port1 or int(sectorNumber) == port2:
            print("sector number {} already exists in the db!".format(sectorNumber))
            return True
    print("sector number {} does not exist in the db".format(sectorNumber))
    return False

# This routine starts searching for an optimal trade route from the
# current sector.
# if it finds one, it returns True, otherwise, it gives up and returns False
# Pass it how many warps MAX to use (default maximum is 100)

def tradeRouteSearch(warpDB, maxTurns=100):
    debug = True
    # retrieve the current trade routes ourselves
    tradeRoutes = retrieveRoutes()
    oreSector = -1
    goodsSector = -1
    portSector = {}
    warpsUsed = 0
    while True:
        if warpsUsed >= maxTurns:
            if debug:
                print("Exceeded allotted turns")
                return ["FAILED", warpDB]

        if debug:
            print("Trying to retrieve player status")
        playerStatus = status.getStatus()
        warps = playerStatus['warps']
        currentSector = playerStatus['currentSector']
        warpDB[currentSector] = warps

        # Is the player ship in a sector with an Ore or Goods port?
        currentPort = playerStatus['sectorPort']
        if debug:
            print("currentPort: {}".format(currentPort))
        # is current port already in our trade route db - OR does it not have a tenable port?
        moveAlong = tradeDbSearch(currentSector, tradeRoutes)
        print("The current port is already in our trade db: {}".format(moveAlong))

        if currentPort != "Ore" and currentPort != "Goods":
            moveAlong = True
        if moveAlong:
            if debug:
                print("Current sector: {} does not have a desired port OR it's already in the DB - need to move".format(currentSector))
            # need to find the next available sector that is higher than the current one
            for newSector in warps:
                if int(newSector) < int(currentSector):
                    continue
                else:
                    break

            if debug:
                print("Attempting to move to sector: {}".format(newSector))
            if not bnw.moveTo(newSector):
                print("Was unable to move to the desired sector: {}".format(newSector))
                exit(1)
            else:
                if debug:
                    print("Successfully moved to the desired sector")
                warpsUsed += 1
                continue

        else:
            if debug:
                print("Current sector has a desired port!")
            portSector[currentPort] = int(currentSector)

            if currentPort == "Ore":
                oreSector = int(currentSector)
                needPort = "Goods"
            else:
                goodsSector = int(currentSector)
                needPort = "Ore"

            warps = playerStatus['warps']
            currentSector = playerStatus['currentSector']
            if debug:
                print("Checking to see if a neighboring sector contains a trading match")
                print("We should currently be in sector: {}".format(currentSector))
                print("Available warps: {}".format(warps))
                port2 = int(currentSector)

            for currentWarp in warps:
                scanResults = scanner.lrScan(currentWarp)
                if debug:
                    print("Scan Results for Sector: {} is: {}".format(currentWarp, scanResults))
                scannedWarps = scanResults['links']
                intWarps = [int(i) for i in scannedWarps]
                warpDB[currentWarp] = scannedWarps

                if scanResults['port'] == needPort:
                    if debug:
                        print('Found a possible {} port: {}'.format(needPort, currentWarp))
                    # does this warp allow return to this sector?
                    if not currentSector in scanResults['links']:
                        if debug:
                            print('{} Port has no return link to the current sector'.format(needPort))
                        continue
                    else:
                        if debug:
                            print('{} Port has a return link to the current sector'.format(needPort))
                            print("Attempting to move to {} sector: {}".format(needPort, currentWarp))
                        if not bnw.moveTo(currentWarp):
                            print("Was unable to move to the desired sector")
                            exit(1)
                        else:
                            warpsUsed += 1
                            if debug:
                                print("Successfully moved to the desired sector")
                            portSector[needPort] = int(currentWarp)
                            playerStatus = status.getStatus()
                            warps = playerStatus['warps']
                            currentSector = playerStatus['currentSector']
                            intWarps = [int(i) for i in warps]
                            warpDB[currentSector] = warps
                            port1 = int(currentSector)

                            if debug:
                                print("Should be able to setup a traderoute between")
                                print("Goods Port: {} and Ore Port: {}".format(portSector["Goods"],
                                                                               portSector["Ore"]))

                            print("Found a Trade Route!")
                            # create the route
                            print("Attempting to create the trade route linkage")
                            trCreateStatus = createRoute(port1, port2, bidir=True, warp=True)
                            if not trCreateStatus:
                                print("Was unable to create the specified trade route")
                                exit(1)
                            else:
                                print("Successfully created a trade route!")
                                # update the trade routes
                                tradeRoutes = retrieveRoutes()
                                return ['SUCCESS', tradeRoutes, warpDB]

            if oreSector == -1 or goodsSector == -1:
                print("Did not find a matching pair - continuing to look")
                oreSector = -1
                goodsSector = -1
                # need to find the next available sector that is higher than the current one
                # should handle the situation where the next sector in numerical order, only
                # leads back to the current one!
                print('examining warps: {}'.format(warps))
                print('warpDB: ')
                print(warpDB)

                for newSector in warps:
                    newLinks = warpDB[newSector]
                    if int(newSector) < int(currentSector):
                        continue
                    else:
                        print("considering moving to sector: {}".format(newSector))
                        print("it has links to: {}".format(newLinks))
                        # verify at least one of the links isn't back to here...
                        goodCheck = False
                        for linkCheck in newLinks:
                            if linkCheck != currentSector:
                                print("Found at least one link to someplace other than current sector")
                                goodCheck = True

                        if not goodCheck:
                            print("We have a problem, search algo would send us back to the current sector!")
                            exit(1)
                        # otherwise, we good to go with this new sector
                        break

                print("Attempting to move to sector: {}".format(newSector))
                if not bnw.moveTo(newSector):
                    print("Was unable to move to the desired sector")
                    exit(1)
                else:
                    print("Successfully moved to the desired sector")
                    warpsUsed += 1
                    playerStatus = status.getStatus()
                    warps = playerStatus['warps']
                    currentSector = playerStatus['currentSector']
                    intWarps = [int(i) for i in warps]
                    warpDB[currentSector] = warps
                    continue

# This function attempts to query the non-direct path distance to the start of a trade route
def queryIndirectPath(sector1, sector2, jump = False):
    debug = False
    xBanner = "html/body/h1"
    xWholePage = "html/body"
    if debug:
        print("Querying indirect distance between current sector {} and sector {}".format(sector1, sector2))
    # retrieve the current page
    currentPage = bnw.getPage()
    baseURL = ('/').join(currentPage.split('/')[:-1])
    rsPage = "{}/rsmove.php?engage=1&destination={}".format(baseURL, sector2)
    mainPage = "{}/main.php".format(baseURL)
    jumpPage = "{}/rsmove.php?engage=2&destination={}".format(baseURL, sector2)
    bnw.loadPage(rsPage)
    time.sleep(2)
    bannerText = bnw.textFromElement(xBanner)
    if bannerText == "DONTEXIST":
        print("Unable to load real space move page")
        exit(1)
    elif not bannerText == "Realspace Move":
        print("Unexpected banner text: {}, was looking for 'Realspace Move'".format(bannerText))
        exit(1)
    if debug:
        print("Realspace Move page successfully loaded")

    # due to non-formatting, we need to grab the entire page text
    entirePage = bnw.textFromElement(xWholePage)
    if entirePage == "DONTEXIST":
        print("Unable to extract the text from the entire page")
        exit(1)
    distance = -1
    energy = -1
    for eachLine in entirePage.split('\n'):
        if debug:
            print('Examining line: {}'.format(eachLine))
        m = re.search("take (\d+) turns.*gather (\d+) units", eachLine)
        if m:
            distance = m.group(1)
            energy = m.group(2)
            if debug:
                print("Distance is {}, would gather {} energy".format(distance, energy))
            break

    if distance == -1:
        print("regex didn't work - Blast!")
        exit(1)

    if not jump:
        # return to the main page
        bnw.loadPage(mainPage)
        return [distance, energy]
    else:
        print("Performing Real Space Jump in 3, 2, 1")
        bnw.loadPage(jumpPage)
        time.sleep(2)
        bnw.loadPage(mainPage)
        return True

# Execute a trade route
# /traderoute.php?engage=34
# This function attempts to query the non-direct path distance to the start of a trade route
def executeTrade(routeId, howManyTimes = 1, stopEarly = False):
    debug = True
    xBanner = "html/body/table/tbody/tr[1]/td/strong/font"
    xTotalProfit = "html/body/center/font/strong/font[1]/strong"
    xTurnsUsed = "html/body/center/font/strong/font[2]/strong/font"
    xTurnsLeft = "html/body/center/font/strong/font[3]/strong/font"
    xCredits   = "html/body/center/font/strong/font[4]/strong/font"
    xRepeat    = "html/body/form/input[1]"
    xSubmit    = "html/body/form/input[2]"
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
    if profit == "DONTEXIST":
        print("Unable to retrieve the profit")
        exit(1)
    profit = int(profit.replace(',', ''))

    turnsUsed = bnw.textFromElement(xTurnsUsed)
    if turnsUsed == "DONTEXIST":
        print("Unable to retrieve the turns used")
        exit(1)
    turnsUsed = int(turnsUsed)

    turnsLeft = bnw.textFromElement(xTurnsLeft)
    if turnsLeft == "DONTEXIST":
        print("Unable to retrieve the turns left")
        exit(1)

    currentCredits = bnw.textFromElement(xCredits)
    if currentCredits == "DONTEXIST":
        print("Unable to retrieve the current credits")
        exit(1)
    currentCredits = int(currentCredits.replace(',', ''))

    print("After initial trade, the results were")
    print("Profit: {}, Turns Left: {}".format(profit, turnsLeft))
    profitEfficiency = profit / turnsUsed
    print("Profit efficiency (profit {} / turns used {}): {}".format(profit, turnsUsed, profitEfficiency))

    if howManyTimes > 1:
        lastProfit = profit
        totalProfits = lastProfit
        totalTurnsUsed = turnsUsed
        moreTimes = howManyTimes - 1
        if debug:
            print("Attempting to execute the trade {} more times".format(moreTimes))
        if not bnw.fillTextBox(xRepeat, howManyTimes):
            print("Unable to fill in the repeat quantity")
            exit(1)
        if debug:
            print("Attempting to execute the multiple trades")
        if not bnw.clickButton(xSubmit):
            print("Unable to click the submit button")
            exit(1)

        if debug:
            print("Attempting to extract the stats from the multiple trades")

        for tradeNumber in range(moreTimes):
            xTotalProfit = "html/body/center[{}]/font/strong/font[1]/strong".format(tradeNumber + 1)
            xCredits     = "html/body/center[{}]/font/strong/font[4]/strong/font".format(tradeNumber + 1)
            xTurnsLeft   = "html/body/center[{}]/font/strong/font[3]/strong/font".format(tradeNumber + 1)
            xTurnsUsed   = "html/body/center[{}]/font/strong/font[2]/strong/font".format(tradeNumber + 1)
            profit = bnw.textFromElement(xTotalProfit)
            if profit == "DONTEXIST":
                print("Unable to retrieve the profit")
                exit(1)
            profit = int(profit.replace(',',''))
            totalProfits = totalProfits + profit

            turnsUsed = bnw.textFromElement(xTurnsUsed)
            if turnsUsed == "DONTEXIST":
                print("Unable to retrieve the turns used")
                exit(1)
            turnsUsed = int(turnsUsed)
            totalTurnsUsed = totalTurnsUsed + turnsUsed

            turnsLeft = bnw.textFromElement(xTurnsLeft)
            if turnsLeft == "DONTEXIST":
                print("Unable to retrieve the turns left")
                exit(1)

            currentCredits = bnw.textFromElement(xCredits)
            if currentCredits == "DONTEXIST":
                print("Unable to retrieve the current credits")
                exit(1)
            currentCredits = int(currentCredits.replace(',',''))

            print("After additional trade #{}, the results were".format(tradeNumber + 1))
            print("Profit: {}, Turns Left: {}, Credits: {}".format(profit, turnsLeft, currentCredits))
            profitEfficiency = totalProfits / turnsUsed
            print("Profit efficiency (total profit / total turns used): {}".format(profitEfficiency))

            profitDiff = profit - lastProfit
            lastProfit = profit
            if profitDiff < 0:
                print("Profits are declining!")
                if stopEarly:
                    if debug:
                        print("Stopping early to maintain efficiency!")
                    break
            elif profitDiff == 0:
                print("Profits are stable")
            else:
                print("Profits are increasing!")

    bnw.loadPage(mainPage)
    return

    # multiple trades
    # profit1 - html/body/center[1]/font/strong/font[1]/strong
    # profit2 - html/body/center[2]/font/strong/font[1]/strong



# For Edit Route
#  /traderoute.php?command=edit&traderoute_id=XX

# For Delete Route
#  /traderoute.php?command=delete&traderoute_id=Xx
