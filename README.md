kahvipoliisi
============

Following info is for raspbian. 

Configure networking
--------------------
```sh
sudo wpa_supplicant -c/etc/wpa_supplicant/wpa_supplicant.conf -iwlan0 -d
```
TODO

Install OpenCV
--------------
Note rasbian supports only OpenCV 2.3.1

```sh
sudo apt-get install python-opencv
```

Disable camera auto focus
-------------------------
http://www.bot-thoughts.com/2013/01/lifecam-hd-6000-autofocus-fix-raspberry.html

```sh
sudo apt-get install uvcdynctrl
uvcdynctrl --set='Focus, Auto' 0
```
