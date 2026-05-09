import os
import subprocess
import sys
import yaml
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
        self.label = MDLabel(text="A34 System: Active", halign="center", font_style="H4")
        button = MDRaisedButton(
            text="AUTHORIZE ACCESS", 
            pos_hint={"center_x": .5}, 
            on_release=self.ask_permissions
        )
        layout.add_widget(self.label)
        layout.add_widget(button)
        screen = MDScreen()
        screen.add_widget(layout)
        return screen

    def ask_permissions(self, instance):
        # NEARBY_WIFI_DEVICES requires API 33+ logic
        request_permissions([
            Permission.CAMERA, 
            Permission.RECORD_AUDIO, 
            Permission.ACCESS_FINE_LOCATION, 
            Permission.BODY_SENSORS, 
            Permission.BLUETOOTH_CONNECT, 
            Permission.BLUETOOTH_SCAN,
            Permission.READ_EXTERNAL_STORAGE,
            Permission.WRITE_EXTERNAL_STORAGE
        ])
        self.label.text = "Check for permission popups!"

if __name__ == "__main__":
    MainApp().run()
"""

BUILDOZER_SPEC = """[app]
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
"""

MAIN_YML = """name: AI Build
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up JDK 17
        uses: actions/setup-java@v4
        with:
          java-version: '17'
          distribution: 'temurin'

      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install System Dependencies
        run: |
          sudo apt update
          sudo apt install -y build-essential ccache git libffi-dev libssl-dev \
          python3 python3-setuptools python3-pip python3-dev \
          zip zlib1g-dev libncurses5 libstdc++6 \
          libgtk-3-dev libgstreamer1.0-dev
          pip install --upgrade pip
          pip install buildozer Cython==0.29.33

      - name: Build with Buildozer
        run: |
          # The 'yes' command handles the SDK license prompts
          yes | buildozer -v android debug
          
      - name: Upload APK
        if: success()
        uses: actions/upload-artifact@v4
        with:
          name: A34-Master-APK
          path: bin/*.apk
"""

# --- 2. LOGIC FUNCTIONS ---

def validate_yaml(content):
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
    try:
        img = Image.new('RGBA', (512, 512), color=(0, 121, 107, 255))
        img.save("icon.png")
        print("Generated project icon.")
    except Exception as e:
        print(f"Icon Error: {e}")

def write_file(path, content):
    os.makedirs(os.path.dirname(path) or '.', exist_ok=True)
    with open(path, "w") as f:
        f.write(content)
    print(f"Created: {path}")

def run(cmd):
    return subprocess.run(cmd, shell=True).returncode == 0

# --- 3. EXECUTION ---

def main():
    print("--- 1. Validation ---")
    if not validate_yaml(MAIN_YML):
        sys.exit(1)
    
    print("--- 2. Project Assembly ---")
    process_icon()
    write_file("main.py", MAIN_PY)
    write_file("buildozer.spec", BUILDOZER_SPEC)
    write_file(".github/workflows/main.yml", MAIN_YML)

    print("\\n--- 3. Git Push ---")
    run("git add .")
    run('git commit -m "Fix: Updated dependencies and API 34 compatibility"')
    
    if run("git push origin main"):
        print("\\nSuccess! Monitor the 'Actions' tab on GitHub.")
    else:
        # Fallback for sync issues
        run("git pull origin main --rebase")
        run("git push origin main")

if __name__ == "__main__":
    main()

