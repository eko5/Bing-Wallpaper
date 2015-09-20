#!/usr/bin/python
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
        env = self.get_enviroment()

        # check if file exists
        if not os.path.isfile(self.target):
            self.save(url)

        if env == "ubuntu" or env == "gnome":
            os.system('gsettings set org.gnome.desktop.background picture-uri "file://%s"' % self.target)
        elif env == "lubuntu":
            os.system('pcmanfm -w %s' % self.target);
        elif env == "xfce":
            os.system('xfconf-query -c xfce4-desktop -p /backdrop/screen0/monitorLVDS-0/workspace0/last-image -s %s' % self.target)
        else:
            print "Can't to set wallpaper, because your distro is unsupported."

    # Save current Bing wallpaper
    def save(self, url):
        imgfile = urllib2.urlopen(url)
        output = open(self.target, 'wb')
        output.write(imgfile.read())
        output.close()

    # Get distro name
    def get_enviroment(self):
        return os.environ['DESKTOP_SESSION']

# Run application
def main():
    bb = BingBackground()
    bb.set_as_wallpaper()

if __name__ == "__main__":
    main()
