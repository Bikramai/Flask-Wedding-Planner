from datetime import datetime

from flask_login import UserMixin, current_user
from sqlalchemy import Column, Integer, String, ForeignKey, Text, Float, JSON, Boolean

from .extns import db


class Account(db.Model, UserMixin):
    id = Column(Integer, primary_key=True)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(60), nullable=False)
    account_type = Column(String(10), nullable=False)

    profile = db.relationship("Profile", backref="account", uselist=False)

    def __init__(self, email, password, account_type):
        self.email = email
        self.password = password
        self.account_type = account_type

    def is_vendor(self):
        return True if self.profile else False

    def get_notifications(self):
        return Notification.query.filter_by(user_id=self.id).order_by(Notification.id.desc()).limit(7).all()


class Profile(db.Model):
    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey('account.id'), nullable=False)
    service_id = Column(Integer, ForeignKey('services.id'), nullable=False)
    venue_id = Column(Integer, ForeignKey('venue.id'), nullable=True)
    caterer_id = Column(Integer, ForeignKey('caterer.id'), nullable=True)
    entertainment_id = Column(Integer, ForeignKey('entertainment.id'), nullable=True)
    videographer_id = Column(Integer, ForeignKey('videographer.id'), nullable=True)
    florist_id = Column(Integer, ForeignKey('florist.id'), nullable=True)
    photographer_id = Column(Integer, ForeignKey('photographer.id'), nullable=True)
    is_completed = Column(Boolean, nullable=False, default=False)

    refund_policy = db.relationship("RefundPolicy", backref="profile", uselist=False)

    def get_vendor(self):
        if self.venue_id:
            return self.venue
        elif self.caterer_id:
            return self.caterer
        elif self.entertainment_id:
            return self.entertainment
        elif self.videographer_id:
            return self.videographer
        elif self.florist_id:
            return self.florist
        elif self.photographer_id:
            return self.photographer

    def get_vendor_type(self):
        return self.service.service

    def get_balance(self):
        vendor_type = self.get_vendor_type()

        total_earning = 0
        for booking in self.booking:
            if booking.status == 'completed':
                total_earning += booking.get_total_price()

        return total_earning


class Services(db.Model):
    id = Column(Integer, primary_key=True)
    service = Column(String(50), nullable=False)

    profiles = db.relationship("Profile", backref="service")


class Venue(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    description = Column(Text, nullable=False)
    price = Column(Float, nullable=False)
    number_of_guests = Column(Integer, nullable=False)
    contact_email = Column(String(120), nullable=False)
    address = Column(String(120), nullable=False)
    city = Column(String(120), nullable=False)
    contact_number = Column(String(20), nullable=False)
    images = Column(JSON, nullable=False, default=[])

    def get_price(self):
        return f"${self.price} per day"

    profile = db.relationship("Profile", backref="venue", uselist=False)


class Caterer(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    description = Column(Text, nullable=False)
    contact_email = Column(String(120), nullable=False)
    address = Column(String(120), nullable=False)
    city = Column(String(120), nullable=False)
    contact_number = Column(String(20), nullable=False)
    images = Column(JSON, nullable=False, default=[])

    def get_price(self):
        return f"Starting from ${self.menu[0].price}"

    menu = db.relationship("VendorMenu", backref="caterer")
    profile = db.relationship("Profile", backref="caterer", uselist=False)


class VendorMenu(db.Model):
    id = Column(Integer, primary_key=True)
    caterer_id = Column(Integer, ForeignKey('caterer.id'))
    florist_id = Column(Integer, ForeignKey('florist.id'))
    name = Column(String(50), nullable=False)
    description = Column(Text, nullable=False)
    price = Column(Float, nullable=False)


class Florist(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    description = Column(Text, nullable=False)
    contact_email = Column(String(120), nullable=False)
    address = Column(String(120), nullable=False)
    city = Column(String(120), nullable=False)
    contact_number = Column(String(20), nullable=False)
    images = Column(JSON, nullable=False, default=[])

    def get_price(self):
        return f"Starting from ${self.menu[0].price}"

    menu = db.relationship("VendorMenu", backref="florist")
    profile = db.relationship("Profile", backref="florist", uselist=False)


class Photographer(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    description = Column(Text, nullable=False)
    contact_email = Column(String(120), nullable=False)
    address = Column(String(120), nullable=False)
    city = Column(String(120), nullable=False)
    contact_number = Column(String(20), nullable=False)
    images = Column(JSON, nullable=False, default=[])
    price = Column(Float, nullable=False)
    profile = db.relationship("Profile", backref="photographer", uselist=False)

    def get_price(self):
        return f"${self.price} per day"


class Videographer(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    description = Column(Text, nullable=False)
    contact_email = Column(String(120), nullable=False)
    address = Column(String(120), nullable=False)
    city = Column(String(120), nullable=False)
    contact_number = Column(String(20), nullable=False)
    images = Column(JSON, nullable=False, default=[])
    price = Column(Float, nullable=False)

    profile = db.relationship("Profile", backref="videographer", uselist=False)

    def get_price(self):
        return f"${self.price} per day"


class Entertainment(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    description = Column(Text, nullable=False)
    contact_email = Column(String(120), nullable=False)
    address = Column(String(120), nullable=False)
    city = Column(String(120), nullable=False)
    contact_number = Column(String(20), nullable=False)
    images = Column(JSON, nullable=False, default=[])
    price = Column(Float, nullable=False)

    def get_price(self):
        return f"${self.price} per day"

    profile = db.relationship("Profile", backref="entertainment", uselist=False)


class Booking(db.Model):
    id = Column(Integer, primary_key=True)
    event_name = Column(String(50), nullable=False)
    event_date = Column(db.Date, nullable=False)
    event_time = Column(db.Time, nullable=False)
    description = Column(Text)
    booking_date = Column(db.DateTime, default=datetime.now())
    status = Column(String(20), nullable=False, default="pending")
    guests = Column(Integer, nullable=True)

    profile_id = Column(Integer, ForeignKey('profile.id'))
    user_id = Column(Integer, ForeignKey('account.id'))
    package_id = Column(Integer, ForeignKey('vendor_menu.id'))

    booking_by = db.relationship("Account", backref="booking")
    profile = db.relationship("Profile", backref="booking")
    package = db.relationship("VendorMenu", backref="booking")

    def get_total_price(self):
        if self.package and self.guests is not None:
            return self.guests * self.package.price
        elif self.package:
            return self.package.price
        else:
            return self.profile.get_vendor().price


class RefundPolicy(db.Model):
    id = Column(Integer, primary_key=True)
    days = Column(Integer, nullable=False)
    description = Column(Text, nullable=False)

    profile_id = Column(Integer, ForeignKey('profile.id'), unique=True)


class Todo(db.Model):
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    account_id = Column(Integer, ForeignKey('account.id'), nullable=False)

    account = db.relationship("Account", backref="todo")


class ChatThread(db.Model):
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('account.id'), nullable=False)
    vendor_id = Column(Integer, ForeignKey('account.id'), nullable=False)

    def get_receiver_title(self):
        if current_user.is_vendor():
            account = Account.query.get(self.customer_id)
            return account.email
        else:
            account = Account.query.get(self.vendor_id)
            return account.profile.get_vendor().name


class Messages(db.Model):
    id = Column(Integer, primary_key=True)
    message = Column(Text, nullable=False)
    sent_time = Column(db.DateTime, default=datetime.now())
    chat_thread_id = Column(Integer, ForeignKey('chat_thread.id'), nullable=False)
    sender_id = Column(Integer, ForeignKey('account.id'), nullable=False)

    chat = db.relationship("ChatThread", backref="messages")
    sender = db.relationship("Account", backref="messages")

    def is_sender_vendor(self):
        return self.sender_id == self.chat.vendor_id


class Notification(db.Model):
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    user_id = Column(Integer, ForeignKey('account.id'), nullable=False)

    user = db.relationship("Account", backref="notification")