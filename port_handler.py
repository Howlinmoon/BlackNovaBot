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
    xCredits        = "html/body/p[1]"
    xResultsBanner  = "html/body/table/tbody/tr[1]/td/font/strong"
    xTotalCost      = "html/body/table/tbody/tr[2]/td/strong/font"

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

    # hack
    bnw.onBlurFix()

    # determine how many credits are available for spending
    textBlob = bnw.textFromElement(xCredits)
    # regex out the cost
    # You have 206,527,757 credits to spend.
    m = re.search("have\s+(.*)\s+credits", textBlob)
    if not m:
        print("Unable to regex the available credits!")
        exit(1)
    creditAvailable = int(m.group(1).replace(",",""))

    requestedEngineTech = purchaseDict["engineTech"]
    requestedComputerTech = purchaseDict["computerTech"]
    requestedHullTech = purchaseDict["hullTech"]

    # set the requested tech drop downs
    currentEngineTech = bnw.selectedValue(xEnginesSelect)
    currentComputerTech = bnw.selectedValue(xComputerSelect)
    currentHullTech = bnw.selectedValue(xHullSelect)

    print("Credits available: {}".format(creditAvailable))
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

    print("Attempting to execute the purchase")
    if not bnw.clickButton(xBuyButton):
        print("Was unable to click the 'Buy' button")
        exit(1)

    time.sleep(2)
    if not bnw.elementExists(xResultsBanner):
        allText = bnw.textFromElement(xWholePage)
        m = re.search("total cost is\s+(.*)\s+credits and you only have\s+(.*)\s+credits.", allText)
        if not m:
            print("Not a successful trade, and unable to determine why")
            exit(1)
        theCost = int(m.group(1).replace(",",""))
        theCredits = int(m.group(2).replace(",",""))
        notEnough = theCost - theCredits
        print("Short {} credits".format(notEnough))
        return["ERROR", "TOO EXPENSIVE"]

    resultBanner = bnw.textFromElement(xResultsBanner)
    if not resultBanner == "Results for this trade":
        print("Results banner not found")
        exit(1)

    # Cost : 2,500 Credits
    finalBlob = bnw.textFromElement(xTotalCost)
    if finalBlob == "DONTEXIST":
        print("Total cost not found")
        exit(1)
    m = re.search("Cost\s\:\s(.*)\sCredits", finalBlob)
    if not m:
        print("Unable to regex the final cost")
        exit(1)
    finalCost = int(m.group(1).replace(",",""))
    bnw.loadPage(mainPage)
    return ["SUCCESS", finalCost]
