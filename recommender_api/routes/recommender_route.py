from flask import Blueprint
from recommender_api.controller.account_controller import AccountController
from recommender_api.controller.status_controller import StatusController

blueprint = Blueprint("recommender_route", __name__)

account_controller = AccountController()
status_controller = StatusController()

blueprint.route("/accounts/<account_id>/create-sorted-timeline", methods=["POST"])(account_controller.sort_timeline)

blueprint.route("/statuses/<status_id>/generate-interests", methods=["GET"])(status_controller.generate_interests)