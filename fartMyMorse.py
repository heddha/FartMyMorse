import sys


# before doing anything, check whether the function receives the correct amount of arguments

def makeTitleValid(title):
    if (not ".mp4" in title):
        title = title + ".mp4"
    return title


def getSentenceAndTitle():
    if (len(sys.argv) == 3):
        sentence = sys.argv[1]
        title = makeTitleValid(sys.argv[2])
        return sentence, title
    else:
        print("\nDude, wrong arguments! Call the function like this: \n\n    python3 fartMyMorse.py SENTENCE TITLE\n")
        sys.exit(0)


mySentence, myTitle = getSentenceAndTitle()



# once sentence and title were obtained, start the actual program!

from morseAlphabet import letters
from moviepy.editor import *
import random


# bind picture of short and long farts to the duration they're supposed to have.

shortfartpic = ImageClip('resources/farting.png', duration=1)
longfartpic = shortfartpic.set_duration(3)



# bind pictures for the break to durations of breaks

shortbreak = ImageClip('resources/notfarting.png', duration=1)
intermediatebreak = shortbreak.set_duration(2)
longbreak = shortbreak.set_duration(4)


# import four different short fart sounds, then put them into an array (length of the array doesn't matter, as long as it contains at least one element)

shortfart1 = AudioFileClip('resources/fart1.mp3')
shortfart2 = AudioFileClip('resources/fart2.mp3')
shortfart3 = AudioFileClip('resources/fart3.mp3')
shortfart4 = AudioFileClip('resources/fart4.mp3')
shortfartarray = [shortfart1, shortfart2, shortfart3, shortfart4]


# import four different long fart sounds, then put them into an array (length of the array doesn't matter, as long as it contains at least one element)

longfart1 = AudioFileClip('resources/longfart1.mp3')
longfart2 = AudioFileClip('resources/longfart2.mp3')
longfart3 = AudioFileClip('resources/longfart3.mp3')
longfart4 = AudioFileClip('resources/longfart4.mp3')
longfartarray = [longfart1, longfart2, longfart3, longfart4]


# getAudio returns a random audio file, depending on the length requested. Options are 1 and 0; 0 returns a one-second audio file, 1 returns a 3-second audio sample.

def getAudio(size):
    if (size == 0):
        return random.choice(shortfartarray)
    elif (size == 1):
        return random.choice(longfartarray)
    else:
        print("incorrect input size. choose 1 or 0")


def combineAudioAndPic(length):
    if (length == "."):
        clip = shortfartpic.set_audio(getAudio(0))
    elif (length == "_"):
        clip = longfartpic.set_audio(getAudio(1))
    return clip


# retrieves the letters from morseAlphabet.py
def getLetter(letter):
    return letters[letter]


#returns an array with clips of all morse-encoded parts of a letter. The array has  only to be concatenated using the concatenate_videoclips(array) option. A 1-second bread is added between every letter. In the end, a 2-second break is added, as the break between 2 letters is 3 seconds long.

def translateLetter(letter):
    morse = getLetter(letter)
    videoarray = []
    for i in morse:
        videoarray.append(combineAudioAndPic(i))
        videoarray.append(shortbreak)
    videoarray.append(intermediatebreak)
    return videoarray



#translates a whole word to morse. in the end, the function appends a 4-second break, as the duration between 2 words is 7 seconds, and the translateLetter-function ends on a 3-second break.
def translateWord(word):
    videoarray = []
    for letter in word:
        translatedLetter = translateLetter(letter)
        videoarray+=translatedLetter
    videoarray.append(longbreak)
    return videoarray


# translates a whole sentence divided by spaces into morse. no special characters allowed. all allowed characters can be seen in morseAlphabet.py.
def translateSentence(sentence):
    videoarray = []
    splitSentence = sentence.split(" ")
    for word in splitSentence:
        translatedWord= translateWord(word)
        videoarray+=translatedWord
    return videoarray



# shifts the whole input to lowercase.
def makeValid(word):
    return word.lower()



# puts everything together. change title of output file at will.
def makeMovie(sentence, title):
    safesentence = makeValid(sentence)
    translatedsentence = translateSentence(safesentence)
    final = concatenate_videoclips(translatedsentence) 
    final.write_videofile(title, fps=1, audio=True)


def finalise():
    makeMovie(mySentence, myTitle)


finalise()

