from flask import (
    Flask,
    render_template,
    request,
    Response,
    stream_with_context,
    session,
    jsonify
)

import json
import uuid

from graph import app_graph
from llm import stream_answer


app = Flask(__name__)
app.secret_key = "agentic-secret"


# helpers
def get_store():
    if "conversations" not in session:
        session["conversations"] = {}
    return session["conversations"]


def get_current_id():
    if "current_chat" not in session:
        cid = str(uuid.uuid4())
        session["current_chat"] = cid
        get_store()[cid] = []
    return session["current_chat"]

# routes
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/conversations")
def conversations():
    store = get_store()

    items = []
    for cid, msgs in store.items():
        title = msgs[0][:40] if msgs else "New Chat"
        items.append({"id": cid, "title": title})

    return jsonify(items)


@app.route("/switch/<cid>")
def switch(cid):
    session["current_chat"] = cid
    return jsonify(success=True)


@app.route("/new")
def new_chat():
    cid = str(uuid.uuid4())
    get_store()[cid] = []
    session["current_chat"] = cid
    return jsonify(success=True)


@app.route("/chat", methods=["POST"])
def chat():
    question = request.json["question"]

    store = get_store()
    cid = get_current_id()
    history = store.get(cid, [])

    result = app_graph.invoke({
        "question": question,
        "history": history
    })

    contexts = result["contexts"]
    scores = result["scores"]

    def generate():
        full_answer = ""
        context_text = "\n\n".join(contexts)

        for token in stream_answer(context_text, question):
            full_answer += token
            yield f"data: {token}\n\n"

        history.append("User: " + question)
        history.append("Assistant: " + full_answer)

        store[cid] = history[-10:]
        session.modified = True

        confidence = sum(scores) / len(scores) if scores else 0

        yield (
            "event: done\n"
            f"data: {json.dumps({'contexts': contexts, 'confidence': confidence})}\n\n"
        )

    return Response(
        stream_with_context(generate()),
        mimetype="text/event-stream"
    )


if __name__ == "__main__":
    app.run(debug=False, use_reloader=False)
