#!/usr/bin/env python3
"""
A34 Master Tool - Hybrid Build System
Kivy development + Gradle CI/CD for Android 16
"""

import os
import sys
import subprocess
import yaml
from pathlib import Path
from typing import Tuple
from PIL import Image
import json

# ============================================================================
# KIVY APPLICATION CODE (Same as before, Android 16 optimized)
# ============================================================================

MAIN_PY = """from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from android.permissions import request_permissions, Permission
from android import api_version, android_version

class MainApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Teal"
        layout = MDBoxLayout(orientation='vertical', spacing=20, padding=50)
        
        self.label = MDLabel(
            text=f"A34 Master Tool\\nAndroid {android_version} (API {api_version})",
            halign="center",
            font_style="H4"
        )
        
        button = MDRaisedButton(
            text="START SESSION",
            pos_hint={"center_x": .5},
            on_release=self.request_permissions
        )
        
        layout.add_widget(self.label)
        layout.add_widget(button)
        
        screen = MDScreen()
        screen.add_widget(layout)
        return screen
    
    def request_permissions(self, instance):
        permissions = [
            Permission.CAMERA,
            Permission.RECORD_AUDIO,
            Permission.ACCESS_FINE_LOCATION,
            Permission.BODY_SENSORS,
        ]
        
        # Android 13+ (API 33+) needs media permissions
        if api_version >= 33:
            permissions.extend([
                Permission.READ_MEDIA_IMAGES,
                Permission.READ_MEDIA_VIDEO,
                Permission.READ_MEDIA_AUDIO
            ])
        else:
            permissions.extend([
                Permission.READ_EXTERNAL_STORAGE,
                Permission.WRITE_EXTERNAL_STORAGE
            ])
        
        request_permissions(permissions)
        self.label.text = "✓ Permissions Granted\\nSession Ready"

if __name__ == "__main__":
    MainApp().run()
"""

# ============================================================================
# GRADLE BUILD FILES (For GitHub Actions)
# ============================================================================

SETTINGS_GRADLE = """rootProject.name = "A34MasterTool"
include ':app'
"""

ROOT_BUILD_GRADLE = """// Top-level build file
buildscript {
    repositories {
        google()
        mavenCentral()
        maven { url 'https://chaquo.com/maven' }
    }
    dependencies {
        classpath 'com.android.tools.build:gradle:8.2.0'
        classpath 'com.chaquo.python:gradle:14.0.2'
    }
}

allprojects {
    repositories {
        google()
        mavenCentral()
        maven { url 'https://chaquo.com/maven' }
    }
}

tasks.register('clean', Delete) {
    delete rootProject.buildDir
}
"""

APP_BUILD_GRADLE = """plugins {
    id 'com.android.application'
    id 'com.chaquo.python'
}

android {
    namespace 'org.ranjha.mastertool'
    compileSdk 37
    
    defaultConfig {
        applicationId "org.ranjha.mastertool"
        minSdk 21
        targetSdk 37
        versionCode 5
        versionName "0.5"
        
        ndk {
            abiFilters "arm64-v8a"
        }
        
        python {
            buildPython "python3"
            pip {
                install "kivy==2.3.0"
                install "kivymd==1.1.1"
                install "pillow==10.0.0"
                install "pyjnius==1.5.0"
            }
        }
    }
    
    buildTypes {
        release {
            minifyEnabled false
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt')
        }
    }
    
    compileOptions {
        sourceCompatibility JavaVersion.VERSION_17
        targetCompatibility JavaVersion.VERSION_17
    }
}

dependencies {
    implementation 'androidx.core:core:1.12.0'
    implementation 'androidx.appcompat:appcompat:1.6.1'
    implementation 'com.google.android.material:material:1.11.0'
}
"""

ANDROID_MANIFEST = """<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="org.ranjha.mastertool">
    
    <!-- Android 16 (API 37) permissions -->
    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.CAMERA" />
    <uses-permission android:name="android.permission.RECORD_AUDIO" />
    <uses-permission android:name="android.permission.ACCESS_FINE_LOCATION" />
    <uses-permission android:name="android.permission.BODY_SENSORS" />
    <uses-permission android:name="android.permission.BODY_SENSORS_BACKGROUND" />
    <uses-permission android:name="android.permission.VIBRATE" />
    
    <!-- Android 13+ media permissions -->
    <uses-permission android:name="android.permission.READ_MEDIA_IMAGES" />
    <uses-permission android:name="android.permission.READ_MEDIA_VIDEO" />
    <uses-permission android:name="android.permission.READ_MEDIA_AUDIO" />
    <uses-permission android:name="android.permission.POST_NOTIFICATIONS" />
    
    <!-- Legacy storage permissions -->
    <uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE" 
        android:maxSdkVersion="32" />
    <uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE"
        android:maxSdkVersion="32" />
    
    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="A34 Master Tool"
        android:theme="@style/Theme.MaterialComponents.DayNight.NoActionBar">
        
        <activity
            android:name="org.kivy.android.PythonActivity"
            android:exported="true"
            android:launchMode="singleTask"
            android:configChanges="orientation|screenSize|keyboardHidden">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>
"""

# ============================================================================
# ENHANCED GITHUB ACTIONS WORKFLOW (Pure Gradle)
# ============================================================================

GRADLE_WORKFLOW = """name: Hybrid Build - Gradle CI/CD

on:
  push:
    branches: [ main, master ]
    tags: ['v*']
  pull_request:
    branches: [ main, master ]
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    timeout-minutes: 30
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up JDK 17
      uses: actions/setup-java@v4
      with:
        java-version: '17'
        distribution: 'temurin'
    
    - name: Setup Android SDK
      uses: android-actions/setup-android@v3
      with:
        packages: |
          platform-tools
          platforms;android-37
          build-tools;34.0.0
          ndk;26.1.10909125
    
    - name: Setup Gradle
      uses: gradle/actions/setup-gradle@v3
      with:
        gradle-version: '8.5'
        cache-read-only: ${{ github.ref != 'refs/heads/main' }}
    
    - name: Grant execute permission
      run: chmod +x gradlew
    
    - name: Build Debug APK
      run: ./gradlew assembleDebug --no-daemon
    
    - name: Build Release APK
      run: ./gradlew assembleRelease --no-daemon
      if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    
    - name: Sign Release APK
      if: success() && github.event_name == 'push' && github.ref == 'refs/heads/main' && secrets.KEYSTORE_BASE64 != ''
      run: |
        echo "${{ secrets.KEYSTORE_BASE64 }}" | base64 --decode > keystore.jks
        echo "storePassword=${{ secrets.KEYSTORE_PASSWORD }}" >> keystore.properties
        echo "keyPassword=${{ secrets.KEY_PASSWORD }}" >> keystore.properties
        echo "keyAlias=${{ secrets.KEY_ALIAS }}" >> keystore.properties
        echo "storeFile=../keystore.jks" >> keystore.properties
        mv keystore.properties app/
        ./gradlew signRelease
    
    - name: Upload Debug APK
      uses: actions/upload-artifact@v4
      with:
        name: A34-Master-Tool-Debug
        path: app/build/outputs/apk/debug/*.apk
        retention-days: 30
    
    - name: Upload Release APK
      if: success() && github.event_name == 'push' && github.ref == 'refs/heads/main'
      uses: actions/upload-artifact@v4
      with:
        name: A34-Master-Tool-Release
        path: app/build/outputs/apk/release/*.apk
        retention-days: 90
    
    - name: Create Release
      if: startsWith(github.ref, 'refs/tags/v')
      uses: softprops/action-gh-release@v1
      with:
        files: app/build/outputs/apk/release/*.apk
        generate_release_notes: true
"""

# ============================================================================
# GRADLE WRAPPER SCRIPT (For Termux/CI)
# ============================================================================

GRADLE_WRAPPER = """#!/bin/sh
# Gradle wrapper for Termux/CI
GRADLE_VERSION="8.5"
GRADLE_HOME="$HOME/.gradle/wrapper/dists/gradle-${GRADLE_VERSION}-bin"

if [ ! -d "$GRADLE_HOME" ]; then
    echo "Downloading Gradle ${GRADLE_VERSION}..."
    wget -q "https://services.gradle.org/distributions/gradle-${GRADLE_VERSION}-bin.zip"
    unzip -q "gradle-${GRADLE_VERSION}-bin.zip" -d "$HOME/.gradle/wrapper/"
    rm "gradle-${GRADLE_VERSION}-bin.zip"
fi

exec "$GRADLE_HOME/gradle-${GRADLE_VERSION}/bin/gradle" "$@"
"""

# ============================================================================
# MAIN GENERATION FUNCTION
# ============================================================================

def setup_hybrid_project():
    """Generate complete hybrid project structure"""
    
    print("\n" + "="*60)
    print("🔧 A34 MASTER TOOL - HYBRID BUILD SETUP")
    print("="*60 + "\n")
    
    # Create directory structure
    directories = [
        ".github/workflows",
        "app/src/main/java/org/ranjha/mastertool",
        "app/src/main/res/mipmap-hdpi",
        "app/src/main/res/mipmap-mdpi",
        "app/src/main/res/mipmap-xhdpi",
        "app/src/main/res/mipmap-xxhdpi",
        "app/src/main/res/mipmap-xxxhdpi",
        "gradle/wrapper"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"📁 Created: {directory}")
    
    # Write all files
    files = {
        "main.py": MAIN_PY,
        "settings.gradle": SETTINGS_GRADLE,
        "build.gradle": ROOT_BUILD_GRADLE,
        "app/build.gradle": APP_BUILD_GRADLE,
        "app/src/main/AndroidManifest.xml": ANDROID_MANIFEST,
        ".github/workflows/gradle-build.yml": GRADLE_WORKFLOW,
        "gradlew": GRADLE_WRAPPER,
        "gradle/wrapper/gradle-wrapper.properties": "distributionUrl=https\\://services.gradle.org/distributions/gradle-8.5-bin.zip"
    }
    
    for path, content in files.items():
        with open(path, 'w') as f:
            f.write(content)
        print(f"✅ Created: {path}")
    
    # Make gradlew executable
    os.chmod("gradlew", 0o755)
    
    # Generate icons
    generate_icons()
    
    print("\n" + "="*60)
    print("✅ HYBRID PROJECT READY!")
    print("="*60)
    print("\n📱 Your Kivy code is in: main.py")
    print("🔧 Build with Gradle: ./gradlew assembleDebug")
    print("☁️ GitHub Actions will auto-build on push")
    print("\n🚀 Next steps:")
    print("  1. git add . && git commit -m 'Hybrid build setup'")
    print("  2. git push origin main")
    print("  3. Check Actions tab for APK download")
    print("="*60 + "\n")

def generate_icons():
    """Generate app icons for all resolutions"""
    icon_sizes = {
        "mipmap-mdpi": 48,
        "mipmap-hdpi": 72,
        "mipmap-xhdpi": 96,
        "mipmap-xxhdpi": 144,
        "mipmap-xxxhdpi": 192
    }
    
    base_color = (0, 121, 107, 255)
    
    for folder, size in icon_sizes.items():
        img = Image.new('RGBA', (size, size), color=base_color)
        # Add simple "A" logo
        from PIL import ImageDraw, ImageFont
        draw = ImageDraw.Draw(img)
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", size//2)
        except:
            font = ImageFont.load_default()
        
        text = "A"
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (size - text_width) // 2
        y = (size - text_height) // 2
        draw.text((x, y), text, fill="white", font=font)
        
        img.save(f"app/src/main/res/{folder}/ic_launcher.png")
        print(f"🎨 Generated icon: {folder}/ic_launcher.png")

if __name__ == "__main__":
    setup_hybrid_project()
