import support_lib as bnw

# This module scans the specified sector and returns what it finds

# XPaths
xLinks    = "html/body/table[2]/tbody/tr[2]/td"
xShips    = "html/body/table[2]/tbody/tr[4]/td"
xPort     = "html/body/table[2]/tbody/tr[6]/td"
xPlanets  = "html/body/table[2]/tbody/tr[8]/td"
xMines    = "html/body/table[2]/tbody/tr[10]/td"
xFighters = "html/body/table[2]/tbody/tr[12]/td"
xBanner   = "html/body/table[1]/tbody/tr/td/strong"

def lrScan(sector):
    # retrieve the current page
    currentPage = bnw.getPage()
    baseURL = ('/').join(currentPage.split('/')[:-1])
    scanURL = "{}/lrscan.php?sector={}".format(baseURL, sector)

    # load the page
    scanResult = {}
    bnw.loadPage(scanURL)
    verifyText = bnw.textFromElement(xBanner)
    if not "Sector {}".format(sector) in verifyText:
        print("Illegal sector specified: {}".format(sector))
        exit(1)

    # Retrieve any links out of the sector
    linksText = bnw.textFromElement(xLinks)
    if linksText == "DONTEXIST":
        print("xLinks is incorrect - aborting")
        exit(1)
    scanResult['links'] = linksText.replace(' ','').split(',')

    # Retrieve any ships in the sector
    shipsText = bnw.textFromElement(xShips)
    if shipsText == "DONTEXIST":
        print("xShips is incorrect - aborting")
        exit(1)
    scanResult['ships'] = shipsText.replace(' ','').split(',')

    # Retrieve port info - if any
    portText = bnw.textFromElement(xPort)
    if portText == "DONTEXIST":
        print("xPort is incorrect - aborting")
        exit(1)
    else:
        scanResult['port'] = portText

    # Retrieve any planets in the sector
    planetsText = bnw.textFromElement(xPlanets)
    if planetsText == "DONTEXIST":
        print("xPlanets is incorrect - aborting")
        exit(1)
    else:
        scanResult['planets'] = planetsText.replace(' ','').split(',')

    # Retrieve any mines in the sector
    minesText = bnw.textFromElement(xMines)
    if minesText == "DONTEXIST":
        print("xMines is incorrect - aborting")
        exit(1)
    print('minesText: "{}"'.format(minesText))
    scanResult['mines'] = int(minesText.replace(', ',''))

    # Retrieve any fighters in the sector
    fightersText = bnw.textFromElement(xFighters)
    if fightersText == "DONTEXIST":
        print("xFighters is incorrect - aborting")
        exit(1)
    scanResult['fighters'] = int(fightersText.replace(',',''))

    # Important - Return to the original page!
    bnw.loadPage(currentPage)


    return scanResult



