# Python-pygame-overlay
## How to use
This script lets you create overlay over any window you like and draw on it using pygame:
![image](https://user-images.githubusercontent.com/48300772/111068299-28524680-84c0-11eb-8fce-c33bb72640d8.png)
Initialize the overlay, and start the loop in which you draw like so:
```
overlay = Overlay(targetWindowTitle)

while overlay.window:
  overlay.draw("fillRect", vector=Vector(30, 30, 60, 60), color=(255, 0, 255))
  overlay.handle()
```
