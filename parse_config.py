import os

# This routine reads the blacknova.config file
def readConfig(configName):
    if not os.path.isfile(configName):
        return ['ERROR', 'Config file not found']

    # bulk read the contents of the configuration file
    with open(configName, 'r') as fileHandle:
        raw_data = fileHandle.read()
        fileHandle.closed
    processed = parseConfig(raw_data)
    return ['SUCCESS', processed]

# this routine parses the config data it is passed
def parseConfig(configData):
    debug = False
    parsed = {}
    if debug:
        print('parseConfig received:')
        print(configData)
        print("Splitting non-comments")
    for currentLine in configData.split('\n'):
        stripped = currentLine.strip()
        if len(stripped) == 0 or currentLine.strip()[0] == "#":
            continue
        if debug:
            print('currentLine ==> {}'.format(currentLine))
        (cfgKey, cfgValue) = stripped.split(':')
        cfgKey = cfgKey.strip()
        cfgValue = cfgValue.strip()
        if len(cfgKey) == 0 or len(cfgValue) == 0:
            continue
        parsed[cfgKey] = cfgValue
    if debug:
        print('parseConfig dict output')
        print(parsed)
    return parsed

if __name__ == '__main__':
    print("Loaded as a main script - probably not what you wanted to do.")
    exit(1)
