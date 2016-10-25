import support_lib as bnw
import time
# 2016/09/06 - Original version

# This handles the supported game options
# Currently, only user language and changing their password

def changePasswd(currentPass, newPass):
    debug = True
    # xpaths
    xCurrentPass = "html/body/form/table/tbody/tr[2]/td[2]/input"
    xNewPass     = "html/body/form/table/tbody/tr[3]/td[2]/input"
    xConfirmPass = "html/body/form/table/tbody/tr[4]/td[2]/input"
    xSaveButton  = "html/body/form/input"
    xBanner      = "html/body/h1"
    xWholePage   = "html/body"

    # retrieve the current page
    currentPage = bnw.getPage()
    baseURL = ('/').join(currentPage.split('/')[:-1])
    print("baseURL: {}".format(baseURL))
    optionPage = "{}/options.php".format(baseURL)
    print("optionPage: {}".format(optionPage))
    bnw.loadPage(optionPage)
    time.sleep(2)
    bannerText = bnw.textFromElement(xBanner)
    if bannerText == "DONTEXIST":
        print("Unable to load the options page")
        exit(1)
    elif not bannerText == "Options":
        print("Unexpected banner text: {}, was looking for 'Options'".format(bannerText))
        exit(1)
    if debug:
        print("Option page successfully loaded")

    print("Attempting to change the player password")

    if not bnw.fillTextBox(xCurrentPass, currentPass):
        if debug:
            print('Unable to fill in the player current password')
        return ['ERROR', 'Current Password XPath Error']

    if not bnw.fillTextBox(xNewPass, newPass):
        if debug:
            print('Unable to fill in the player new password')
        return ['ERROR', 'New Password XPath Error']

    if not bnw.fillTextBox(xConfirmPass, newPass):
        if debug:
            print('Unable to fill in the player confirm password')
        return ['ERROR', 'Confirm Password XPath Error']

    if debug:
        print("Attempting to submit the changes")

    if not bnw.clickButton(xSaveButton):
        if debug:
            print('Unable to click the Save button')
        return ['ERROR', 'Save Button Error']

    saved = False
    # determine if the update succeeded or not
    # have to examine the entire page text
    if bnw.elementExists(xWholePage):
        wholePageText = bnw.textFromElement(xWholePage)
    else:
        print("Was not able to extract all text from the option change")
        exit(1)

    if "Password changed." in wholePageText:
        print("Password has been successfully changed")
        return ["SUCCESS", ""]
    else:
        return ['ERROR', 'Could not change password']
