import support_lib as bnw
import time
import re
# This module handles interactions with special ports, and normal trading ports

def specialPort(purchaseDict):
    specialText = "Special Port"
    genericText = "Trading Commodities"
    xBanner          = "html/body/h1"
    xWholePage       = "html/body"
    # cost of the tech, Quantity on hand, input box for purchasing more
    xGenesisTorps    = ["html/body/form/table[1]/tbody/tr[2]/td[2]", "html/body/form/table[1]/tbody/tr[2]/td[3]", "html/body/form/table[1]/tbody/tr[2]/td[5]/input"]
    xSpaceBeacons    = ["html/body/form/table[1]/tbody/tr[3]/td[2]", "html/body/form/table[1]/tbody/tr[3]/td[3]", "html/body/form/table[1]/tbody/tr[3]/td[5]/input"]
    xEmerWarpDev     = ["html/body/form/table[1]/tbody/tr[4]/td[2]", "html/body/form/table[1]/tbody/tr[4]/td[3]", "html/body/form/table[1]/tbody/tr[4]/td[5]/input"]
    xWarpEditors     = ["html/body/form/table[1]/tbody/tr[5]/td[2]", "html/body/form/table[1]/tbody/tr[5]/td[3]", "html/body/form/table[1]/tbody/tr[5]/td[5]/input"]
    xMineDeflectors  = ["html/body/form/table[1]/tbody/tr[7]/td[2]", "html/body/form/table[1]/tbody/tr[7]/td[3]", "html/body/form/table[1]/tbody/tr[7]/td[5]/input"]
    xFighters        = ["html/body/form/table[2]/tbody/tr[2]/td[2]", "html/body/form/table[2]/tbody/tr[2]/td[3]", "html/body/form/table[2]/tbody/tr[2]/td[5]/input"]
    xArmorPoints     = ["html/body/form/table[2]/tbody/tr[3]/td[2]", "html/body/form/table[2]/tbody/tr[3]/td[3]", "html/body/form/table[2]/tbody/tr[3]/td[5]/input"]
    xEscapePod       = ["html/body/form/table[1]/tbody/tr[8]/td[2]", "html/body/form/table[1]/tbody/tr[8]/td[3]", "html/body/form/table[1]/tbody/tr[8]/td[5]/input"]
    xFuelScoop       = ["html/body/form/table[1]/tbody/tr[9]/td[2]", "html/body/form/table[1]/tbody/tr[9]/td[3]", "html/body/form/table[1]/tbody/tr[9]/td[5]/input"]
    xLastShipSeenDev = ["html/body/form/table[1]/tbody/tr[10]/td[2]", "html/body/form/table[1]/tbody/tr[10]/td[3]", "html/body/form/table[1]/tbody/tr[10]/td[5]/input"]
    xTorpedoes       = ["html/body/form/table[2]/tbody/tr[2]/td[7]", "html/body/form/table[2]/tbody/tr[2]/td[8]", "html/body/form/table[2]/tbody/tr[2]/td[10]/input"]
    xColonists       = ["html/body/form/table[2]/tbody/tr[3]/td[6]", "html/body/form/table[2]/tbody/tr[3]/td[8]", "html/body/form/table[2]/tbody/tr[3]/td[10]/input"]
    compList = ["Hull", "Engines", "Power", "Computer", "Sensors", "Beam Weapons",
                     "Armor", "Cloak", "Torpedo launchers", "Shields"]
    xSelectors = {}
    # http://stackoverflow.com/questions/22171558/what-does-enumerate-mean
    for compoffset, compName in enumerate(compList, 2):
        xSelectors[compName] = "html/body/form/table[1]/tbody/tr[{}]/td[9]/select".format(compoffset)

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

    # determine how many credits are available for spending
    textBlob = bnw.textFromElement(xCredits)
    # regex out the cost
    # You have 206,527,757 credits to spend.
    m = re.search("have\s+(.*)\s+credits", textBlob)
    if not m:
        print("Unable to regex the available credits!")
        exit(1)
    creditAvailable = int(m.group(1).replace(",",""))
    print("Credits available: {}".format(creditAvailable))

    # get the current tech levels
    currentTech = {}
    desiredTech = {}
    for compName in compList:
        if compName in purchaseDict:
            xpath = xSelectors[compName]
            currentTech[compName] = int(bnw.selectedValue(xpath))
            desiredTech[compName] = purchaseDict[compName]
            print("Current {} Tech: {}, Desired Tech: {}".format(compName, currentTech[compName], desiredTech[compName]))

            if desiredTech[compName] != currentTech[compName]:
                if not bnw.selectDropDownNew(xSelectors[compName], desiredTech[compName]):
                    print("Unable to select the requested {} tech value".format(compName))
                    exit(1)


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
    print("final cost: {}".format(finalCost))
    bnw.loadPage(mainPage)
    return ["SUCCESS", finalCost]
