[app]
title = Custom A34 Python
package.name = a34python
package.domain = org.ranjha
source.dir = src
requirements = python3,kivy,sdl2,pyjnius

# Crucial for A34 hardware
android.archs = arm64-v8a
android.api = 33
android.minapi = 21
orientation = portrait
fullscreen = 0

