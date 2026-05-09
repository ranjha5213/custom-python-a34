[app]
title = A34 Master Tool
package.name = ranjha.master.tool
package.domain = org.ranjha
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.2
icon.filename = icon.png
requirements = python3,kivy==2.3.0,kivymd,pillow
orientation = portrait
android.api = 34
android.minapi = 21
android.ndk = 26b
android.archs = arm64-v8a
android.accept_sdk_license = True
# Removed NEARBY_WIFI_DEVICES temporarily to ensure build stability on API 34
android.permissions = INTERNET, CAMERA, RECORD_AUDIO, ACCESS_FINE_LOCATION, BODY_SENSORS, BLUETOOTH_CONNECT, BLUETOOTH_SCAN, VIBRATE, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE
log_level = 2
