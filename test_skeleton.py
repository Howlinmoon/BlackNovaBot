import support_lib as bnw
import add_player as addp
import parse_config as parser
import email_poller as email
import login_player as login
import options as options
import player_status as status
import scan_sector as scanner
import trade_route as route
import time
import random
import retrieve_settings as settings

# a rudimentary testing framework for bot creation


# This routine starts searching for an optimal trade route from the
# current sector.
# if it finds one, it returns True, otherwise, it gives up and returns False
# Pass it how many warps MAX to use (default maximum is 100), and your current Warps To Zero list

def tradeRouteSearch(zeroPath, sectorDB, maxTurns = 100):
    debug = True
    oreSector = -1
    goodsSector = -1
    portSector = {}
    warpsUsed = 0
    while True:
        if warpsUsed >= maxTurns:
            if debug:
                print("Exceeded allotted turns")
                return ["FAILED", sectorDB, zeroPath]

        if debug:
            print("Trying to retrieve player status")
        playerStatus = status.getStatus()
        warps = playerStatus['warps']
        currentSector = playerStatus['currentSector']
        intWarps = [int(i) for i in warps]
        sectorDB[int(currentSector)] = intWarps

        # Is the player ship in a sector with an Ore or Goods port?
        currentPort = playerStatus['sectorPort']
        if debug:
            print("currentPort: {}".format(currentPort))
        if currentPort != "Ore" and currentPort != "Goods":
            if debug:
                print("Current sector: {} does not have a desired port - need to move".format(currentSector))
            # need to find the next available sector that is higher than the current one
            for newSector in warps:
                if int(newSector) < int(currentSector):
                    continue
                else:
                    break

            if debug:
                print("Attempting to move to sector: {}".format(newSector))
            if not bnw.moveTo(newSector):
                print("Was unable to move to the desired sector: {}".format(newSector))
                exit(1)
            else:
                if debug:
                    print("Successfully moved to the desired sector")
                zeroPath.append(newSector)
                warpsUsed += 1
                continue

        else:
            if debug:
                print("Current sector has a desired port!")
            portSector[currentPort] = int(currentSector)

            if currentPort == "Ore":
                oreSector = int(currentSector)
                needPort = "Goods"
            else:
                goodsSector = int(currentSector)
                needPort = "Ore"

            if debug:
                print("Checking to see if a neighboring sector contains a trading match")
            warps = playerStatus['warps']

            for currentWarp in warps:
                scanResults = scanner.lrScan(currentWarp)
                if debug:
                    print("Scan Results for Sector: {} is: {}".format(currentWarp, scanResults))
                sectorDB[currentWarp] = scanResults

                if scanResults['port'] == needPort:
                    if debug:
                        print('Found a possible {} port: {}'.format(needPort, currentWarp))
                    # does this warp allow return to this sector?
                    if not currentSector in scanResults['links']:
                        if debug:
                            print('{} Port has no return link to the current sector'.format(needPort))
                        continue
                    else:
                        if debug:
                            print('{} Port has a return link to the current sector'.format(needPort))
                            print("Attempting to move to {} sector: {}".format(needPort, currentWarp))
                        if not bnw.moveTo(currentWarp):
                            print("Was unable to move to the desired sector")
                            exit(1)
                        else:
                            warpsUsed += 1
                            if debug:
                                print("Successfully moved to the desired sector")
                            portSector[needPort] = int(currentWarp)
                            playerStatus = status.getStatus()
                            warps = playerStatus['warps']
                            currentSector = playerStatus['currentSector']
                            intWarps = [int(i) for i in warps]
                            sectorDB[int(currentSector)] = intWarps

                            if debug:
                                print("Should be able to setup a traderoute between")
                                print("Goods Port: {} and Ore Port: {}".format(portSector["Goods"], portSector["Ore"]))
                            prevSector = zeroPath[-1]
                            if debug:
                                print("Returning to previous sector:{} ".format(prevSector))
                            if not bnw.moveTo(prevSector):
                                print("Was unable to move to the previous sector: {}".format(prevSector))
                                exit(1)
                            warpsUsed += 1

                            print("Found a Trade Route!")
                            # Return stuff here
                            return ['SUCCESS', portSector, sectorDB, zeroPath]

            if oreSector == -1 or goodsSector == -1:
                print("Did not find a matching pair - continuing to look")
                oreSector = -1
                goodsSector = -1
                # need to find the next available sector that is higher than the current one
                # should handle the situation where the next sector in numerical order, only
                # leads back to the current one!

                for newSector in warps:
                    newLinks = sectorDB[newSector]['links']
                    if int(newSector) < int(currentSector):
                        continue
                    else:
                        print("considering moving to sector: {}".format(newSector))
                        print("it has links to: {}".format(newLinks))
                        # verify at least one of the links isn't back to here...
                        goodCheck = False
                        for linkCheck in newLinks:
                            if linkCheck != currentSector:
                                print("Found at least one link to someplace other than current sector")
                                goodCheck = True

                        if not goodCheck:
                            print("We have a problem, search algo would send us back to the current sector!")
                            exit(1)
                        # otherwise, we good to go with this new sector
                        break

                print("Attempting to move to sector: {}".format(newSector))
                if not bnw.moveTo(newSector):
                    print("Was unable to move to the desired sector")
                    exit(1)
                else:
                    print("Successfully moved to the desired sector")
                    zeroPath.append(newSector)
                    warpsUsed += 1
                    playerStatus = status.getStatus()
                    warps = playerStatus['warps']
                    currentSector = playerStatus['currentSector']
                    intWarps = [int(i) for i in warps]
                    sectorDB[int(currentSector)] = intWarps
                    continue

# This routine attempts to move the player to Zero within the allotted move limit
# returns the updated sector db
def gotoSectorZero(maxMoves, sectorDB):
    print('gotoSectorZero called with maxMoves: {}'.format(maxMoves))
    # Get player status - pull out current sector
    # if current sector == 0, return True
    # if not, move to the lowest warp
    # return to top
    while maxMoves > 0:
        playerStatus = status.getStatus()
        inSector = playerStatus['currentSector']
        warps = playerStatus['warps']
        intWarps = [int(i) for i in warps]
        sectorDB[int(inSector)] = intWarps
        if inSector == "0":
            return [True, sectorDB]
        # attempt to move to the first available warp, which will be the closest to zero (theoretically)
        if len(warps) == 0:
            print('We are in a dead end!')
            exit(1)
        newSector = warps[0]
        print("gotoSectorZero is attempting to move to sector: {}".format(newSector))
        if not bnw.moveTo(newSector):
            print("Was unable to move to the desired sector: {}".format(newSector))
            exit(1)
        maxMoves = maxMoves - 1
    print('Ran out of moves in gotoSectorZero')
    return [False, sectorDB]



###########################################################
## MAIN ENTRY
##
###########################################################

parseResults = parser.readConfig('blacknova.config')
parseStatus = parseResults[0]
if not parseStatus == 'SUCCESS':
    print("Error parsing the config file: {}".format(parseResults[1]))
    exit(1)

parseDict = parseResults[1]
print('parseDict: {}'.format(parseDict))

# fire up the browser
bnw.startBrowser("chrome")

print("You have 4 seconds to move the browser before it is used.")
time.sleep(4)

# createPlayer(playerEmail, playerName, playerPassword, shipName, gameURL)
playerEmail = parseDict['UserEmailAddress']
playerName = parseDict['PlayerName']
playerPassword = parseDict['PlayerPassword']
shipName = parseDict['ShipName']
gameURL = parseDict['baseURL']

print("playerEmail: {}".format(playerEmail))
print("playerName: {}".format(playerName))
print("playerPassword: {}".format(playerPassword))
print("Ship Name: {}".format(shipName))
print("Base Game URL: {}".format(gameURL))

print('Retrieving the game settings')
gameSettings = settings.getSettings(gameURL)
print("Retrieved game settings")
print(gameSettings)
print("Trying to login with the supplied credentials")
loginResults = login.login(playerEmail, playerPassword, gameURL)
if not loginResults[0] == "SUCCESS":
    errorMsg = loginResults[1]
    print("Error logging in with the supplied credentials: {}".format(errorMsg))
    if errorMsg == "No Such Player":
        print("Need to create player...")
        addResults = addp.createPlayer(playerEmail, playerName, shipName, gameURL)
        print('addResults: {}'.format(addResults))
        tries = 5
        while True:
            print("Checking for password, tries remaining: {}".format(tries))
            passwordDict = email.pollEmail('blacknova.config')
            if playerEmail in passwordDict:
                serverPass = passwordDict[playerEmail]
                print("We received a server password: {}".format(serverPass))
                break
            else:
                tries = tries - 1
                if tries > 0:
                    print('No password yet, waiting 30 seconds before trying again')
                else:
                    print("Email problem?  Need to use the password resend link")
                    print("not implemented - yet!")
                    exit(1)

        print("Now attempting to login the newly created player")
        loginResults = login.login(playerEmail, serverPass, gameURL)

        if not loginResults[0] == "SUCCESS":
            print("Ran into a credentials issue attempting to login as: {} with password: {}".format(playerEmail, serverPass))
            exit(1)

        print("Logged in - now to change the password...")
        chgPassResults = options.changePasswd(serverPass, playerPassword, gameURL)

        if not chgPassResults[0] == "SUCCESS":
            print("Was unable to change the player password")
            exit(1)

        print("Player password has been changed!")
        # end up at the normal main page
        mainPage = 'http://{}/main.php'.format(gameURL)
        bnw.loadPage(mainPage)


    elif errorMsg == 'Incorrect Password':
        print("Checking for server password")
        passwordDict = email.pollEmail('blacknova.config')
        if playerEmail in passwordDict:
            serverPass = passwordDict[playerEmail]
            print("We received a server password: {}".format(serverPass))
            loginResults = login.login(playerEmail, serverPass, gameURL)

            if not loginResults[0] == "SUCCESS":
                print("Ran into a credentials issue attempting to login as: {} with password: {}".format(playerEmail, serverPass))
                exit(1)

            print("Logged in - now to change the password...")
            chgPassResults = options.changePasswd(serverPass, playerPassword, gameURL)

            if not chgPassResults[0] == "SUCCESS":
                print("Was unable to change the player password")
                exit(1)

            print("Player password has been changed!")
            # end up at the normal main page
            mainPage = 'http://{}/main.php'.format(gameURL)
            bnw.loadPage(mainPage)
        else:
            print("Supplied password is incorrect, need to request a resend")
            print("not implemented - yet!")
            exit(1)

    else:
        print("Unsupported error...")
        exit(1)

print("Player should now be logged in!")

# Main game loop starts here
sectorDB = {}
numberOfSectors = int(gameSettings['Number of Sectors'])
print("Creating an empty sector warp lookup table, {} sectors worth".format(numberOfSectors))
for sectorNumber in range(1, numberOfSectors + 1):
    sectorDB[sectorNumber] = []


print("Trying to retrieve player status")
playerStatus = status.getStatus()

print("Player Status:")
print(playerStatus)

currentSector = playerStatus['currentSector']
print("Player is currently in sector {}".format(currentSector))
availableWarps = playerStatus['warps']
# we just want ints - not strings
intWarps = [int(i) for i in availableWarps]
sectorDB[int(currentSector)] = intWarps
if currentSector != '0':
    print('Attempting to move player to sector 0 starting position')
    returnStatus = gotoSectorZero(100, sectorDB)
    passOrFail = returnStatus[0]
    sectorDB = returnStatus[1]
    print("Found Sector Zero: {}".format(passOrFail))
    if not passOrFail:
        print('Was unable to find sector zero - aborting')
        exit(1)

# at this point, the bot is in sector zero
warpsFromZero = []
oreSector = -1
goodsSector = -1
portSector = {}
distanceBeforeSearching = 10


print("#######\n##########\nAttempting to move {} sectors away from Zero before looking for a trade route".format(distanceBeforeSearching))
for moved in range(0, distanceBeforeSearching):
    playerStatus = status.getStatus()
    print("Player Status:")
    print(playerStatus)
    availableWarps = playerStatus['warps']
    while True:
        # select a random warp
        randomIndex = random.randint(0, len(availableWarps) - 1)
        randomWarp = availableWarps[randomIndex]
        print('Considering jumping to: {}'.format(randomWarp))
        if randomWarp in warpsFromZero:
            print("Already been to {}, picking another".format(randomWarp))
            continue
        else:
            break
    print("Performing a random jump to: {}".format(randomWarp))
    if not bnw.moveTo(randomWarp):
        print("Was unable to move to the desired sector: {}".format(randomWarp))
        exit(1)
    playerStatus = status.getStatus()
    availableWarps = playerStatus['warps']
    intWarps = [int(i) for i in availableWarps]
    sectorDB[int(randomWarp)] = intWarps
    warpsFromZero.append(randomWarp)
    # if we ended up back in port 0, reset warpsFromZero!
    if randomWarp == "0":
        print('Ended up back in 0, resetting warpsFromZero')
        warpsFromZero = []

print("Starting search for a trade route from: {}".format(randomWarp))

searchResults = tradeRouteSearch(warpsFromZero, sectorDB, 100)
print("searchResults: {}".format(searchResults))
searchStatus = searchResults[0]
if searchStatus != "SUCCESS":
    print("Failed to find a trade route")
    exit(1)
else:
    # ['SUCCESS', portSector, sectorDB, zeroPath]
    print("Attempting to create the trade route linkage")
    portDict = searchResults[1]
    sectorDb = searchResults[2]
    warpsFromZero = searchResults[3]
    currentSector = warpsFromZero[-1]
    port1 = currentSector
    goodsPort = portDict['Goods']
    orePort = portDict['Ore']
    if goodsPort == int(currentSector):
        port2 = orePort
    elif orePort == int(currentSector):
        port2 = goodsPort
    else:
        print('Whoah! - Something is wrong here...')
        exit(1)

    trCreateStatus = route.createRoute(port1, port2, bidir=True , warp=True)
    if trCreateStatus:
        print("Successfully created a trade route!")
    else:
        print("Was unable to create the specified trade route")

print("warps from zero")
print(warpsFromZero)

print("Sector Database")
print(sectorDB)

print("Stopping")
exit(1)
