from flask import Blueprint

bp = Blueprint('prob', __name__)

from app.prob import routes
