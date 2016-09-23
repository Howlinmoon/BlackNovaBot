 # This module retrieves the global game settings and parses them
import support_lib as bnw
import time

def getSettings(baseURL):
    debug = True
    # xpaths
    # Key #1
    # html/body/table[1]/tbody/tr[1]/td[1]
    # Value #1
    # html/body/table[1]/tbody/tr[1]/td[2]
    # Key #2
    # html/body/table[1]/tbody/tr[2]/td[1]
    # Value #2
    # html/body/table[1]/tbody/tr[2]/td[2]
    # ...
    # Key # 27
    # html/body/table[1]/tbody/tr[27]/td[1]
    # Value # 27
    # html/body/table[1]/tbody/tr[27]/td[2]
    xBanner = "html/body/h1[3]"


    settingsPage = "http://{}/settings.php".format(baseURL)
    bnw.loadPage(settingsPage)
    time.sleep(2)
    bannerText = bnw.textFromElement(xBanner)
    if bannerText == "DONTEXIST":
        print("Unable to load the game global settings page")
        exit(1)
    elif not bannerText == "Game Settings":
        print("Unexpected banner text: {}, was looking for 'Game Settings'".format(bannerText))
        exit(1)
    if debug:
        print("Game Settings page successfully loaded")

    gameSettings = {}

    for settingNumber in range(1, 28):
        keyXpath   = "html/body/table[1]/tbody/tr[{}]/td[1]".format(settingNumber)
        valueXpath = "html/body/table[1]/tbody/tr[{}]/td[2]".format(settingNumber)
        keyText = bnw.textFromElement(keyXpath)
        valueText = bnw.textFromElement(valueXpath)
        keyText = keyText.strip()
        valueText = valueText.strip()
        if keyText == "DONTEXIST" or valueText == "DONTEXIST":
            print("Unable to retrieve the key value for settings #{}".format(settingNumber))
            exit(1)

        # remove commas from numbers
        valueText = valueText.replace(',', '')
        gameSettings[keyText] = valueText

    if debug:
        print("DONE Parsing the settings page")
    return gameSettings
