import websocket
import time
import json
import datetime
import requests

def runWS():
    ws = websocket.WebSocket();

    while True:
        try:
            ws.connect("wss://chat-gateway-dev.iceposeidon.com/socketcluster/")
            print('Successfully connected to websocket.')
            break;
        except(TimeoutError):
            print('Error connecting to websocket.')

        time.sleep(1)
        print('Reattempting connection to server...')

    ws.send('{"event":"#handshake","data":{"authToken":null},"cid":1}')
    ws.send('{"event":"#subscribe","data":{"channel":"yell"},"cid":2}')

    return ws

def logToFile(openedFile, message):
    openedFile.write(message + '\r\n')
    openedFile.flush()

def getMessage(rawData):
    jsonData = json.loads(rawData)

    if jsonData["event"] == "#publish" and jsonData["data"]["data"]["t"] == "ccm": #ccm used for chat
        timestamp = str(datetime.datetime.now().time()).split(".")[0]
        username = jsonData["data"]["data"]["u"]
        message = jsonData["data"]["data"]["c"]
        return timestamp, username, message

def checkPingPong(rawData):
    if rawData == '#1':
        ws.send('#2')

logMode = False

if __name__ == "__main__":
    ws = runWS() #Initialize and check websocket

    if logMode == True:
        logFile = open("log.txt", "a+", encoding='utf-8')

    while True: #Main loop
        dataRecv = ws.recv()

        checkPingPong(dataRecv)
        if dataRecv.startswith('{"event'): #Check if data is a message
            timestamp, username, message = getMessage(dataRecv)
            finalMessage = '[' + timestamp + '] ' + username + ': ' + message
            print(finalMessage)

            if logMode == True: #Log if logmode enabled
                logToFile(logFile, finalMessage)
        time.sleep(0.01)