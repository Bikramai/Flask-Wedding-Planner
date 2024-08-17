from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user

from weddingPlanner.extns import save_form_images, db
from weddingPlanner.model import Venue

venue = Blueprint("venue", __name__, url_prefix="/venue")


@venue.route("/complete-profile", methods=["GET", "POST"])
@login_required
def complete_profile():
    if current_user.profile.is_completed:
        return redirect(url_for('vendor.dashboard.index'))

    if request.method == 'POST':
        venue_name = request.form.get("venue_name")
        per_day_price = request.form.get("per_day_price")
        total_guests = request.form.get("total_guests")
        about = request.form.get("about")
        contact_email = request.form.get("contact_email")
        phone_number = request.form.get("phone_number")
        address = request.form.get("address")
        city = request.form.get("city")

        # Saving Uploaded Images
        images = request.files.getlist("images")
        filenames = save_form_images(images, "venue")

        new_venue = Venue(
            name=venue_name,
            description=about,
            price=per_day_price,
            number_of_guests=total_guests,
            contact_email=contact_email,
            address=address,
            city=city,
            contact_number=phone_number,
            images=filenames
        )

        current_user.profile.venue = new_venue
        current_user.profile.is_completed = True

        try:
            db.session.commit()
            # REDIRECT TO DASHBOARD
            flash("Profile Created Successfully", 'success')
            return redirect(url_for('vendor.dashboard.index'))
        except:
            db.session.rollback()
            flash("An Error Occurred", "danger")

    return render_template("vendor/venue/complete-profile.html")
