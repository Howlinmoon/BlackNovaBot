import support_lib as bnw
import time
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

    # retrieve the current page
    currentPage = bnw.getPage()
    baseURL = ('/').join(currentPage.split('/')[:-1])
    optionPage = "http://{}/traderoute.php?command=settings".format(baseURL)
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
    # XPaths
    xBanner = "html/body/h1"
    # Route 1 Source
    # html/body/table/tbody/tr[3]/td[1]/font/a
    # Route 1 Source Type
    # html/body/table/tbody/tr[3]/td[2]/font
    # Route 1 Destination
    # html/body/table/tbody/tr[3]/td[3]/font/a
    # Route 1 Destination Type
    # html/body/table/tbody/tr[3]/td[4]/font
    # Route 1 Distance
    # html/body/table/tbody/tr[3]/td[5]/font
    # Route 1 Circuit
    # html/body/table/tbody/tr[3]/td[6]/font
    # Route 1 Edit
    # html/body/table/tbody/tr[3]/td[7]/font/a[1]
    # Route 1 Delete
    # html/body/table/tbody/tr[3]/td[7]/font/a[2]

    # Route 2 Source
    # html/body/table/tbody/tr[4]/td[1]/font/a
    # Route 2 Source Type
    # html/body/table/tbody/tr[4]/td[2]/font
    # Route 2 Destination
    # html/body/table/tbody/tr[4]/td[3]/font/a
    # Route 2 Destination Type
    # html/body/table/tbody/tr[4]/td[4]/font
    # Route 2 Distance
    # html/body/table/tbody/tr[4]/td[5]/font
    # Route 2 Circuit
    # html/body/table/tbody/tr[4]/td[6]/font
    # Route 2 Edit
    # html/body/table/tbody/tr[4]/td[7]/font/a[1]
    # Route 2 Delete
    # html/body/table/tbody/tr[4]/td[7]/font/a[2]


    # retrieve the current page
    currentPage = bnw.getPage()
    baseURL = ('/').join(currentPage.split('/')[:-1])
    routePage = "http://{}/traderoute.php".format(baseURL)
    bnw.loadPage(routePage)
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
