import calendar
import datetime

from flask import Blueprint, render_template, request, abort, url_for, redirect, flash
from flask_login import login_required, current_user
from sqlalchemy import or_

from weddingPlanner.extns import db
from weddingPlanner.model import Booking, Account, RefundPolicy, Notification

dashboard = Blueprint("dashboard", __name__, url_prefix="/dashboard")

bookings_status = ["all", "pending", "payment requested", "confirmed", "completed", "cancelled"]


def get_calender(month):
    today = datetime.date.today()
    first_day = today.replace(day=1)
    num_days = calendar.monthcalendar(today.year, month)

    return num_days


def add_notification(message, user_id):
    notification = Notification(title=message, user_id=user_id)
    db.session.add(notification)
    db.session.commit()


@dashboard.route("/")
@login_required
def index():
    bookings = current_user.profile.booking

    # CALCULATING EVERY TYPE OF BOOKING
    bookings_count_by_type = {
        "pending": 0,
        "payment requested": 0,
        "confirmed": 0,
        "completed": 0,
    }

    for booking in bookings:
        if booking.status == "cancelled":
            continue
        bookings_count_by_type[booking.status] += 1

    return render_template("vendor/dashboard.html"
                           , bookings_count_by_type=bookings_count_by_type)


@dashboard.route("/manage-booking")
@login_required
def manage_booking():
    search_customer_email = request.args.get("search_customer_email", None, type=str)
    search_event_date = request.args.get("search_event_date", None, type=str)
    search_event_status = request.args.get("search_event_status", 'All', type=str)

    search_params = {
        "search_customer_email": search_customer_email or '',
        "search_event_date": search_event_date or '',
        "search_event_status": search_event_status
    }

    selected_month = request.args.get("month", datetime.datetime.now().month, type=int)

    if selected_month > 12:
        selected_month = 1
    elif selected_month < 1:
        selected_month = 12

    calender = get_calender(selected_month)

    selected_month_name = calendar.month_name[selected_month]

    bookings = Booking.query.filter(Booking.profile_id == current_user.profile.id)
    current_month_bookings = bookings.filter(
        or_(Booking.status == "confirmed", Booking.status == "payment requested")).filter(
        db.extract('month', Booking.event_date) == selected_month).all()

    booking_days = [(int(booking.event_date.strftime("%d")), booking.status, booking.id) for booking in
                    current_month_bookings]
    for index_parent, calender_list in enumerate(calender):
        for index_child, day in enumerate(calender_list):
            if booking_days:
                for bdays in booking_days:
                    if day == bdays[0]:
                        calender[index_parent][index_child] = bdays
                        break

                    calender[index_parent][index_child] = (day, None, None)
            else:
                calender[index_parent][index_child] = (day, None, None)

    if search_customer_email:
        user = Account.query.filter_by(email=search_customer_email.lower()).first()
        bookings = bookings.filter(Booking.user_id == user.id)

    if search_event_date:
        search_event_date = datetime.datetime.strptime(search_event_date, "%Y-%m-%d")
        bookings = bookings.filter(Booking.event_date == search_event_date)

    if search_event_status and search_event_status.lower() != "all":
        bookings = bookings.filter(Booking.status == search_event_status.lower())

    bookings = bookings.order_by(Booking.booking_date.desc()).all()

    return render_template("vendor/manage-booking.html"
                           , calender=calender
                           , selected_month_name=selected_month_name
                           , selected_month=selected_month
                           , bookings=bookings
                           , search_params=search_params
                           , bookings_status=bookings_status)


@dashboard.route("/cancel-booking/<int:booking_id>")
@login_required
def cancel_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    if not booking in current_user.profile.booking:
        abort(403)

    booking.status = "cancelled"
    db.session.commit()

    add_notification(f"Your booking for {booking.event_name} at {booking.event_date} has been cancelled!", booking.booking_by.id)

    flash(f"{booking.booking_by.email}'s Booking Cancelled", "success")

    return redirect(url_for("vendor.dashboard.manage_booking"))


@dashboard.route("/view-booking/<int:booking_id>")
@login_required
def view_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    return render_template("vendor/view-booking.html"
                           , booking=booking)


@dashboard.route("/accept-booking/<int:booking_id>")
@login_required
def accept_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    if not booking in current_user.profile.booking:
        abort(403)

    booking.status = "payment requested"
    db.session.commit()

    add_notification(f"{current_user.profile.get_vendor().name} has requested you a payment!", booking.booking_by.id)

    flash(f"{booking.booking_by.email}'s Payment Requested", "success")

    return redirect(url_for("vendor.dashboard.manage_booking"))


@dashboard.route("/complete-booking/<int:booking_id>")
@login_required
def complete_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    if not booking in current_user.profile.booking:
        abort(403)

    booking.status = "completed"
    db.session.commit()

    add_notification(f"Your booking for {booking.event_name} at {booking.event_date} has been completed!", booking.booking_by.id)

    flash(f"{booking.booking_by.email}'s Booking Completed", "success")

    return redirect(url_for("vendor.dashboard.manage_booking"))


@dashboard.route("/policy", methods=["GET", "POST"])
@login_required
def policy():
    policy = current_user.profile.refund_policy

    if request.method == 'POST':
        days = request.form.get('days')
        desc = request.form.get('desc')

        if not policy:
            current_user.profile.refund_policy = RefundPolicy(days=days, description=desc)
        else:
            policy.days = days
            policy.description = desc

        db.session.commit()

        flash("Refund Policy Updated!", "success")
        return redirect(url_for("vendor.dashboard.policy"))

    return render_template("vendor/policy.html"
                           , policy=policy)
