[app]
title = Custom A34 Python
package.name = mya34app
package.domain = org.test
source.dir = src
version = 0.1
requirements = python3,kivy==2.3.0,kivymd,pillow
orientation = portrait
fullscreen = 0

[buildozer]
log_level = 2
warn_on_root = 1

[app:android]
# Crucial for A34 hardware
android.archs = arm64-v8a
android.api = 33
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True
android.release_artifact = apk
android.permissions = INTERNET,ACCESS_NETWORK_STATE
android.features = 

[app:android.permissions]
INTERNET = 
ACCESS_NETWORK_STATE = 
