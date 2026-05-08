[app]

# (str) Title of your application
title = A34 Python App

# (str) Package name
package.name = ranjha_a34_app

# (str) Package domain (needed for android packaging)
package.domain = org.ranjha

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas

# (str) Application versioning (method 1)
version = 0.1

# (list) Application requirements
# Added kivymd and pillow for the modern UI we wrote
requirements = python3,kivy==2.3.0,kivymd,pillow,google-generativeai

# (str) Supported orientations
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# (int) Target Android API, should be as high as possible.
android.api = 34

# (int) Minimum API your APK will support.
android.minapi = 21

# (str) Android SDK directory (if empty, it will be installed automatically)
# GitHub Actions handles this automatically

# (str) Android NDK version to use
android.ndk = 26b

# (bool) If True, then skip trying to update the Android sdk
# This can be useful to avoid any automated update while testing.
android.skip_update = False

# (bool) If True, then automatically accept SDK license
android.accept_sdk_license = True

# (str) The Android arch to build for.
# CRITICAL: Samsung A34 is a 64-bit device
android.archs = arm64-v8a

# (list) The Android architectures to build for.
# We focus ONLY on arm64 to speed up the 22-minute build time
android.arch = arm64-v8a

# (str) Log level (0 = error only, 1 = info, 2 = debug (with command output))
# Set to 2 so our heal.py script can read the errors
log_level = 2

# (int) Display warning if buildozer is run as root (0 = off, 1 = on)
warn_on_root = 1

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = off, 1 = on)
warn_on_root = 1

