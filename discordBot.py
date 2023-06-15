import datetime
import discord
import random
import discordDefs
import time
import re
#import mysql.connector

runningOnPi = 1 # if .env error, check errors. try setting this to 0 some python installations need the full path.
#runningOnPi = int(input('Is this running on the pi? 1 for yes 0 for no.'))

games = ['$rps','$rr','$doot','$noot','$roll','$math','$pickle','$depickle']
possibleChoices = ['rock','paper','scissors','lizard','spock']
paperWeakness = ['Scissors','Lizard']
rockWeakness = ['Paper','Spock']
lizardWeakness = ['Rock','Scissors']
spockWeakness = ['Lizard','Spock']
scissorsWeakness = ['Spock','Rock']
computerChoice = []
global userChoice
userChoice = []
fired = 1
spin = 0
global chamber
chamber = 0
global revolverCapacity
revolverCapacity = 6


#when on pi just use x = open("data.env", 'rt')
if runningOnPi == 1:
    x = open("data.env", 'rt')
else:
    x = open("Python/discordBot/data.env", 'rt')
dotenv = x.readlines(0)
discordToken = dotenv[0]
randomToken = dotenv[1]
mysqlUserName = dotenv[2]
mysqlPassword = dotenv[3]
mysqlAddress = dotenv[4]
mysqlDatabase = dotenv[5]

x.close()

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    global fired
    global spin
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    if message.content.startswith('$help'):
        await message.channel.send('Available commands are: {}'.format(games))

    if message.content.startswith('$rps'):
        #await message.channel.send(message.content)
        splitString = message.content.split()
        splitString.append('')
        userChoice = splitString[1].lower()
        
        if userChoice in possibleChoices:
            computerChoice = discordDefs.generateComputerChoice()
            winner = discordDefs.determineWinner(userChoice,computerChoice)
            print('test')
            if winner == 'player':
                await message.channel.send('You won!')
                discordDefs.updateScores(message.author,runningOnPi)
            if winner == 'computer':
                await message.channel.send('You lost :(')
                discordDefs.updateScores('computer',runningOnPi)
            if winner == 'tie':
                await message.channel.send('It was a tie.')
            await message.channel.send('Computer chose: {}.'.format(computerChoice))
        else:
            options = ' '.join(possibleChoices)
            await message.channel.send('Select one from this list: {}\nChoose using $rps followed by the selection.'.format(options))
            return

    if message.content.startswith('$rr'):
        global chamber
        global revolverCapacity
        splitString = message.content.split()
        splitString.append('')
        containsDigit = re.findall('\d',splitString[1])
        if containsDigit: 
            revolverCapacity = int(splitString[1]) - 1
            await message.channel.send('Revolver capacity set to {}'.format(revolverCapacity + 1))
            fired = 1
            return
        if revolverCapacity < 0 or revolverCapacity > 30:
            await message.channel.send('You broke the laws of physics and the physics police have come to stop you. Bang.\nResetting physics.')
            await message.author.move_to(None)
            #await message.author.timeout(datetime.timedelta(5),'You are dead.')
            revolverCapacity = 6
            fired = 1
            return
        if fired == 1:
            spin = 0
            fired = 0
            chamber = random.randint(0,revolverCapacity)
            await message.channel.send('You pick up the revolver from the hands of the dead body in front of you. You reload it, give the cylinder a spin, and pull the trigger.')
        if chamber == spin:
            #await message.author.move_to(None)
            await message.channel.send('bang')
            #await message.author.timeout(datetime.timedelta(5),'You are dead.')
            fired = 1
        
        else:
            await message.channel.send(f'click\n\nYou collectively have tempted fate {spin + 1} time(s).')
            spin += 1

    if message.content.startswith('$doot'):
        #channel = message.author.voice.channel
        #vc = await channel.connect()
        #vc.play(discord.FFmpegPCMAudio(executable="/ec2-user/ffmpeg.exe", source='ec2-user/skullsound2.mp3'))
        #time.sleep(1)        
        #await message.guild.voice_client.disconnect()
        await message.channel.send('doot')
        discordDefs.updateScores('dootCounter',runningOnPi)
        if runningOnPi == 1:
            counter = open('scores/{}.txt'.format('dootCounter'),'r')
            numberOfDoots = counter.readlines(0)
            await message.channel.send('{} collective doots.'.format(numberOfDoots[0]))
    
    if message.content.startswith('$noot'):
        #channel = message.author.voice.channel
        #vc = await channel.connect()
        #vc.play(discord.FFmpegPCMAudio(executable="/ec2-user/ffmpeg.exe", source='ec2-user/skullsound2.mp3'))
        #time.sleep(1)        
        #await message.guild.voice_client.disconnect()
        await message.channel.send('NOOT NOOT')
        discordDefs.updateScores('nootCounter',runningOnPi)
        if runningOnPi == 1:
            counter = open('scores/{}.txt'.format('nootCounter'),'r')
            numberOfDoots = counter.readlines(0)
            await message.channel.send('{} collective noots.'.format(numberOfDoots[0]))

    if message.content.startswith('$math'):
        splitString = message.content.split()
        splitString.append('')
        await message.channel.send(splitString)
        mathVar1 = int(splitString[1])
        mathVar2 = int(splitString[3])
        if splitString[2] == '*': await message.channel.send(mathVar1 * mathVar2)
        if splitString[2] == '/': await message.channel.send(mathVar1 / mathVar2)
        if splitString[2] == '+': await message.channel.send(mathVar1 + mathVar2)
        if splitString[2] == '-': await message.channel.send(mathVar1 - mathVar2)

    if message.content.startswith('$mysql'):
        #discordDefs.mysqlScoreUpdater(mysqlUserName,mysqlPassword,mysqlAddress,mysqlDatabase)
        await message.channel.send('Not implemented yet.')

    if message.content.startswith('$pickle'):
        tempString = ''
        splitString = message.content.split()
        splitString.append('')
        print(splitString)
        if splitString[1] == 'help':
            await message.channel.send('$pickle @{}\nPlease pickle responsibly.'.format(message.author))
        else:            
            for char in splitString[1]:
                if char == '<': continue
                elif char == '>': continue
                elif char == '@': continue
                else: tempString += char
            discordDefs.updateScores(tempString,runningOnPi)
        if runningOnPi == 1:
            scores = open('scores/{}.txt'.format(tempString),'r')
        else:
            scores = open('Python/discordBot/scores/{}.txt'.format(tempString),'r')
        count = scores.readlines(0)
        print(count[0])
        if count[0] == '1' or count[0] == '-1':
            await message.channel.send('{} has been pickled {} time.'.format(splitString[1],count[0]))
        else:
            await message.channel.send('{} has been pickled {} times.'.format(splitString[1],count[0]))

    if message.content.startswith('$depickle'):
        tempString = ''
        splitString = message.content.split()
        splitString.append('')
        print(splitString)
        if splitString[1] == 'help':
            await message.channel.send('$depickle @{}\nPlease pickle responsibly.'.format(message.author))
        else:            
            for char in splitString[1]:
                if char == '<': continue
                elif char == '>': continue
                elif char == '@': continue
                else: tempString += char
            discordDefs.updateScores('{}pickle'.format(tempString),runningOnPi,1)
        if runningOnPi == 1:
            scores = open('scores/{}.txt'.format(tempString),'r')
        else:
            scores = open('Python/discordBot/scores/{}pickle.txt'.format(tempString),'r')
        count = scores.readlines(0)
        print(count[0])
        if count[0] == '1' or count[0] == '-1':
            await message.channel.send('{} has been pickled {} time.'.format(splitString[1],count[0]))
        else:
            await message.channel.send('{} has been pickled {} times.'.format(splitString[1],count[0]))

    if '(╯°□°)╯︵ ┻━┻' in message.content:
        await message.channel.send('NO TABLE FLIPPING\n┬─┬ノ( º _ ºノ)')

client.run(discordToken)
