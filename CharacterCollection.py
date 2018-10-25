import urllib2
from bs4 import BeautifulSoup
from bs4.diagnose import diagnose
from urllib2 import Request, urlopen
from bs4.element import Comment
from bs4 import SoupStrainer

"""
This script is used to generate a file for each of the top 300 most mentioned charcaters in the 
A Song of Ice and Fire novels. The file is then populated with the info found on the 
characters respective Wiki page. 

Created by Patrick Gibson
"""

"""
This function is used to help textFromHtml strip the the HTML tags 
"""
def tagVisible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


"""
This function is used to seperate the tags and other HTML junk and return only the visible text seen on the webpage
"""
def textFromHtml(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visibleTexts = filter(tagVisible, texts)  
    return u" ".join(t.strip() for t in visibleTexts).encode('utf-8')


"""
This function writes the page info for every character to its own seperate text file 
"""
def writePageInfo(name, link):
	req = Request(link, headers={'User-Agent': 'Mozilla/5.0'}) 
	webpage = urlopen(req).read()
	justText = textFromHtml(webpage)
	file = open("Characters Pages/" + name + '.txt', "w")
	file.write(justText)


#get names for only top 300 characters
with open('top 300.txt') as file:
	top300 = file.read().splitlines()

#get only links for characters 
mainPage = 'https://awoiaf.westeros.org'
charListPage = mainPage + '/index.php/List_of_characters'
req = Request(charListPage, headers={'User-Agent': 'Mozilla/5.0'}) #did not have access without this 
webpage = urlopen(req).read()
soup2 = BeautifulSoup(webpage, 'html.parser')
tag = soup2.find_all('li')

#Loop begins at first character, and subsequently checks each character to see if they are in the top 300.
#If they are, a file is created, their Wiki page info is added, and they are removed from the top300 list. 
flag = 1 
for each in tag:
	if (each.a.string == 'Abelar Hightower'): #beginning of characters
		flag = 0
	elif (each.a.string == "Characters"): #end of characters
		break

	if (flag == 0 and (each.a.string in top300) ):
		link = mainPage + each.a["href"]
		writePageInfo(each.a.string, link)
		top300.remove(each.a.string)
for stuff in top300:
	print stuff

#Some of the names in the top300 list are not the same as they are listed on the wiki. I check which characters
#are still in the list, and manually add their name and link. This was quicker than changing their names on the 
#top300 list. 
name = ''
print ('Enter "done" for name when finished')
while 1:
	name = raw_input('Enter name of missing character: ')
	link = raw_input('Enter link for missing character: ')
	if name == 'done':
		break
	writePageInfo(name, link)
		












