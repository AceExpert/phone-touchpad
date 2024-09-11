import subprocess, re, threading

threading.Thread(target=lambda: subprocess.Popen(["python", re.search(r"(.+)\\.+", __file__).group(1)+"\\server\\main.py"])).run()
threading.Thread(target=lambda: subprocess.Popen(["python", re.search(r"(.+)\\.+", __file__).group(1)+"\\app\\main.py"])).run()
