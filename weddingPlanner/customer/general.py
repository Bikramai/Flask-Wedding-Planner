import calendar
import datetime

from flask import render_template, request, flash, redirect, url_for, abort
from flask_login import login_required, current_user
from sqlalchemy import or_

from weddingPlanner.customer import customer
from weddingPlanner.extns import db
from weddingPlanner.model import Venue, Caterer, Entertainment, Videographer, Florist, Photographer, Profile, Services, \
    Booking, Notification


def filter_vendor(Vendor, name, location):
    vendor_query = Vendor.query
    if name:
        vendor_query = vendor_query.filter(Vendor.name.ilike(f"%{name}%"))

    if location:
        vendor_query = vendor_query.filter_by(city=location)

    vendor_query = vendor_query.order_by(Vendor.id.desc()).all()

    return vendor_query


def get_vendors(name, start_price, end_price, location, type='all'):
    vendors = dict()

    if end_price and start_price:
        if end_price < start_price:
            raise ValueError

    if type.lower() == 'venue' or type.lower() == 'all':
        vendors['venue'] = filter_vendor(Venue, name, location)

    if type.lower() == 'catering' or type.lower() == 'all':
        vendors['catering'] = filter_vendor(Caterer, name, location)

    if type.lower() == 'photographer' or type.lower() == 'all':
        vendors['photographer'] = filter_vendor(Photographer, name, location)

    if type.lower() == 'videographer' or type.lower() == 'all':
        vendors['videographer'] = filter_vendor(Videographer, name, location)

    if type.lower() == 'entertainment' or type.lower() == 'all':
        vendors['entertainment'] = filter_vendor(Entertainment, name, location)

    if type.lower() == 'florist' or type.lower() == 'all':
        vendors['florist'] = filter_vendor(Florist, name, location)

    if start_price or end_price:
        for key, value in vendors.items():
            if key in ['catering', 'florist']:
                for index, ven in enumerate(vendors[key]):
                    if start_price:
                        if ven.menu[0].price < start_price:
                            del vendors[key][index]

                    if end_price:
                        if ven.menu[0].price > end_price:
                            del vendors[key][index]
            else:
                for index, ven in enumerate(vendors[key]):
                    if start_price:
                        if ven.price < start_price:
                            del vendors[key][index]

                    if end_price:
                        if ven.price > end_price:
                            del vendors[key][index]

    return vendors


def get_calender(month):
    today = datetime.date.today()
    first_day = today.replace(day=1)
    num_days = calendar.monthcalendar(today.year, month)

    return num_days


def add_notification(message, user_id):
    notification = Notification(title=message, user_id=user_id)
    db.session.add(notification)
    db.session.commit()


@customer.route("/")
def index():
    if current_user.is_authenticated and current_user.profile:
        return redirect(url_for("vendor.dashboard.index"))
    # Handling URL Arguments
    search_vendor_name = request.args.get("vendor_name", None, type=str)
    search_start_price = request.args.get("start_price", None, type=int)
    search_end_price = request.args.get("end_price", None, type=int)
    search_vendor_location = request.args.get("vendor_location", None, type=str)
    search_vendor_type = request.args.get("service", "All", type=str)

    search_params = {
        "vendor_name": search_vendor_name or '',
        "start_price": search_start_price or '',
        "end_price": search_end_price or '',
        "vendor_location": search_vendor_location or '',
        "service": search_vendor_type or ''
    }

    try:
        vendors = get_vendors(search_vendor_name, search_start_price, search_end_price, search_vendor_location,
                              search_vendor_type)
    except ValueError:
        vendors = get_vendors()
        flash("End price cannot be less than start price", "danger")
        return redirect(url_for("customer.index"))

    services = Services.query.all()

    return render_template("customer/index.html"
                           , services=services
                           , vendors=vendors
                           , search_params=search_params)


@customer.route("/vendor-profile/<profile_id>")
def view_vendor_profile(profile_id):
    selected_month = request.args.get("month", datetime.datetime.now().month, type=int)

    profile = Profile.query.get_or_404(profile_id)
    vendor = profile.get_vendor()
    service = profile.service.service

    if selected_month > 12:
        selected_month = 1
    elif selected_month < 1:
        selected_month = 12

    calender = get_calender(selected_month)
    selected_month_name = calendar.month_name[selected_month]

    bookings = Booking.query.filter(Booking.profile_id == profile.id).filter(
        or_(Booking.status == "confirmed")).filter(
        db.extract('month', Booking.event_date) == selected_month).all()

    booking_days = [(int(booking.event_date.strftime("%d")), booking.status, booking.id) for booking in
                    bookings]

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

    return render_template("view-vendor-profile.html"
                           , vendor=vendor
                           , calender=calender
                           , selected_month_name=selected_month_name
                           , selected_month=selected_month)


@customer.route("/book", methods=['POST'])
@login_required
def book():
    if request.method == 'POST':
        event_name = request.form.get("event_name")
        date = datetime.datetime.strptime(request.form.get("date"), '%Y-%m-%d').date()
        time = datetime.datetime.strptime(request.form.get("start_time"), '%H:%M').time()
        profile_id = request.form.get("profile_id")
        desc = request.form.get("desc") or None
        package = request.form.get("package") or None
        guests = request.form.get("guests") or None

        if date < datetime.datetime.now().date() or (
                date == datetime.datetime.now().date() and time < datetime.datetime.now().time()):
            flash("Invalid Date or Time", 'danger')
            return redirect(url_for("customer.view_vendor_profile", profile_id=profile_id))

        new_booking = Booking(event_name=event_name, event_date=date, event_time=time, description=desc,
                              profile_id=profile_id, package_id=package, guests=guests)
        current_user.booking.append(new_booking)

        try:
            db.session.commit()
            flash("Booking Requested! Vendor will contact you soon!", 'success')

            add_notification(f"You have a new booking request from {current_user.email}!", new_booking.profile.account_id)
        except Exception:
            db.session.rollback()
            flash("An Error Occurred", 'danger')

        return redirect(url_for("customer.view_vendor_profile", profile_id=profile_id))


@customer.route("/booking", methods=['GET'])
@login_required
def view_booking():
    bookings = current_user.booking
    bookings.reverse()
    return render_template("customer/view_booking.html"
                           , bookings=bookings)


@customer.route("/cancel-booking/<booking_id>", methods=['GET'])
@login_required
def cancel_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    if not booking in current_user.booking:
        abort(403)

    if booking.status == 'confirmed':
        days_passed_after_booking = (datetime.datetime.now().date() - booking.booking_date.date()).days
        if days_passed_after_booking > booking.profile.refund_policy.days:
            flash(f"Booking Cannot be refunded! As it's more than {booking.profile.refund_policy.days} Days", "danger")
            return redirect(url_for("customer.view_booking"))

    booking.status = "cancelled"
    db.session.commit()

    add_notification(f"Booking by {booking.booking_by.email} is being cancelled!", booking.profile.account_id)

    flash("Booking Cancelled", "success")

    return redirect(url_for("customer.view_booking"))


@customer.route("/booking/pay/<booking_id>", methods=['POST'])
@login_required
def payment(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    if not booking in current_user.booking:
        abort(403)

    booking.status = "confirmed"
    db.session.commit()

    add_notification(f"Booking by {booking.booking_by.email} is being confirmed!", booking.profile.account_id)

    flash("Payment Successfully! Your booking has been confirmed", "success")

    return redirect(url_for("customer.view_booking"))
