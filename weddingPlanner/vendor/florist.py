from flask import Blueprint, render_template, request, flash, redirect, url_for
from weddingPlanner.extns import save_form_images, db
from flask_login import login_required, current_user
from weddingPlanner.model import Florist, VendorMenu

florist = Blueprint("florist", __name__, url_prefix="/florist")


@florist.route("/complete-profile", methods=['GET', 'POST'])
@login_required
def complete_profile():

    if current_user.profile.is_completed:
        return redirect(url_for('vendor.dashboard.index'))

    if request.method == 'POST':
        caterer_name = request.form.get("florist_name")
        about = request.form.get("about")
        contact_email = request.form.get("contact_email")
        phone_number = request.form.get("phone_number")
        address = request.form.get("address")
        city = request.form.get("city")

        # Saving Uploaded Images
        images = request.files.getlist("images")
        filenames = save_form_images(images, "florist")

        new_florist = Florist(
            name=caterer_name,
            description=about,
            contact_email=contact_email,
            address=address,
            city=city,
            contact_number=phone_number,
            images=filenames
        )

        plan_names = request.form.getlist("plan_name")
        plan_prices = request.form.getlist("plan_price")
        plan_description = request.form.getlist("plan_description")

        for name, price, description in zip(plan_names, plan_prices, plan_description):
            plan = VendorMenu(
                name=name,
                price=price,
                description=description
            )

            new_florist.menu.append(plan)

        current_user.profile.florist = new_florist
        current_user.profile.is_completed = True

        try:
            db.session.commit()
            # REDIRECT TO DASHBOARD
            flash("Profile Created Successfully", 'success')
            return redirect(url_for('vendor.dashboard.index'))
        except:
            db.session.rollback()
            flash("An Error Occurred", "danger")

    return render_template("vendor/florist/complete-profile.html")
