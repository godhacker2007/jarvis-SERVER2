import os
import subprocess
import webbrowser

def open_app(app_name):
    app_name = app_name.lower()

    apps = {
        "notepad": lambda: os.startfile("notepad.exe"),
        "calculator": lambda: os.startfile("calc.exe"),
        "cmd": lambda: os.startfile("cmd.exe"),

        # 🌐 Browsers / Web
        "chrome": lambda: subprocess.Popen(
            r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        ),
        "youtube": lambda: webbrowser.open("https://www.youtube.com"),
        "gmail": lambda: webbrowser.open("https://mail.google.com"),
        "whatsapp": lambda: webbrowser.open("https://web.whatsapp.com"),
        "google": lambda: webbrowser.open("https://www.google.com"),
        "chatgpt": lambda: webbrowser.open("https://www.chatgpt.com")
    }

    if app_name in apps:
        apps[app_name]()
        return f"Opening {app_name}"
    else:
        return "Sorry, I don't know this application"
