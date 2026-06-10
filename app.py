



@app.route('/')
def home():
    return "Jarvis server is running!"

@app.route("/")
def ui():
    return send_from_directory(frontend, "index.html")

@app.route("/chat", methods=["POST"])
def chat1():
    data = request.get_json()
    user_msg = data.get("message", "").strip().lower()
   
    if not user_msg:
        return jsonify({"reply": "No message received"})
    
    command_reply = handle_command(user_msg)
    if command_reply:
        return jsonify({"reply": command_reply})

    reply = process(user_msg)
    return jsonify({"reply": reply})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
