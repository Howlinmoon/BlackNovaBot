import support_lib as bnw
import time

# 2016/08/31 - Original version

# This routine attempts to add a player to the specified game
def createPlayer(playerEmail, playerName, shipName, gameURL):
    debug = True
    # xpaths
    xEmailAddress = 'html/body/form/dl/dd[1]/input'
    xShipName     = 'html/body/form/dl/dd[2]/input'
    xPlayerName   = 'html/body/form/dl/dd[3]/input'
    xPageBanner   = 'html/body/h1'
    xSubmitButton = 'html/body/form/div/input[1]'
    if debug:
        print("Attempting to load the new player entry page")
    newPlayerPage = 'http://{}/new.php'.format(gameURL)

    bnw.loadPage(newPlayerPage)
    bannerText = bnw.textFromElement(xPageBanner)
    if not bannerText == 'Create New Player':
        if debug:
            print('Unable to load the create new player page - bad URL?')
        return ['ERROR', 'Bad URL']

    if not bnw.fillTextBox(xEmailAddress, playerEmail):
        if debug:
            print('Unable to fill in the new player email address')
        return ['ERROR', 'E-Mail XPath Error']

    if not bnw.fillTextBox(xShipName, shipName):
        if debug:
            print('Unable to fill in the new player ship name')
        return ['ERROR', 'Ship Name XPath Error']

    if not bnw.fillTextBox(xPlayerName, playerName):
        if debug:
            print('Unable to fill in the new player name')
        return ['ERROR', 'Player Name XPath Error']

    if not bnw.clickButton(xSubmitButton):
        if debug:
            print('Unable to click the new player submit button')
        return ['ERROR', 'Submit Button Error']

    time.sleep(3)
    bannerText = bnw.textFromElement(xPageBanner)
    if not bannerText == 'Create New Player Phase Two':
        if debug:
            print('Error entering new player info?')
        return ['ERROR', 'Bad Player Info']

    print('Password must have been sent...')