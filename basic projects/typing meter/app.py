from flask import Flask, render_template
import random

app = Flask(__name__)

# sample text
texts = [
    "Typing speed tests can improve your efficiency at work.In a world driven by technology, the ability to type swiftly and accurately is a game-changer.",
    "Typing is an essential skill in the modern world. It helps you communicate quickly and efficiently. Whether you are writing an email, chatting with friends, or completing a school project, typing accurately saves time. With practice, you can become a faster and better typist.",
    "Technology has changed the way we live. Computers, smartphones, and the internet have made our lives easier and more connected. Typing is a crucial skill that allows us to use these tools effectively. Everyone can benefit from improving their typing speed.",
    "Technology evolves rapidly, shaping the future of humanity.A journey of a thousand miles begins with a single step."
]

@app.route("/")
def index():
    
    random_text = random.choice(texts)
    return render_template("index.html", text=random_text)

if __name__ == "__main__":
    app.run(debug=True)
