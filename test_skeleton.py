import support_lib as bnw
import add_player as addp
import parse_config as parser
import email_poller as email
import login_player as login
import options as options
import player_status as status
import trade_route as trade
import retrieve_settings as settings
import port_handler as port

import time
import random
from tinydb import TinyDB, Query
# a rudimentary testing framework for bot creation

# Compute the cost of an upgrade
def upgradeCost(desiredvalue,currentvalue):
    DeltaCost = 0
    Delta = desiredvalue - currentvalue
    while Delta > 0:
        DeltaCost = DeltaCost + (2 **  (desiredvalue - Delta))
        Delta = Delta - 1

    DeltaCost = DeltaCost * 1000
    return DeltaCost


# This routine attempts to move the player to Zero within the allotted move limit
# returns the updated sector db
def gotoSectorZero(maxMoves, warpDB):
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
        warpDB[inSector] = warps
        if inSector == 0:
            return [True, warpDB]
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
    return [False, warpDB]

# This routine attempts to navigate the supplied sectors
# returns True if it succeeds, False if it is unable to comply
def moveVia(path):
    print('moveVia called with path: {}'.format(path))
    for eachSector in path:
        print("moveVia is attempting to move to sector: {}".format(eachSector))
        if not bnw.moveTo(eachSector):
            print("Was unable to move to the desired sector: {}".format(eachSector))
            return False
    # assume we made it
    return True

# a wrapper for the shortest path finder which strips off the first element (unless None)
# since it is always the current sector the ship is in
def find_shortest_path(graph, start, end):
    shortPath = find_path_shortest(graph, start, end)
    if shortPath != None:
        shortPath.pop(0)
    return shortPath

# A rudimentary shortest path calculator
# found here:  https://www.python.org/doc/essays/graphs/
def find_path_shortest(graph, start, end, path=[]):
    debug = False
    if path ==[]:
        # initial entry into the function
        if debug:
            print("Trying to find path from {} to {}".format(start, end))
    else:
        # function called itself
        if debug:
            print("Recursively - path is now: {}".format(path))
    path = path + [start]
    if start == end:
        return path
    if not start in graph:
        return None
    shortest = None
    for node in graph[start]:
        if node not in path:
            newpath = find_path_shortest(graph, node, end, path)
            if newpath:
                if not shortest or len(newpath) < len(shortest):
                    shortest = newpath
    return shortest

# search for and create an initial trade route
# this route will NOT verify it is unique!
def initialRoute(warpDB):
    oreSector = -1
    goodsSector = -1
    portSector = {}
    distanceBeforeSearching = 10
    zeroMove = gotoSectorZero(100, warpDB)
    inZero = False
    if zeroMove[0]:
        print("Made it to sector Zero")
        inZero = True
    else:
        print("Starting Route search from where ever we are...")
    warpDB = zeroMove[1]

    if inZero:
        beenThere = []
        print("#######\n##########\nAttempting to move {} sectors away from Zero before looking for a trade route".format(distanceBeforeSearching))
        while True:
            playerStatus = status.getStatus()
            print("Player Status:")
            print(playerStatus)
            availableWarps = playerStatus['warps']
            while True:
                # select a random warp
                randomIndex = random.randint(0, len(availableWarps) - 1)
                randomWarp = availableWarps[randomIndex]
                print('Considering jumping to: {}'.format(randomWarp))
                if randomWarp in beenThere:
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
            warpDB[randomWarp] = availableWarps
            beenThere.append(randomWarp)
            # if we ended up back in port 0, reset beenThere!
            if randomWarp == "0":
                print('Ended up back in 0, resetting beenThere')
                beenThere = []
            currentPath = find_shortest_path(warpDB, randomWarp, '0')
            if currentPath == None:
                print("Went through a one way warp - we're lost!".format(randomWarp))
                break
            howFar = len(currentPath)
            print("We are now {} jumps from zero".format(howFar))
            if howFar >= 10:
                print("That's far enough!")
                break
            else:
                print("Still need to move further away!")

    print("Starting search for a trade route")
    searchResults = trade.tradeRouteSearch(warpDB, 100)
    print("searchResults: {}".format(searchResults))
    searchStatus = searchResults[0]
    if searchStatus != "SUCCESS":
        print("Failed to find a trade route")
        exit(1)
    else:
        # ['SUCCESS', tradeRoutes, warpDB]
        tradeRoutes = searchResults[1]
        warpDB = searchResults[2]
        return [warpDB, tradeRoutes]

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
        chgPassResults = options.changePasswd(serverPass, playerPassword,)

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
            chgPassResults = options.changePasswd(serverPass, playerPassword)

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

# The above needs to be refactored and cleaned up.
# a player object with login credentials, and it logs itself in?


# create a player DB reference based on the name of the bot
db = TinyDB("{}.db".format(playerName))
warpsTable = db.table('warps')
warpDB = warpsTable.all()
print("length of warpDB: {} ".format(len(warpDB)))

# retrieve the warpDB if present
if len(warpDB):
    print("Retrieving saved Warp DB")
    warpDB = warpDB[0]
else:
    print("Initializing a new Warp DB")
    warpDB = {}
    numberOfSectors = int(gameSettings['Number of Sectors'])
    print("Creating an empty sector warp lookup table, {} sectors worth".format(numberOfSectors))
    for sectorNumber in range(1, numberOfSectors + 1):
        warpDB[str(sectorNumber)] = []


# Main game loop starts here

goals = {"planets": 10, "credits": 10000000000, "techLevel": 20, "traderoutes": 10 }
planetGoal = False
creditsGoal = False
techGoal = False
tradeGoal = False

tradeRoutes = trade.retrieveRoutes()
print('Established trade routes: {}'.format(tradeRoutes))
numRoutes = len(tradeRoutes)
if numRoutes >= goals["traderoutes"]:
    tradeGoal = True

print("Trying to retrieve player status")
playerStatus = status.getStatus()

print("Player Status:")
print(playerStatus)
turnsLeft = playerStatus["turnsLeft"]

currentSector = playerStatus['currentSector']
print("Player is currently in sector {}".format(currentSector))

availableWarps = playerStatus['warps']
warpDB[currentSector] = availableWarps

planetStatus = status.getPlanetStatus()
numPlanets = len(planetStatus)
if numPlanets >= goals["planets"]:
    planetGoal = True

playerCredits = playerStatus["credits"]
if playerCredits >= goals["credits"]:
    creditsGoal = True

shipStatus = status.getShipStatus()
print(shipStatus)
playerTech = shipStatus["Average tech level"]
if playerTech >= goals["techLevel"]:
    techGoal = True

print("Player has {} planets, desired number of planets: {}, goal met: {}".format(numPlanets, goals["planets"], planetGoal))
print("Player has {} credits, desired number of credits: {}, goal met: {}".format(playerCredits, goals["credits"], creditsGoal))
print("Player has {} average tech level, desired average tech level: {}, goal met: {}".format(playerTech, goals["techLevel"], techGoal))
print("Player has {} trade routes established, target number of routes: {}, goal met: {}".format(numRoutes, goals["traderoutes"], tradeGoal))
print("ship status")
print(shipStatus)

if not tradeGoal:
    needRoutes = goals["traderoutes"] - numRoutes
    print("Attempting to establish {} trade routes".format(needRoutes))
    if numRoutes == 0:
        print("Working on initial trade route")
        #return [warpDB, tradeRoutes]
        createResults = initialRoute(warpDB)
        warpDB = createResults[0]
        tradeRoutes = createResults[1]
        numRoutes = len(tradeRoutes)

    for routeNumber in range(numRoutes+1, 11):
        print("Working on trade route #{}".format(routeNumber))
        searchResults = trade.tradeRouteSearch(warpDB, 100)
        print("searchResults: {}".format(searchResults))
        searchStatus = searchResults[0]
        if searchStatus != "SUCCESS":
            print("Failed to find a trade route")
            exit(1)
        else:
            print("Successfully established a new trade route!")
            # ['SUCCESS', tradeRoutes, warpDB]
            tradeRoutes = searchResults[1]
            warpDB = searchResults[2]

tradeRoutes = trade.retrieveRoutes()
numRoutes = len(tradeRoutes)
turnsLeft = playerStatus["turnsLeft"]

# Examine our established trade routes
shortestRoute = 9999
startRoute = 9999
directPath = False
routeId = -1
currentSector = playerStatus['currentSector']
print("Our current sector is: {}".format(currentSector))

for routeId in tradeRoutes:
    currentRoute = tradeRoutes[routeId]
    port1 = currentRoute["port1"]
    port2 = currentRoute["port2"]
    print("Current Sector: {}, Examining Trade Route Id {},  {} <=> {}".format(currentSector, routeId, port1, port2))
    # handle the case where we are sitting on a trade route
    if currentSector == port1 or currentSector == port2:
        shortestRoute = 0
        directPath = True
        bestRouteId = routeId
        break
    else:
        shortestPath = find_shortest_path(warpDB, currentSector, port1)
        if not shortestPath == None:
            print("There is no direct path to the start of the Trade Route")
            distance = len(shortestPath)
            print("Trade Route via direct path is {} turns away".format(distance))
            print("direct path: {}".format(shortestPath))
            if distance < shortestRoute:
                shortestRoute = distance
                directPath = True
                bestRouteId = routeId
        else:
            print("Querying indirect path to trade route start")
            indirectDistance = int(trade.queryIndirectPath(currentSector, port1)[0])
            print("Trade Route via indirect path is {} turns away".format(indirectDistance))
            if indirectDistance < shortestRoute:
                shortestRoute = indirectDistance
                directPath = False
                bestRouteId = routeId

theRoute = tradeRoutes[bestRouteId]
print("Selected Trade Route Id {}, starting at port {}, which is {} moves away".format(bestRouteId, theRoute["port1"], shortestRoute))
if shortestRoute == 0:
    print("Ship is already there")
else:
    if shortestRoute > turnsLeft:
        print("Not enough turns left to travel to start of trade route.")
        print("This is where we would log out for a while")
        exit(1)

    if directPath:
        print("Traveling to the start of the trade route")
        shortestPath = find_shortest_path(warpDB, currentSector, theRoute["port1"])
        if moveVia(shortestPath):
            print('Successfully moved to start of trade route, sector: {}'.format(theRoute["port1"]))
        else:
            print('Something happened attempting to move to start of trade route, sector: {}'.format(theRoute["port1"]))
            exit(1)
    else:
        print("Using a realspace jump to the start of the trade route")
        if trade.queryIndirectPath(currentSector, theRoute["port1"], True):
            print("Jump succeeded!")
        else:
            print("Something unhandled happended during the Real Space jump...")
            exit(1)


print("At this point, we should be ready to run the trade route and make some credits!")
playerStatus = status.getStatus()
print("Player Status:")
print(playerStatus)
currentSector = playerStatus['currentSector']
print("Player is currently in sector {}".format(currentSector))
turnsLeft = playerStatus["turnsLeft"]
print("Warp Database")
print(warpDB)

print("trade routes: {}".format(tradeRoutes))


print("Saving the warpDB")
warpsTable.insert(warpDB)
print("Saving the trade route DB")
warpsTable.insert(tradeRoutes)

print("current trade routes")
print(tradeRoutes)

# determine how many times we can execute the trade - if less than 25
if turnsLeft < 25 * theRoute["distance"]:
    maxTrades = int(turnsLeft / theRoute["distance"])
    print("Can perform a maximum of {} trades".format(maxTrades))
else:
    maxTrades = 25
print("Need to start executing trade route Id: {}".format(bestRouteId))
trade.executeTrade(bestRouteId, maxTrades, True)
shipStatus = status.getShipStatus()
print("ship status")
print(shipStatus)
playerStatus = status.getStatus()
turnsLeft = playerStatus["turnsLeft"]

# Calculate the upgrade cost prior to attempting to buy them
currentHull     = shipStatus["Hull"]
currentEngines  = shipStatus["Engines"]
currentPower    = shipStatus["Power"]
currentComputer = shipStatus["Computer"]
currentSensors  = shipStatus["Sensors"]
currentArmor    = shipStatus["Armor"]
currentShields  = shipStatus["Shields"]
currentBeams    = shipStatus["Beam Weapons"]
currentTorpedo  = shipStatus["Torpedo launchers"]
currentCloak    = shipStatus["Cloak"]



hullCost = upgradeCost(currentHull + 1, currentHull)
engineCost = upgradeCost(currentEngines + 1, currentEngines)
powerCost  = upgradeCost(currentPower + 1, currentPower)
computerCost = upgradeCost(currentComputer + 1, currentComputer)
sensorsCost = upgradeCost(currentSensors + 1, currentSensors)
armorCost = upgradeCost(currentArmor + 1, currentArmor)
shieldsCost = upgradeCost(currentShields + 1, currentShields)
beamsCost = upgradeCost(currentBeams + 1, currentBeams)
torpedoCost = upgradeCost(currentTorpedo + 1, currentTorpedo)
cloakCost = upgradeCost(currentCloak + 1, currentCloak)

print("Current Hull tech: {}, cost to upgrade: {}".format(currentHull, hullCost))
print("Current Engine tech: {}, cost to upgrade: {}".format(currentEngines, engineCost))
print("Current Power tech: {}, cost to upgrade: {}".format(currentPower, powerCost))
print("Current Computer tech: {}, cost to upgrade: {}".format(currentComputer, computerCost))
print("Current Sensors tech: {}, cost to upgrade: {}".format(currentSensors, sensorsCost))
print("Current Armor tech: {}, cost to upgrade: {}".format(currentArmor, armorCost))
print("Current Shields tech: {}, cost to upgrade: {}".format(currentShields, shieldsCost))
print("Current Beams tech: {}, cost to upgrade: {}".format(currentBeams, beamsCost))
print("Current Torpedo tech: {}, cost to upgrade: {}".format(currentTorpedo, torpedoCost))
print("Current Cloak tech: {}, cost to upgrade: {}".format(currentCloak, cloakCost))

shoppingList = {}

shoppingList["Hull"] = str(currentHull + 1)
shoppingList["Engines"] = str(currentEngines + 1)
shoppingList["Power"] = str(currentPower + 1)
shoppingList["Computer"] = str(currentComputer + 1)
shoppingList["Sensors"] = str(currentSensors + 1)
shoppingList["Armor"] = str(currentArmor + 1)
shoppingList["Shields"] = str(currentShields + 1)
shoppingList["Beam Weapons"] = str(currentBeams + 1)
shoppingList["Torpedo launchers"] = str(currentTorpedo + 1)
shoppingList["Cloak"] = str(currentCloak + 1)


totalCost = hullCost + engineCost + powerCost + computerCost + sensorsCost + armorCost + shieldsCost + beamsCost + torpedoCost + cloakCost
if totalCost > playerStatus['credits']:
    print("Cost for upgrades: {}, Credits available: {}".format(totalCost, playerStatus['credits']))
    print("Not enough credits for the upgrades")
    exit(1)

else:
    print("Returning to Sector Zero to make some purchases")
    shortestPath = find_shortest_path(warpDB, currentSector, '0')
    if shortestPath != None:
        print("Best Path to sector 0")
        print(shortestPath)
        print('Using the new "moveVia" function')
        # remove the first sector, which is where we are currently
        if moveVia(shortestPath):
            print('Successfully moved to sector 0!')
        else:
            print('Something happened attempting to move to sector 0')
            exit(1)

    else:
        print('There is no known path from {} to sector 0'.format(currentSector))
        print('Attempting to move player to sector 0 starting position')
        returnStatus = gotoSectorZero(100, warpDB)
        passOrFail = returnStatus[0]
        warpDB = returnStatus[1]
        print("Found Sector Zero: {}".format(passOrFail))
        if not passOrFail:
            print('Was unable to find sector zero - aborting')
            exit(1)

    print("Now in sector Zero - attempting to make a purchase")

    print("shopping list: {}".format(shoppingList))

    purchaseResults = port.specialPort(shoppingList)
    howMuch = purchaseResults[1]
    if purchaseResults[0] == "SUCCESS":
        print("Purchase was successful, cost was: {}".format(howMuch))
    else:
        print("Could not afford the purchase")
        creditsAvailable = purchaseResults[2]
        print("Purchase cost: {}, Credits available: {}, Difference: {}".format(howMuch, creditsAvailable, howMuch - creditsAvailable))
        exit(1)
exit(1)

# Need to evaluate turns remaining prior to attempting jumps
