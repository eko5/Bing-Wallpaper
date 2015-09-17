# Author         Piotr Filipek
# Email          danoxide@outlook.com
# Release date   17 september 2015

import json, urllib2, os

# Class that download current wallpaper from the Bing
# site and sets its as a desktop wallpaper.
class BingBackground:
	domain = "http://www.bing.com%s"
	data = domain % "/HPImageArchive.aspx?format=js&idx=0&n=1&mkt=en-US"

	def __init__(self):
		# print self.command % 'filename.jpg'
		imgurl = self.domain % self.getJSON()['images'][0]['url']
		imgname = imgurl.split('/')[-1]
		target = self.save(imgurl, imgname)
		self.setAsWallpaper(target)

	# Download informations from the Bing site in JSON
	def getJSON(self):
		return json.load(urllib2.urlopen(self.data))

	# Set downloaded picture as a wallpaper
	def setAsWallpaper(self, fileurl):
		# os.system("chmod +r %s" % fileurl)
		os.system('gsettings set org.gnome.desktop.background picture-uri "file://%s"' % fileurl)

	# Save current Bing wallpaper
	def save(self, url, filename, directory='wallpapers'):
		imgfile = urllib2.urlopen(url)
		target = '%s/%s/%s' % (os.path.dirname(os.path.abspath(__file__)), directory, filename)
		output = open(target, 'wb')
		output.write(imgfile.read())
		output.close()
		return target

# Run application
bb = BingBackground()