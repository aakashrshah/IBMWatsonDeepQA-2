import requests
import sys
from bs4 import BeautifulSoup
import os

def exportToFile(title,tupleoftags):

	if os.path.exists("test"):
		os.chdir("test")

		#Write to files
		test = open(title,'w')

		for a,b in tupleoftags:
			test.write("Point:")
			test.write(str(a))
			test.write("\n")
			test.write("Counterpoint:")
			test.write(str(b))
			test.write('\n')

		test.close()
		os.chdir("..")

	if os.path.exists("gold"):
		os.chdir("gold")

		#Write to files
		test = open(title,'w')

		for i in range(0,((len(tupleoftags)*2)-1),2):
			test.write(str(i+1))
			test.write('\t')
			test.write(str(i+1+1))
			test.write('\n')

		test.close()
		os.chdir("..")

def scrape(fileid,soup):
	typetags = soup.find_all('div',class_="field field-type-text field-field-point-type")
	pointtags = soup.find_all('div',class_="field field-type-text field-field-point")
	counterpointtags = soup.find_all('div',class_="field field-type-text field-field-counterpoint")
	counter_tags = []
	point_tags = []
	
	for i,tag in enumerate(typetags):
		if tag.text.strip() == 'Against':
			continue
		elif len(typetags) == len(pointtags) and len(typetags) == len(counterpointtags):
			point_tags.append(u' '.join(pointtags[i].find('p').text.strip().split()))
			counter_tags.append(u' '.join(counterpointtags[i].find('p').text.strip().split()))
			tupleoftags = tuple(zip(point_tags,counter_tags))
			exportToFile(str(fileid),tupleoftags)
		else:
			print("Length problem with ID: ",fileid)
			continue


	


def main():
	urlfile = str(sys.argv[1])
	f = open(urlfile,"r").readlines()
	for line in f:
		fileid = line.split('/')
		fileid = fileid[len(fileid)-1].strip()
		page = requests.get(line.strip())
		soup = BeautifulSoup(page.content,'html.parser')
		scrape(fileid,soup)
		print(line.strip()+" Done!")



if __name__ == "__main__":
	main()

