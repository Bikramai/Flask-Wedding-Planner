from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from weddingPlanner.model import Account, Messages, ChatThread
from weddingPlanner.extns import db

chat = Blueprint("chat", __name__, url_prefix="/chat")


@chat.get("/chat")
@login_required
def index():

    if current_user.is_vendor():
        chats = ChatThread.query.filter_by(vendor_id=current_user.id).all()
    else:
        chats = ChatThread.query.filter_by(customer_id=current_user.id).all()

    return render_template("chat/index.html"
                           , chats=chats)


@chat.get("/start_chat/<start_with>")
@login_required
def start_chat(start_with):
    receiver_account = Account.query.get_or_404(start_with)

    if current_user.is_vendor():
        chatThread = ChatThread.query.filter_by(customer_id=receiver_account.id, vendor_id=current_user.id).first()
        if not chatThread:
            chatThread = ChatThread(customer_id=receiver_account.id, vendor_id=current_user.id)
            db.session.add(chatThread)
            db.session.commit()
    else:
        chatThread = ChatThread.query.filter_by(customer_id=current_user.id, vendor_id=receiver_account.id).first()
        if not chatThread:
            chatThread = ChatThread(customer_id=current_user.id, vendor_id=receiver_account.id)
            db.session.add(chatThread)
            db.session.commit()

    messages = Messages.query.filter_by(chat_thread_id=chatThread.id).all()

    return render_template("chat/start_chat.html"
                           , receiver_account=receiver_account
                           , all_messages=messages)


@chat.post("/send_message")
@login_required
def send_message():
    message = request.form.get("message")
    receiver_id = request.form.get("receiver_id")

    if current_user.is_vendor():
        chatThread = ChatThread.query.filter_by(customer_id=receiver_id, vendor_id=current_user.id).first()
    else:
        chatThread = ChatThread.query.filter_by(customer_id=current_user.id, vendor_id=receiver_id).first()

    new_message = Messages(message=message, sender_id=current_user.id)
    chatThread.messages.append(new_message)
    db.session.commit()

    return {"success": True, "message": message}, 200