[app]
title = Custom A34 Python
package.name = mya34app
package.domain = org.test
source.dir = src
version = 0.1
requirements = python3,kivy==2.3.0,kivymd,pillow
orientation = portrait
fullscreen = 0
icon.filename = %(source.dir)s/data/icon.png
presplash.filename = %(source.dir)s/data/presplash.png

[buildozer]
log_level = 2
warn_on_root = 1
android_skip_update = False
android_accept_sdk_license = True

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
android.gradle_dependencies = 
android.add_src = 

# Security and networking
android.uses_internet = True
android.uses_network = True

# Performance optimization
android.uses_hardware_acceleration = True
android.prebuilt_libraries = 

# Java configuration
android.java_classes = 
android.gradle_options = org.gradle.jvmargs=-Xmx2048m

# Build configuration
android.bootstrap = sdl2
android.entrypoint = org.test.mya34app.MainActivity
