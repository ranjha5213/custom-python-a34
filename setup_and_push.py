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
        self.label = MDLabel(text="A34 Master Tool Ready", halign="center", font_style="H4")
        button = MDRaisedButton(
            text="START SESSION", 
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
            Permission.ACCESS_FINE_LOCATION, Permission.BODY_SENSORS,
            Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE
        ])
        self.label.text = "Permissions Requested"

if __name__ == "__main__":
    MainApp().run()
"""

BUILDOZER_SPEC = """[app]
title = A34 Master Tool
package.name = ranjha.master.tool
package.domain = org.ranjha
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.3
icon.filename = icon.png
requirements = python3,kivy==2.3.0,kivymd,pillow
orientation = portrait
android.api = 34
android.minapi = 21
android.ndk = 26b
android.archs = arm64-v8a
android.accept_sdk_license = True
android.permissions = INTERNET, CAMERA, RECORD_AUDIO, ACCESS_FINE_LOCATION, BODY_SENSORS, VIBRATE, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE
log_level = 2
"""

# Optimized for Ubuntu 24.04 Runners
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
          sudo apt-get update
          sudo apt-get install -y --no-install-recommends \
            build-essential git ccache libffi-dev libssl-dev \
            python3-setuptools python3-pip python3-dev \
            zip zlib1g-dev libncurses5 libstdc++6 \
            libgtk-3-dev libgstreamer1.0-dev
          pip install --upgrade pip
          pip install buildozer Cython==0.29.33

      - name: Build with Buildozer
        run: |
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
        print("ERROR: TABS detected in YAML. Use SPACES.")
        return False
    try:
        yaml.safe_load(content)
        return True
    except yaml.YAMLError as exc:
        print(f"YAML Syntax Error: {exc}")
        return False

def process_icon():
    img = Image.new('RGBA', (512, 512), color=(0, 121, 107, 255))
    img.save("icon.png")
    print("Default icon generated.")

def write_file(path, content):
    os.makedirs(os.path.dirname(path) or '.', exist_ok=True)
    with open(path, "w") as f:
        f.write(content)
    print(f"Written: {path}")

def run(cmd):
    return subprocess.run(cmd, shell=True).returncode == 0

# --- 3. EXECUTION ---

def main():
    if not validate_yaml(MAIN_YML):
        sys.exit(1)
    
    process_icon()
    write_file("main.py", MAIN_PY)
    write_file("buildozer.spec", BUILDOZER_SPEC)
    write_file(".github/workflows/main.yml", MAIN_YML)

    print("\\n--- Committing Fixes ---")
    run("git add .")
    run('git commit -m "Fix: Add --no-install-recommends to apt and update APK version"')
    
    # Ensuring we handle remote conflicts
    if not run("git push origin main"):
        print("Push failed. Reversing and forcing update...")
        run("git pull origin main --rebase")
        run("git push origin main")

if __name__ == "__main__":
    main()
