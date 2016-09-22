from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import Select
import re
import time
from selenium.webdriver.common.keys import Keys

# url open is a little convoluted
try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen



# this is needed to squelch the overly verbose debug logs
import logging
from selenium.webdriver.remote.remote_connection import LOGGER

LOGGER.setLevel(logging.WARNING)
# attempting to get to the bottom of the alert object


# This routine is used to fill in simple text boxes
# returns True if it succeeded, False otherwise
# 2016/02/05 - Updated to convert dictionaries into strings, since "send_keys" can't handle dictionaries...
def fillTextBox(xpath, text):
    debug = False
    if debug:
        print("fillTextBox sez text received: {} and its type: {}".format(text, type(text)))
    # massage our data into a simple string
    if type(text) == dict:
        if debug:
            print("Attempting to convert a dictionary to a string")
        text = str(text)
    elif type(text) == list:
        if debug:
            print("Attempting to convert a list to a string")
        text = text[0]
    if type(text) == int:
        if debug:
            print("Attempting to convert an int to a string")
        text = str(text)
    else:
        if debug:
            print("Passing text through as-is")

    if not elementExists(xpath):
        print("fillTextBox sez, specified xpath does not exist!")
        return False
    else:
        # there has been issues where the input data was appended to the old data
        # so we need to be 100% sure what we end up with is what was specified.
        while True:
            element = driver.find_element_by_xpath(xpath)
            # oldContents should eventually contain the desired text
            # in which case, it will short circuit the change attempt and return
            oldContents = element.get_attribute('value')
            if debug:
                print("oldContents = {}".format(oldContents))
            if not oldContents == text:
                if debug:
                    # need to erase the current contents of the input field
                    print("oldContents:  {}, text: {}".format(oldContents, text))
                    print("Erasing the current contents of the input field")
                element.send_keys(Keys.CONTROL + "a");
                time.sleep(1)
                element.send_keys(Keys.DELETE);
                time.sleep(1)
                if debug:
                    print("Typing into text field: {}".format(text))
                # try typing something in it
                if debug:
                    print("entering: {}".format(text))
                element.send_keys(text)
                time.sleep(1)
                # back to the top to check our work
                continue
            else:
                if debug:
                    print("Input contents match target")
                return True

# simple routine that clicks a button
def clickButton(xpath):
    if not elementExists(xpath):
        return False
    elem = driver.find_element_by_xpath(xpath)
    elem.click()
    return True


# check and see if a check box is checked or not
def isChecked(xpath):
    if not elementExists(xpath):
        print("isChecked says the specified checkbox does not exist: {}".format(xpath))
        exit(1)
    if driver.find_element_by_xpath(xpath).is_selected():
        return True
    else:
        return False


# if needed
# http://stackoverflow.com/questions/14442636/how-can-i-check-if-a-checkbox-is-checked-in-selenium-python-webdriver

# This routine is used to toggle checkboxes
# requires a checkbox Id and the requested state (True = Checked, False = not Checked)
# returns False if it detects an error, True if it thinks it succeeded
def checkBox(checkBoxId, state):
    debug = False
    # Get the current status of the checkbox
    if not elementExists(checkBoxId):
        print("Did not find the check Box")
        return False

    elem = driver.find_element_by_id(checkBoxId)
    checked = elem.get_attribute("checked")
    # retrieve the status of the checkbox, and morph it to either True (checked) or False (not checked)
    # if not checked, checked will be set to the 'NoneType'
    if checked is None:
        # we override that to the more familiar "False"
        checked = False
    else:
        if checked == "true":
            checked = True
        else:
            print("Unsupported value for 'checked' - aborting!")
            exit(1)

    # if state is True, the box is supposed to be checked
    if state:
        if not checked:
            # it's not...
            time.sleep(1)
            # click it...
            driver.execute_script("arguments[0].click()", elem)
        else:
            # it is set - so we do nothing...
            if debug:
                print("The checkbox is already selected...")
    else:
        # in this case, the checkbox is NOT supposed to be checked
        if checked:
            # it IS though - so we attempt to un-check it
            time.sleep(1)
            # click it
            driver.execute_script("arguments[0].click()", elem)
        else:
            if debug:
                print("The checkbox is already de-selected...")

    # assume all went well
    return True


# simple brute force check for an element via selenium
# if it does not exist, we cause an exception...
def elementExists(target):
    #print("Executing elementExists")
    # if we encounter a stale element, we need to make sure we try again
    while True:
        try:
            driver.find_element_by_xpath(target)
            # if this is executing - the element exists, and everything is good
            return True

        except NoSuchElementException:
            # This means it was not found via xPath - so now we try via Id
            try:
                driver.find_element_by_id(target)
                # element exists - everything is good
                return True

            except NoSuchElementException:
                # two strikes and we are out for now
                return False

        except StaleElementReferenceException:
            # if this is executing, no idea if the element exists, but the reference was stale...
            # so we need to go around again.
            #print("elementExists caught StaleElementReferenceException")
            time.sleep(1)

# a routine to check if the specified text exists anywhere on the page
# good when minimal formatting is being used
def textExists(theText):
    pageSrc = driver.page_source
    m = re.search(theText, pageSrc)
    if m:
        return True
    else:
        return False

# a routine that returns the text from an element if it exists, otherwise 'DONTEXIST'
# assumes it is being passed an xpath
# 2016/02/24 - added stale element exception protection
def textFromElement(xpath):
    #print("Checking on xpath: {}".format(xpath))
    while True:
        try:
            # first - verify it actually exists
            if not elementExists(xpath):
                print("elementExists says the xpath does not exist")
                return "DONTEXIST"
            elem = driver.find_element_by_xpath(xpath)
            text = elem.text
            return text
        except StaleElementReferenceException:
            print("textFromElement caught a stale element exception, trying again in 2 seconds")
            time.sleep(2)
            continue

# set the browser window size
def setWindowSize(height, width):
    driver.set_window_size(height, width)

# what window size is the browser set to?
def getWindowSize():
    return driver.get_window_size()


# simple routine to allow the caller to shut down the browser
def killBrowser():
    if type(driver) == str:
        print("Browser was not launched..")
    else:
        print("Killing browser")
        driver.close()

# simple routine to start the browser if needed
# 2016/07/19 - handle self signed certs
def startBrowser(browser="firefox"):
    global driver

    if browser != "firefox" and browser != "chrome":
        print("browser: {} is not supported - sorry".format(browser))
        exit(1)
    print("Firing up a browser: {}".format(browser))

    if browser == "firefox":
        profile = webdriver.FirefoxProfile()
        profile.accept_untrusted_certs = True
        driver = webdriver.Firefox(firefox_profile=profile)
        return
    else:
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        driver = webdriver.Chrome(chrome_options=options, executable_path="/usr/local/bin/chromedriver", service_args=["--verbose", "--log-path=/tmp/chrome.log"])
        #driver = webdriver.Chrome()
        return

# central routine for loading a specified page, returns nothing
def loadPage(pageToLoad):
    driver.get(pageToLoad)

# Returns the current input value from a text box
def inputValue(xpath):
    if not elementExists(xpath):
        return "ERROR"
    else:
        element = driver.find_element_by_xpath(xpath)
        currentContents = element.get_attribute('value')
        return currentContents

# returns the currently selected value from a selector
# http://stackoverflow.com/questions/30872786/how-to-get-selected-option-using-selenium-webdriver-with-python
def selectedValue(xpath):
    if not elementExists(xpath):
        return "ERROR"
    else:
        select = Select(driver.find_element_by_xpath(xpath))
        selected_option = select.first_selected_option
        return selected_option.text

# bog standard selector
# http://stackoverflow.com/questions/7867537/selenium-python-drop-down-menu-option-value
def selectDropDownNew(labelXPath, selection):
    if elementExists(labelXPath):
        while True:
            try:
                select = Select(driver.find_element_by_xpath(labelXPath))
                # select by visible text
                select.select_by_visible_text(selection)
                break
            except Exception as ex:
                exType = str(type(ex))
                print("We caught an exception of type: %s" % exType)
                print("selectDropDownNew caught an exception - trying again in 3")
                print("The selection is: {}".format(selection))
                time.sleep(3)
        return True
    else:
        return False

# Attempt to move the player ship to the designated adjoining sector
def moveTo(newSector):
    xInSector = "html/body/table[1]/tbody/tr[3]/td[1]/span"

    debug = True
    if debug:
        print('moveTo is attempting to move to sector: {}'.format(newSector))
    # determine the current base URL
    currentPage = getPage()
    baseURL = ('/').join(currentPage.split('/')[:-1])
    moveToURL = "{}/move.php?sector={}".format(baseURL, newSector)
    driver.get(moveToURL)
    # now, query our current sector
    currentSector = textFromElement(xInSector)
    if currentSector == "DONTEXIST":
        print("The current sector xpath is incorrect")
        exit(1)

    if currentSector == newSector:
        return True
    else:
        if debug:
            print("Wanted sector: {}, ended up in sector: {}".format(newSector, currentSector))
        return False

# returns the current page
def getPage():
    currentPage = driver.current_url
    return currentPage



################### end of functions #######################

if __name__ == '__main__':
    print("Loaded as a main script - probably not what you wanted to do.")
    exit(1)
else:
    # create a placeholder for the driver if we need to launch a browser
    driver = ""
    # our headless display flag
    headless = False
