import support_lib as bnw
import time

# 2016/09/02 - Original version

# This routine attempts to log a player into the specified game
def login(email, password, gameURL):
    debug = True
    # xpaths
    xEmail       = ".//*[@id='email']"
    xPassword    = ".//*[@id='pass']"
    xBadLogin    = "html/body/h1"
    xLoginButton = "html/body/div[6]/form/div[2]/input"
    xTurnsLeft   = "html/body/table[1]/tbody/tr[1]/td[1]/span"
    xInSector    = "html/body/table[1]/tbody/tr[3]/td[1]/span"
    xFunds       = "html/body/table[1]/tbody/tr[1]/td[1]/span"
    xScore       = "html/body/table[1]/tbody/tr[1]/td[3]/span"
    xSectorType  = "html/body/table[1]/tbody/tr[3]/td[3]/a"
    xSectorPort  = "html/body/table[2]/tbody/tr/td[2]/div[1]"
    xSectorPort  = "html/body/table[2]/tbody/tr/td[2]/div[1]/span"
    xPageBanner  = "html/body/div[6]/h1"
    xWholePage   = "html/body"

    if debug:
        print("Attempting to load the player login page")
    loginPage = 'http://{}'.format(gameURL)

    bnw.loadPage(loginPage)
    bannerText = bnw.textFromElement(xPageBanner)
    if not bannerText == 'Welcome to Blacknova Traders!':
        if debug:
            print('Unable to load the login page - bad URL?')
        return ['ERROR', 'Bad URL']

    if not bnw.fillTextBox(xEmail, email):
        if debug:
            print('Unable to fill in the player email address')
        return ['ERROR', 'E-Mail XPath Error']

    if not bnw.fillTextBox(xPassword, password):
        if debug:
            print('Unable to fill in the new player ship name')
        return ['ERROR', 'Ship Name XPath Error']

    if not bnw.clickButton(xLoginButton):
        if debug:
            print('Unable to click the LOGIN button')
        return ['ERROR', 'LOGIN Button Error']

    # Keep looping till either we log in, or get an error
    while True:
        if bnw.elementExists(xTurnsLeft):
            break
        if bnw.elementExists(xBadLogin):
            badText = bnw.textFromElement(xBadLogin)
            if badText == "Login Phase Two":
                if debug:
                    print("Problem with the login credentials")
                wholePageText = bnw.textFromElement(xWholePage)
                if "The password you entered is incorrect" in wholePageText:
                    return ['ERROR', 'Incorrect Password']
                if "No Such Player" in wholePageText:
                    return ['ERROR', "No Such Player"]
        time.sleep(1)

    print("Looks like we logged in!")
    return ("SUCCESS", "")
