import support_lib as bnw
import time
import re
# This module handles interactions with special ports, and normal trading ports

def specialPort(purchaseDict):
    specialText = "Special Port"
    genericText = "Trading Commodities"
    xBanner         = "html/body/h1"
    xWholePage      = "html/body"
    xHullSelect     = "html/body/form/table[1]/tbody/tr[2]/td[9]/select"
    xEnginesSelect  = "html/body/form/table[1]/tbody/tr[3]/td[9]/select"
    xComputerSelect = "html/body/form/table[1]/tbody/tr[5]/td[9]/select"
    xBuyButton      = "html/body/form/table[3]/tbody/tr/td[1]/input"
    xTotalCost      = "html/body/form/table[3]/tbody/tr/td[2]/input"

    currentPage = bnw.getPage()
    baseURL = ('/').join(currentPage.split('/')[:-1])
    portPage = "{}/port.php".format(baseURL)
    mainPage = "{}/main.php".format(baseURL)

    # load the page
    bnw.loadPage(portPage)

    if not bnw.elementExists(xBanner):
        allText = bnw.textFromElement(xWholePage)
        if "There is no port here" in allText:
            print("There is no port in this sector")
            bnw.load(mainPage)
            return ["ERROR", "NO PORT"]
        else:
            print("Unhandled Error #1 in specialPort")
            exit(1)

    bannerText = bnw.textFromElement(xBanner)
    if genericText in bannerText:
        print("This is not a special port")
        bnw.load(mainPage)
        return ["ERROR", "WRONG PORT"]

    if not bannerText == specialText:
        print("Unhandled Error #2 in specialPort")
        exit(1)

    requestedEngineTech = purchaseDict["engineTech"]
    requestedComputerTech = purchaseDict["computerTech"]
    requestedHullTech = purchaseDict["hullTech"]

    # set the requested tech drop downs
    currentEngineTech = bnw.selectedValue(xEnginesSelect)
    currentComputerTech = bnw.selectedValue(xComputerSelect)
    currentHullTech = bnw.selectedValue(xHullSelect)

    print("Current Engine Tech: {}, Req Engine Tech: {}".format(currentEngineTech, requestedEngineTech, ))
    print("Current Computer Tech: {}, Req Computer Tech: {}".format(currentComputerTech, requestedComputerTech))
    print("Current Hull Tech: {}, Req Hull Tech: {}".format(currentHullTech, requestedHullTech))

    if requestedEngineTech != currentEngineTech:
        if not bnw.selectDropDownNew(xEnginesSelect, requestedEngineTech):
            print("Unable to select the requested engine tech value")

    if requestedComputerTech != currentComputerTech:
        if not bnw.selectDropDownNew(xComputerSelect, requestedComputerTech):
            print("Unable to select the requested computer tech value")

    if requestedHullTech != currentHullTech:
        if not bnw.selectDropDownNew(xHullSelect, requestedHullTech):
            print("Unable to select the requested hull tech value")

    # read how much it is going to cost
    howMuch = bnw.textFromElement(xTotalCost)
    if howMuch == "DONTEXIST":
        print("Unable to find the total cost display")
        exit(1)
    print("Cost is: {}".format(howMuch))

    if howMuch == "Not enough credits":
        print("Unable to afford this purchase")
        bnw.loadPage(mainPage)
        return ["ERROR", "TOO EXPENSIVE"]

    print("Attempting to execute the purchase")
    if not bnw.clickButton(xBuyButton):
        print("Was unable to click the 'Buy' button")
        exit(1)

    bnw.loadPage(mainPage)
    return ["SUCCESS", ""]
