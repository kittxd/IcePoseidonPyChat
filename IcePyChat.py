'''
    Author: Kitt
    Python Version: 3.6.3
'''

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

def getMessage(jsonData):
        timestamp = str(datetime.datetime.now().time()).split(".")[0]
        username = jsonData["data"]["data"]["u"]
        message = jsonData["data"]["data"]["c"]
        return timestamp, username, message

def sendMessage(username, message):
    ws.send('{"event":"chat","data":"{\"t\":\"ccm\",\"u\":\"CxTester\",\"c\":\"test2\"}"}')
def checkPingPong(rawData):
    if rawData == '#1':
        ws.send('#2')

logMode = False
authMode = False
authToken = ""

if __name__ == "__main__":
    ws = runWS() #Initialize and check websocket

    if logMode == True:
        logFile = open("log.txt", "a+", encoding='utf-8')

    while True: #Main loop
        dataRecv = ws.recv()

        try: #Checks if data passed is JSON
            jsonData = json.loads(dataRecv)
            if "event" in jsonData and jsonData["event"] == "#publish" and jsonData["data"]["data"]["t"] == "ccm": #ccm used for chat
                timestamp, username, message = getMessage(jsonData)
                finalMessage = '[' + timestamp + '] ' + username + ': ' + message
                print(finalMessage)
                if logMode == True: #Log if logmode enabled
                    logToFile(logFile, finalMessage)
        except(ValueError):
            checkPingPong(dataRecv)
        time.sleep(0.01) #Added to optimise performance