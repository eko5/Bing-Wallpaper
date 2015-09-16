import json, urllib2, os

class BingBackground:
	domain = "http://www.bing.com%s"
	command = 'gsettings set org.gnome.desktop.background picture-uri "%s"'
	data = domain % "/HPImageArchive.aspx?format=js&idx=0&n=1&mkt=en-US"

	def __init__(self):
		# print self.command % 'filename.jpg'
		imgurl = self.domain % self.getJSON()['images'][0]['url']
		imgname = imgurl.split('/')[-1]
		target = self.save(imgurl, imgname)
		self.setAsWallpaper(target)

	def getJSON(self):
		return json.load(urllib2.urlopen(self.data))

	def setAsWallpaper(self, fileurl):
		# os.system("chmod +r %s" % fileurl)
		os.system(self.command % fileurl)
		print 'gsettings set org.gnome.desktop.background picture-uri "%s"' % fileurl

	def save(self, url, filename, directory='wallpapers'):
		imgfile = urllib2.urlopen(url)
		target = '%s/%s/%s' % (os.path.dirname(os.path.abspath(__file__)), directory, filename)
		output = open(target, 'wb')
		output.write(imgfile.read())
		output.close()

		return target

bb = BingBackground()