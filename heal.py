import os
import google.generativeai as genai
import subprocess
import sys

# 1. Setup API Configuration
# The key must be stored in GitHub Secrets as GEMINI_API_KEY
API_KEY = os.environ.get("GEMINI_API_KEY")

if not API_KEY:
    print("Error: GEMINI_API_KEY not found in environment variables.")
    sys.exit(1)

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

def get_fix_from_ai(error_log):
    """
    Sends the error log to Gemini and requests a specific bash fix.
    """
    prompt = f"""
    CONTEXT:
    You are an expert Android Developer using Buildozer and Kivy. 
    The target device is a Samsung Galaxy A34 (Architecture: arm64-v8a, OS: Android 14).
    The build is running on a GitHub Actions Ubuntu runner.

    TASK:
    Analyze the Buildozer error log below. Identify why the build failed.
    Provide ONLY a single-line bash command using 'sed' to fix the 'buildozer.spec' or 'main.yml'.

    COMMON FIXES:
    - Missing requirements: sed -i 's/requirements = .*/requirements = python3,kivy,NEW_LIB/' buildozer.spec
    - Arch mismatch: sed -i 's/android.archs = .*/android.archs = arm64-v8a/' buildozer.spec
    - API Level: sed -i 's/android.api = .*/android.api = 34/' buildozer.spec

    CONSTRAINTS:
    - Output ONLY the bash command. 
    - No explanations. No markdown code blocks. No backticks.
    - Focus on 64-bit compatibility for the Samsung A34.

    ERROR LOG:
    {error_log}
    """
    
    try:
        response = model.generate_content(prompt)
        # Strip any accidental backticks or whitespace AI might include
        return response.text.strip().replace('`', '')
    except Exception as e:
        print(f"AI Generation failed: {e}")
        return None

def run_heal():
    """
    Reads the build log, gets the fix, and applies it.
    """
    log_file = "build.log"
    
    if not os.path.exists(log_file):
        print(f"Log file {log_file} not found. Cannot heal.")
        return

    print("Reading build log for analysis...")
    with open(log_file, "r") as f:
        # Get the last 150 lines - enough for context, small enough for the API
        log_lines = f.readlines()[-150:]
        error_context = "".join(log_lines)

    print("Consulting Gemini AI for a fix...")
    fix_command = get_fix_from_ai(error_context)

    if fix_command and "sed" in fix_command:
        # Final safety check to prevent accidental destructive commands
        if "buildozer.spec" in fix_command or "main.yml" in fix_command:
            print(f"Applying AI-suggested fix: {fix_command}")
            result = subprocess.run(fix_command, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                print("Fix applied successfully.")
            else:
                print(f"Failed to apply fix: {result.stderr}")
        else:
            print(f"AI suggested an unusual command. Skipping for safety: {fix_command}")
    else:
        print("AI could not determine a safe bash fix.")

if __name__ == "__main__":
    run_heal()

