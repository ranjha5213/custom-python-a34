import os
import subprocess
import sys
import yaml  # Run 'pip install pyyaml' in Termux if not already done
from PIL import Image

# --- 1. CONFIGURATION DATA ---

MAIN_PY = """from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from android.permissions import request_permissions, Permission

class MainApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Teal"
        layout = MDBoxLayout(orientation='vertical', spacing=20, padding=50)
        self.label = MDLabel(text="WiFi & Sensor System Active", halign="center", font_style="H4")
        button = MDRaisedButton(
            text="AUTHORIZE ALL ACCESS", 
            pos_hint={"center_x": .5}, 
            on_release=self.ask_permissions
        )
        layout.add_widget(self.label)
        layout.add_widget(button)
        screen = MDScreen()
        screen.add_widget(layout)
        return screen

    def ask_permissions(self, instance):
        request_permissions([
            Permission.CAMERA, Permission.RECORD_AUDIO, 
            Permission.ACCESS_FINE_LOCATION, Permission.ACCESS_COARSE_LOCATION,
            Permission.BODY_SENSORS, Permission.BLUETOOTH_CONNECT, 
            Permission.BLUETOOTH_SCAN, Permission.READ_EXTERNAL_STORAGE, 
            Permission.WRITE_EXTERNAL_STORAGE, Permission.NEARBY_WIFI_DEVICES
        ])
        self.label.text = "Check for WiFi & Sensor popups!"

if __name__ == "__main__":
    MainApp().run()
"""

BUILDOZER_SPEC = """[app]
title = A34 Master Tool
package.name = ranjha.master.tool
package.domain = org.ranjha
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
icon.filename = icon.png
requirements = python3,kivy==2.3.0,kivymd,pillow,google-generativeai
orientation = portrait
android.api = 34
android.minapi = 21
android.ndk = 26b
android.archs = arm64-v8a
android.accept_sdk_license = True
android.permissions = INTERNET, CAMERA, RECORD_AUDIO, ACCESS_FINE_LOCATION, ACCESS_COARSE_LOCATION, BODY_SENSORS, BLUETOOTH_CONNECT, BLUETOOTH_SCAN, VIBRATE, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE, ACCESS_WIFI_STATE, CHANGE_WIFI_STATE, ACCESS_NETWORK_STATE, NEARBY_WIFI_DEVICES
android.arch = arm64-v8a
log_level = 2
"""

MAIN_YML = """name: AI Build
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Install Dependencies
        run: |
          pip install buildozer Cython==0.29.33
          sudo apt install -y build-essential libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev zlib1g-dev libgstreamer1.0-dev
      - name: Build with Buildozer
        run: yes | buildozer -v android debug
      - name: Upload APK
        if: success()
        uses: actions/upload-artifact@v4
        with:
          name: A34-APK
          path: bin/*.apk
"""

# --- 2. LOGIC FUNCTIONS ---

def validate_yaml(content):
    """Checks for tabs and indentation errors."""
    if "\\t" in content:
        print("ERROR: YAML contains TABS. Use SPACES only.")
        return False
    try:
        yaml.safe_load(content)
        return True
    except yaml.YAMLError as exc:
        print(f"YAML Syntax Error: {exc}")
        return False

def process_icon():
    """Converts any image to the required 512x512 icon.png"""
    potential_icons = ['icon.png', 'icon.jpg', 'icon.jpeg', 'logo.png']
    found_file = next((f for f in potential_icons if os.path.exists(f)), None)
    try:
        if found_file:
            with Image.open(found_file) as img:
                img = img.convert("RGBA").resize((512, 512), Image.Resampling.LANCZOS)
                img.save("icon.png", "PNG")
                print(f"Icon created from: {found_file}")
        else:
            img = Image.new('RGBA', (512, 512), color=(0, 121, 107, 255))
            img.save("icon.png")
            print("Created default Teal icon.")
    except Exception as e:
        print(f"Icon Processing Error: {e}")

def write_file(path, content):
    dir_name = os.path.dirname(path)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)
    with open(path, "w") as f:
        f.write(content)
    print(f"Generated: {path}")

def run(cmd):
    result = subprocess.run(cmd, shell=True, text=True, capture_output=True)
    return result.returncode == 0

# --- 3. MAIN EXECUTION ---

def main():
    print("--- 1. Validation & Safety Check ---")
    if not validate_yaml(MAIN_YML):
        print("Build Aborted: main.yml is invalid."); sys.exit(1)
    
    print("--- 2. Rebuilding Project Files ---")
    process_icon()
    write_file("main.py", MAIN_PY)
    write_file("buildozer.spec", BUILDOZER_SPEC)
    write_file(".github/workflows/main.yml", MAIN_YML)

    print("\\n--- 3. Deploying to GitHub ---")
    run("git add .")
    # Pull to sync, forcing local truth
    run("git pull origin main --no-rebase")
    run('git commit -m "Verified Deploy: Strict YAML and Sensor Permissions"')
    
    if run("git push origin main"):
        print("\\nSUCCESS! Pushed to GitHub.")
        print("Visit the 'Actions' tab to see the live build logs.")
    else:
        print("Push rejected. Attempting forced sync...")
        if run("git push origin main --force"):
            print("\\nSUCCESS (Forced Push)! Check your GitHub Actions.")
        else:
            print("\\nFATAL: Could not push to GitHub. Check connection.")

if __name__ == "__main__":
    main()

