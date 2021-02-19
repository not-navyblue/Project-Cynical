import os, time

print("Checking for updates...")
if os.system("git pull https://github.com/navyblue44/Project-Cynical.git") == 0:
    print("Auto-update successful.")
else:
    print("Auto-update failed.")

if os.system("pip install -r requirements.txt") == 0:
    time.sleep(3)
    print("Loading Project Cynical...")
    _ = os.system("python main.py")
else:
    print("Failed to install required packages. Terminating...")
    time.sleep(2)