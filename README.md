# Bing Wallpaper
Ten malutki skrypt Pythona pobiera aktualnie używane tło ze strony wyszukiwarki Bing i ustawia jako tło pulpitu.

### Instalacja
Korzystając z polecenia `git clone` sklonuj repozytorium, a następnie uruchom korzystając z terminala:
```
$ git clone https://github.com/danoxide/Bing-Wallpaper.git
$ python bingbackground.py
```
**Automatyczne odświeżanie**

Dodając parametr `--refresh h` możesz sprawić, aby nowa tapeta była sprawdzana co `h` godzin. Poniższy przykład spowoduje, że tapeta będzie sprawdzana co 6h.
```
$ python bingbackground.py --refresh 6
```
Możesz również dodać powyższe polecenie do autostartu, co spowoduje, że program będzie uruchamiany wraz ze startem systemu i automatycznie tapeta będzie zmieniana własnie co `h` godzin.

### Wymagania
 * Python: 2.7.9
 * System Linux z zainstalowanym jednym z podanych środowisk graficznych: Gnome, Unity, Cinnamon, MATE, XFCE4, LXDE, Fluxbox, Blackbox, Openbox, IceWM, JWM, AfterStep, Trinity, KDE.
