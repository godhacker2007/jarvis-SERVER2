import json
import webbrowser
import subprocess
import os
import requests
import re
import datetime
import requests
import re
import json
import os

BASE_DIR = os.path.dirname(__file__)
DATASET_PATH = os.path.join(BASE_DIR, "dataset.json")

def get_time():
    now = datetime.datetime.now()
    return now.strftime("it's %I:%M %p")





class JarvisBrain:
    def __init__(self):
        self.load_dataset()
        self.pending_question = None

    def load_dataset(self):
        with open(DATASET_PATH, "r", encoding="utf-8") as f:
            self.dataset = json.load(f)

    def save_dataset(self):
        with open(DATASET_PATH, "w", encoding="utf-8") as f:
            json.dump(self.dataset, f, indent=2, ensure_ascii=False)

    def reply(self, message):
        msg = message.lower().strip()

        # 🔹 If learning mode ON
        if self.pending_question:
            self.dataset.append({
                "patterns": [self.pending_question],
                "response": message
            })
            self.save_dataset()
            self.pending_question = None
            return "Got it 👍 I will remember this."

        # 🔹 Normal dataset matching
        for item in self.dataset:
            if "patterns" in item and "response" in item:
                if msg in item["patterns"]:
                    return item["response"]

        # 🔹 Unknown question → ask user
        self.pending_question = msg
        return "I don't know this yet 🤔 Please tell me the answer."

# ONE brain instance
brain = JarvisBrain()

def process(message):
    return brain.reply(message)



# 🔹 YouTube play
def play_youtube(song):
    query = song.replace(" ", "+")
    html = requests.get(
        f"https://www.youtube.com/results?search_query={query}"
    ).text

    video_ids = re.findall(r"watch\?v=(\S{11})", html)
    if video_ids:
        url = "https://www.youtube.com/watch?v=" + video_ids[0]
        webbrowser.open(url)


def handle_command(text):
    text = text.lower().strip()

    # 🔹 OPEN APPS
    if "open notepad" in text:
        subprocess.Popen("notepad")
        return "Opening Notepad"

    elif "open cmd" in text or "open command prompt" in text:
        subprocess.Popen("cmd")
        return "Opening Command Prompt"

    elif "open chrome" in text:
        chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        subprocess.Popen(chrome_path)
        return "Opening Chrome"

    elif "open google" in text:
        webbrowser.open("https://www.google.com")
        return "Opening Google"

    elif "open chatgpt" in text:
        webbrowser.open("https://www.chatgpt.com")
        return "Opening ChatGPT"

    # 🔹 PLAY SONG
    elif text.startswith("play"):
        song = text.replace("play", "").strip()
        if song:
            play_youtube(song)
            return f"Playing {song} on YouTube"
        else:
            return "Which song should I play?"

    # 🔹 SEARCH GOOGLE
    elif text.startswith("search"):
        query = text.replace("search", "").strip()
        if query:
            webbrowser.open(f"https://www.google.com/search?q={query}")
            return f"Searching {query} on Google"
        else:
            return "What should I search?"
        
    elif any(x in text for x in ["time", "current time", "what's the time"]):
        return get_time()
    
    elif any(x in text for x in ["my location", "where am i", "current location"]):
        return "Getting your location..."

    elif any(x in text for x in ["weather", "temperature", "climate", "forecast", "how is the weather"]):
        return "Getting weather information..."

    elif (
        re.search(r"\b(image|picture|photo|art|pic|wallpaper|poster|logo|chobi)\b", text)
        or "ছবি" in text
        or re.search(r"\b(generate|create|make|draw|banao|banaw|banayo|toiri|create)\b", text)
        or re.search(r"\b(ghibli|ghibili|anime|manga|realistic|photorealistic|cartoon|3d|cinematic|4k|hd|portrait|sketch|painting|watercolor|oil|pixel|cyberpunk|fantasy|minimal|vector|render|comic|clay|isometric|vaporwave|steampunk|noir)\b", text)
        or looks_like_plain_image_prompt(text)
    ):
        return "Generating image..."


    # 🔹 DATASET CHAT (hello, hi, how are you)
    reply = brain.reply(text)
    if reply:
        return reply

    # 🔹 FALLBACK
    return "Sorry, I am still learning."


def looks_like_plain_image_prompt(text):
    if not text:
        return False

    if re.search(r"^(what|why|how|when|where|who|which|tell|explain|define|is|are|do|does|can)\b", text):
        return False

    if "?" in text:
        return False

    if re.search(r"^(open|search|play|weather|time|current time|my location|where am i)\b", text):
        return False

    if re.search(r"^(hi|hello|hey|thanks|thank you|ok|okay|yes|no)\b", text):
        return False

    return len(text.split()) <= 14


# 🔹 API entry
def process(message):
    return handle_command(message)


