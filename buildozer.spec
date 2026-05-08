[app]
version = 0.1
title = Custom A34 Python
package.name = mya34app
package.domain = org.test
source.dir = src
requirements = python3,kivy==2.3.0,kivymd,pillow

# Crucial for A34 hardware
android.archs = arm64-v8a
android.api = 33
android.minapi = 21
orientation = portrait
fullscreen = 0

