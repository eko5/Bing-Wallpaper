# Autor			Piotr Filipek
# Email			danoxide@outlook.com
# Data wydania	17 września 2015

import json, urllib2, os

# Klasa, która pobiera aktualne tło ze strony
# wyszukiwarki Bing i ustawia jako tło pulpitu.
class BingBackground:
	domain = "http://www.bing.com%s" # główna domena
	data = domain % "/HPImageArchive.aspx?format=js&idx=0&n=1&mkt=en-US" # adres z którego pobierane są informacje

	def __init__(self):
		# print self.command % 'filename.jpg'
		imgurl = self.domain % self.getJSON()['images'][0]['url']
		imgname = imgurl.split('/')[-1]
		target = self.save(imgurl, imgname)
		self.setAsWallpaper(target)

	# Pobiera informacje ze strony Bing w postaci JSON
	def getJSON(self):
		return json.load(urllib2.urlopen(self.data))

	# Ustawia pobrany obraz jako tło pulpitu
	def setAsWallpaper(self, fileurl):
		# os.system("chmod +r %s" % fileurl)
		os.system(self.command % fileurl)
		print 'gsettings set org.gnome.desktop.background picture-uri "%s"' % fileurl

	# Zapisuje aktualnie używany obraz tła ze strony Bing
	def save(self, url, filename, directory='wallpapers'):
		imgfile = urllib2.urlopen(url)
		target = '%s/%s/%s' % (os.path.dirname(os.path.abspath(__file__)), directory, filename)
		output = open(target, 'wb')
		output.write(imgfile.read())
		output.close()
		return target

bb = BingBackground()