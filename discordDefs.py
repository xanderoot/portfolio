import os
import random
import requests
#import mysql.connector 


possibleChoices = ['Rock','Paper','Scissors','Lizard','Spock','End the game']
paperWeakness = ['Scissors','Lizard']
rockWeakness = ['Paper','Spock']
lizardWeakness = ['Rock','Scissors']
spockWeakness = ['Lizard','Spock']
scissorsWeakness = ['Spock','Rock']
computerChoice = []
userChoice = []
computerScore = 0
playerScore = 0
gameRunning = True

def generateComputerChoice():
    while True:
        computerChoice = possibleChoices[random.randint(0,len(possibleChoices) - 1)]
        if computerChoice == 'End the game': 
            continue
        else: 
            break
    return computerChoice

def determineWinner(userChoice, computerChoice):
    victor = ''
    if userChoice == 'rock':
        if computerChoice == 'Paper' or computerChoice == 'Spock':
            #print('You Lose. Computer chose: {}.'.format(computerChoice))
            victor = 'computer'
        elif computerChoice == 'Rock':
            #print('It is a tie.')
            victor = 'tie'
    if userChoice == 'paper':
        if computerChoice == 'Scissors' or computerChoice == 'Lizard':
            #print('You Lose. Computer chose: {}.'.format(computerChoice))
            victor = 'computer'
        elif computerChoice == 'Paper':
            #print('It is a tie.')
            victor = 'tie'
    if userChoice == 'scissors':
        if computerChoice == 'Spock' or computerChoice == 'Rock':
            #print('You Lose. Computer chose: {}.'.format(computerChoice))
            victor = 'computer'
        elif computerChoice == 'Scissors':
            #print('It is a tie.')
            victor = 'tie'
    if userChoice == 'lizard':
        if computerChoice == 'Rock' or computerChoice == 'Scissors':
            #print('You Lose. Computer chose: {}.'.format(computerChoice))
            victor = 'computer'
        elif computerChoice == 'Lizard':
            #print('It is a tie.')
            victor = 'tie'
    if userChoice == 'spock':
        if computerChoice == 'Lizard' or computerChoice == 'Paper':
            #print('You Lose. Computer chose: {}.'.format(computerChoice))
            victor = 'computer'
        elif computerChoice == 'Spock':
            #print('It is a tie.')
            victor = 'tie'
    if userChoice == 'End the game':
        print('Game done, exiting program.')
    
    if victor == '':
        return 'player'
    if victor == 'computer':
        return 'computer'
    if victor == 'tie':
        return 'tie'

def updateScores(playerName,runningOnPi,remove = 0):
    try:
        
        if runningOnPi == 1:
            scores = open('scores/{}.txt'.format(playerName),'r')
        else:
            scores = open('Python/discordBot/scores/{}.txt'.format(playerName),'r')
    except:
        if runningOnPi == 1:
            scores = open('scores/{}.txt'.format(playerName),'x')
        else:
            scores = open('Python/discordBot/scores/{}.txt'.format(playerName),'x')
        scores.write('0')
        if runningOnPi == 1:
            scores = open('scores/{}.txt'.format(playerName),'r')
        else:
            scores = open('Python/discordBot/scores/{}.txt'.format(playerName),'r')
    playerTempScore = int(scores.read())
    if runningOnPi == 1:
        scores = open('scores/{}.txt'.format(playerName),'w')
    else:
        scores = open('Python/discordBot/scores/{}.txt'.format(playerName),'w')
    if remove == 1:
        playerTempScore -= 1
    else:
        playerTempScore += 1
    scores.write(str(playerTempScore))
    scores.close()

def randomJsonRequest(diceNumber,diceType,apiKey):
    jsonResponse = requests.post('https://api.random.org/json-rpc/4/invoke', json={
    "jsonrpc": "2.0",
    "method": "generateIntegers",
    "params": {
        "apiKey": apiKey,
        "n": diceNumber,
        "min": 1,
        "max": diceType,
        "base": 10
    },
    "id": 19185
    })
    #print(f"Status Code: {jsonResponse.status_code}, Response: {jsonResponse.json()}")
    return jsonResponse.json()['result']['random']['data']

def diceDecode(diceInput):
    characters = []
    splitValue = diceInput.split('d')
    #print(splitValue)
    return splitValue
    #for letter in diceInput:
        #characters.append(letter)

'''
def mysqlScoreUpdater(userName,password,host,database): #,userToUpdate
    global cursor
    try:
        global cnx
        cnx = 0
        cnx = mysql.connector.connect(
            user = userName,
            password = password,
            host = host,
            database = database,
            port = 3306)
        print(cnx)
    except mysql.connector.Error as err:
        print('Error connecting to database.')
    cursor = cnx.cursor()
    testQuery = ('select * from userScores')
    cursor.execute(testQuery)
    print(cursor)

    cnx.close()
'''