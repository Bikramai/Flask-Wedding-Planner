from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user

from weddingPlanner.extns import save_form_images, db
from weddingPlanner.model import Entertainment

entertainment = Blueprint("entertainment", __name__, url_prefix="/entertainment")


@entertainment.route("/complete-profile", methods=["GET", "POST"])
@login_required
def complete_profile():
    if current_user.profile.is_completed:
        return redirect(url_for('vendor.dashboard.index'))

    if request.method == 'POST':
        service_name = request.form.get("service_name")
        price = request.form.get("per_day_price")
        about = request.form.get("about")
        contact_email = request.form.get("contact_email")
        phone_number = request.form.get("phone_number")
        address = request.form.get("address")
        city = request.form.get("city")

        # Saving Uploaded Images
        images = request.files.getlist("images")
        filenames = save_form_images(images, "entertainment")

        new_entertainment = Entertainment(
            name=service_name,
            price=price,
            description=about,
            contact_email=contact_email,
            address=address,
            city=city,
            contact_number=phone_number,
            images=filenames
        )

        current_user.profile.entertainment = new_entertainment
        current_user.profile.is_completed = True

        try:
            db.session.commit()
            # REDIRECT TO DASHBOARD
            flash("Profile Created Successfully", 'success')
            return redirect(url_for('vendor.dashboard.index'))
        except:
            db.session.rollback()
            flash("An Error Occurred", "danger")

    return render_template("vendor/entertainment/complete-profile.html")
