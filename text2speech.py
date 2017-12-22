import re, sys
from playsound import playsound
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

NUM_0_9  = {0:'Zero',1:'One',2:'Two',3:'Three',4:'Four',5:'Five',6:'Six',7:'Seven',8:'Eight',9:'Nine'}
NUM_TEEN = {0:'Ten',1:'Eleven',2:'Twelve',3:'Thirteen',4:'Fourteen',5:'Fifteen',6:'Sixteen',7:'Seventeen',8:'Eightteen',9:'Nineteen'}
NUM_TENS = ['Ten','Twenty','Thirty','Fourty','Fifty','Sixty','Seventy','Eighty','Ninety']
NUM_DIG  = ['Hundred','Thousand','Million','Billion','Trillion','Quadrillion']
ALL_NUMBERS = []

PATTERN = re.compile('(?:/audio/lunawav/)(.*?)(?:\.ogg)')
BASE_AUDIO_URL = "http://static.sfdict.com/audio/"
BASE_AUDIO_EXT = ".mp3"

def play_sound(link):
	if link:
		playsound(link)

def play_numb_audio(number):
	places = len(number) // 3
	for n in number:
		play_word_audio(NUM_0_9.get(int(n)))

def play_word_audio(word):
	try:
		content = urlopen('http://www.dictionary.com/browse/%s?s=t' % word).read()
	except HTTPError as error:
		content = error.read()
	result  = re.search( PATTERN, str(content) )
	if result:
		play_sound(BASE_AUDIO_URL + str(result.group(1)) + BASE_AUDIO_EXT)
	
def play_parse_word(word):
	word = ''.join(w for w in word if w.isalnum())
	if word.isalpha():
		return play_word_audio(word)
	elif word.isnumeric():
		return play_numb_audio(str(int(word)))
	else:
		print("invalid word: %s" % word)
		return None

def work_phrase():
	phrase = input("Enter text (q! to quit): ")
	if phrase == 'q!':
		sys.exit()
	for word in phrase.split():
		print(word)
		play_parse_word(word)
	work_phrase()
		
if __name__ == '__main__':
	work_phrase()
	