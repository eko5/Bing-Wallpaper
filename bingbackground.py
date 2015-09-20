#!/usr/bin/python
# Author         Piotr Filipek
# Email          danoxide@outlook.com
# Release date   17 september 2015

import json, urllib2, os, platform, sys, subprocess, gio

# Class that download current wallpaper from the Bing
# site and sets its as a desktop wallpaper.
class BingBackground():
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
        env = self.get_desktop_environment()

        # check if file exists
        if not os.path.isfile(self.target):
            self.save(url)

        # Set as wallpaper
        self.set_wallpaper(self.target, True)

    # Save current Bing wallpaper
    def save(self, url):
        imgfile = urllib2.urlopen(url)
        output = open(self.target, 'wb')
        output.write(imgfile.read())
        output.close()

    # Get name of desktop enviroment
    def get_desktop_environment(self):
        if sys.platform == "darwin":
            return "mac"
        else: #Most likely either a POSIX system or something not much common
            desktop_session = os.environ.get("DESKTOP_SESSION")
            if desktop_session is not None: #easier to match if we doesn't have  to deal with caracter cases
                desktop_session = desktop_session.lower()
                if desktop_session in ["gnome","unity", "cinnamon", "mate", "xfce4", "lxde", "fluxbox", 
                                       "blackbox", "openbox", "icewm", "jwm", "afterstep","trinity", "kde"]:
                    return desktop_session
                ## Special cases ##
                # Canonical sets $DESKTOP_SESSION to Lubuntu rather than LXDE if using LXDE.
                # There is no guarantee that they will not do the same with the other desktop environments.
                elif "xfce" in desktop_session or desktop_session.startswith("xubuntu"):
                    return "xfce4"
                elif desktop_session.startswith("ubuntu"):
                    return "unity"       
                elif desktop_session.startswith("lubuntu"):
                    return "lxde" 
                elif desktop_session.startswith("kubuntu"): 
                    return "kde" 
                elif desktop_session.startswith("razor"): # e.g. razorkwin
                    return "razor-qt"
                elif desktop_session.startswith("wmaker"): # e.g. wmaker-common
                    return "windowmaker"
            if os.environ.get('KDE_FULL_SESSION') == 'true':
                return "kde"
            elif os.environ.get('GNOME_DESKTOP_SESSION_ID'):
                if not "deprecated" in os.environ.get('GNOME_DESKTOP_SESSION_ID'):
                    return "gnome2"
            elif self.is_running("xfce-mcs-manage"):
                return "xfce4"
            elif self.is_running("ksmserver"):
                return "kde"
        return "unknown"

    # Check is process running
    def is_running(self, process):
        try: #Linux/Unix
            s = subprocess.Popen(["ps", "axw"], stdout=subprocess.PIPE)
        except:
            pass

        for x in s.stdout:
            if re.search(process, x):
                return True
        return False

    # Set given file as a wallpaper
    def set_wallpaper(self, file_loc, first_run):
        # Note: There are two common Linux desktop environments where 
        # I have not been able to set the desktop background from 
        # command line: KDE, Enlightenment
        desktop_env = self.get_desktop_environment()
        try:
            if desktop_env in ["gnome", "unity", "cinnamon"]:
                uri = "'file://%s'" % file_loc

                try:
                    SCHEMA = "org.gnome.desktop.background"
                    KEY = "picture-uri"
                    gsettings = Gio.Settings.new(SCHEMA)
                    gsettings.set_string(KEY, uri)
                except:
                    args = ["gsettings", "set", "org.gnome.desktop.background", "picture-uri", uri]
                    subprocess.Popen(args)
            elif desktop_env == "mate":
                try: # MATE >= 1.6
                    # info from http://wiki.mate-desktop.org/docs:gsettings
                    args = ["gsettings", "set", "org.mate.background", "picture-filename", "'%s'" % file_loc]
                    subprocess.Popen(args)
                except: # MATE < 1.6
                    # From https://bugs.launchpad.net/variety/+bug/1033918
                    args = ["mateconftool-2", "-t", "string", "--set", "/desktop/mate/background/picture_filename", '"%s"' % file_loc]
                    subprocess.Popen(args)
            elif desktop_env == "gnome2": # Not tested
                # From https://bugs.launchpad.net/variety/+bug/1033918
                args = ["gconftool-2", "-t", "string", "--set", "/desktop/gnome/background/picture_filename", '"%s"' % file_loc]
                subprocess.Popen(args)
            ## KDE4 is difficult
            ## see http://blog.zx2c4.com/699 for a solution that might work
            elif desktop_env in ["kde3", "trinity"]:
                # From http://ubuntuforums.org/archive/index.php/t-803417.html
                args = 'dcop kdesktop KBackgroundIface setWallpaper 0 "%s" 6' % file_loc
                subprocess.Popen(args, shell=True)
            elif desktop_env == "xfce4":
                #From http://www.commandlinefu.com/commands/view/2055/change-wallpaper-for-xfce4-4.6.0
                if first_run:
                    args0 = ["xfconf-query", "-c", "xfce4-desktop", "-p", "/backdrop/screen0/monitor0/image-path", "-s", file_loc]
                    args1 = ["xfconf-query", "-c", "xfce4-desktop", "-p", "/backdrop/screen0/monitor0/image-style", "-s", "3"]
                    args2 = ["xfconf-query", "-c", "xfce4-desktop", "-p", "/backdrop/screen0/monitor0/image-show", "-s", "true"]
                    subprocess.Popen(args0)
                    subprocess.Popen(args1)
                    subprocess.Popen(args2)
                args = ["xfdesktop", "--reload"]
                subprocess.Popen(args)
            elif desktop_env == "razor-qt": #TODO: implement reload of desktop when possible
                if first_run:
                    desktop_conf = configparser.ConfigParser()
                    # Development version
                    desktop_conf_file = os.path.join(self.get_config_dir("razor"), "desktop.conf") 
                    if os.path.isfile(desktop_conf_file):
                        config_option = r"screens\1\desktops\1\wallpaper"
                    else:
                        desktop_conf_file = os.path.join(self.get_home_dir(), ".razor/desktop.conf")
                        config_option = r"desktops\1\wallpaper"
                    desktop_conf.read(os.path.join(desktop_conf_file))
                    try:
                        if desktop_conf.has_option("razor", config_option): #only replacing a value
                            desktop_conf.set("razor", config_option, file_loc)
                            with codecs.open(desktop_conf_file, "w", encoding="utf-8", errors="replace") as f:
                                desktop_conf.write(f)
                    except:
                        pass
                else:
                    #TODO: reload desktop when possible
                    pass 
            elif desktop_env in ["fluxbox", "jwm", "openbox", "afterstep"]:
                #http://fluxbox-wiki.org/index.php/Howto_set_the_background
                # used fbsetbg on jwm too since I am too lazy to edit the XML configuration 
                # now where fbsetbg does the job excellent anyway. 
                # and I have not figured out how else it can be set on Openbox and AfterSTep
                # but fbsetbg works excellent here too.
                try:
                    args = ["fbsetbg", file_loc]
                    subprocess.Popen(args)
                except:
                    sys.stderr.write("ERROR: Failed to set wallpaper with fbsetbg!\n")
                    sys.stderr.write("Please make sre that You have fbsetbg installed.\n")
            elif desktop_env == "icewm":
                # command found at http://urukrama.wordpress.com/2007/12/05/desktop-backgrounds-in-window-managers/
                args = ["icewmbg", file_loc]
                subprocess.Popen(args)
            elif desktop_env == "blackbox":
                # command found at http://blackboxwm.sourceforge.net/BlackboxDocumentation/BlackboxBackground
                args = ["bsetbg", "-full", file_loc]
                subprocess.Popen(args)
            elif desktop_env == "lxde":
                args = "pcmanfm --set-wallpaper %s --wallpaper-mode=scaled" % file_loc
                subprocess.Popen(args, shell=True)
            elif desktop_env == "windowmaker":
                # From http://www.commandlinefu.com/commands/view/3857/set-wallpaper-on-windowmaker-in-one-line
                args = "wmsetbg -s -u %s" % file_loc
                subprocess.Popen(args, shell=True)
            else:
                if first_run: #don't spam the user with the same message over and over again
                    sys.stderr.write("Warning: Failed to set wallpaper. Your desktop environment is not supported.")
                    sys.stderr.write("You can try manually to set Your wallpaper to %s" % file_loc)
                return False
            return True
        except:
            sys.stderr.write("ERROR: Failed to set wallpaper. There might be a bug.\n")
            return False

    # Get config directory
    def get_config_dir(self, app_name):
        if "XDG_CONFIG_HOME" in os.environ:
            confighome = os.environ['XDG_CONFIG_HOME']
        else:
            try:
                from xdg import BaseDirectory   
                confighome =  BaseDirectory.xdg_config_home
            except ImportError: # Most likely a Linux/Unix system anyway
                confighome =  os.path.join(self.get_home_dir(), ".config")
        configdir = os.path.join(confighome, app_name)
        return configdir

    def get_home_dir(self):
        home_dir = os.getenv('USERPROFILE') or os.getenv('HOME')
        if home_dir is not None:
            return os.path.normpath(home_dir)
        else:
            raise KeyError("Neither USERPROFILE or HOME environment variables set.")
    

# Run application
def main():
    bb = BingBackground()
    bb.set_as_wallpaper()

if __name__ == "__main__":
    main()
