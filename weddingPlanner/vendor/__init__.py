from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user

from weddingPlanner.extns import db
from weddingPlanner.model import Services, Profile
from .catering import catering
from .entertainment import entertainment
from .florist import florist
from .photographer import photographer
from .venue import venue
from .videographer import videographer
from .dashboard import dashboard

vendor = Blueprint("vendor", __name__, url_prefix="/vendor")

vendor.register_blueprint(venue)
vendor.register_blueprint(photographer)
vendor.register_blueprint(videographer)
vendor.register_blueprint(catering)
vendor.register_blueprint(florist)
vendor.register_blueprint(entertainment)
vendor.register_blueprint(dashboard)


def choose_profile_completion_redirection(service):
    if service == "venue":
        return redirect(url_for("vendor.venue.complete_profile"))

    elif service == "photographer":
        return redirect(url_for("vendor.photographer.complete_profile"))

    elif service == "videographer":
        return redirect(url_for("vendor.videographer.complete_profile"))

    elif service == "catering":
        return redirect(url_for("vendor.catering.complete_profile"))

    elif service == "florist":
        return redirect(url_for("vendor.florist.complete_profile"))

    elif service == "entertainment":
        return redirect(url_for("vendor.entertainment.complete_profile"))

    return None


@vendor.route("/choose-vendor", methods=['GET', 'POST'])
def choose_vendor():
    if current_user.profile:
        if not current_user.profile.is_completed:
            return choose_profile_completion_redirection(current_user.profile.service.service)

        return redirect(url_for('vendor.dashboard.index'))

    if request.method == 'POST':
        service = request.form.get('service')
        if not service:
            flash("Please select a service", "danger")
            return redirect(url_for("vendor.choose_vendor"))

        service = Services.query.filter_by(service=service).first()
        if not service:
            flash("Please select a valid service", "danger")
            return redirect(url_for("vendor.choose_vendor"))

        current_user.profile = Profile(service=service)
        try:
            db.session.commit()
            return choose_profile_completion_redirection(service.service)

        except:
            db.session.rollback()
            flash("An Error Occurred", "danger")
            return redirect(url_for("vendor.choose_vendor"))

    services = Services.query.all()

    return render_template("vendor/choose_vendor.html"
                           , services=services)
