# Author         Piotr Filipek
# Email          danoxide@outlook.com
# Release date   17 september 2015

import json, urllib2, os, platform

# Class that download current wallpaper from the Bing
# site and sets its as a desktop wallpaper.
class BingBackground:
    domain = "http://www.bing.com%s"
    data = domain % "/HPImageArchive.aspx?format=js&idx=0&n=1&mkt=en-US"
    target = ''
    directory = 'wallpapers'

    def __init__(self):
        pass

    # Download informations from the Bing site in JSON
    def get_json(self):
        return json.load(urllib2.urlopen(self.data))

    # Set downloaded picture as a wallpaper
    def set_as_wallpaper(self):
        url = self.domain % self.get_json()['images'][0]['url']
        name = url.split('/')[-1]
        self.target = '%s/%s/%s' % (os.path.dirname(os.path.abspath(__file__)), self.directory, name)
        distro = self.linux_distribution()

        # check if file exists
        if not os.path.isfile(self.target):
            self.save(url)

        if distro == "ubuntu":
            os.system('gsettings set org.gnome.desktop.background picture-uri "file://%s"' % self.target)
        elif distro == "lubuntu":
            os.system('pcmanfm -w %s' % self.target);
        else:
            print "Can't to set wallpaper, because your distro is unsupported."

    # Save current Bing wallpaper
    def save(self, url):
        imgfile = urllib2.urlopen(url)
        output = open(self.target, 'wb')
        output.write(imgfile.read())
        output.close()

    # Get distro name
    def linux_distribution(self):
        try:
            return platform.linux_distribution()[0].lower()
        except:
            return "n/a"

# Run application
bb = BingBackground()
bb.set_as_wallpaper()