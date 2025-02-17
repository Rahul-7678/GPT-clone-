from flask import Flask, render_template, request, jsonify
from flask_pymongo import PyMongo
import openai



app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/myDatabase"
mongo = PyMongo(app)

@app.route("/")
def home():
    chats = mongo.db.chats.find({})
    mychats = [chat for chat in chats]
    print(mychats)
    return render_template("index.html", mychats = mychats)  # Ensure 'index.html' exists in the 'templates' folder

@app.route("/api", methods=["GET", "POST"])
def qa():
    if request.method == "POST":
        print(request.json)
        question = request.json.get("question")
        chat = mongo.db.find_one({"question": question})
        print(chat)

        if chat:
            data = {"result": f"{chat['answer']}"}
            return jsonify(data)
        else:
            data = {"result": f"answer of {question}"}
            response = client.chat.completions.create(
                model="o1-preview-2024-09-12",
                prompt = question,
                temperature =0.7,
                max_tokens=256,
                frequency_penalty = 0,
                presence_penalty = 0
                )
            mongo.db.chats.insert_one({"question": question, "answer":response})
            return jsonify(data)
    data = {"result": "Hey! How's it going? 😊"}

    return jsonify(data)

    
app.run(debug=True)


