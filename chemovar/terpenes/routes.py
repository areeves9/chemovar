from flask import Blueprint, render_template
from flask import current_app as app
from .views import create_terpene, get_terpene_list


terpene_bp = Blueprint('terpene_bp', __name__,
                        template_folder='templates',
                        static_folder='static')


# ROUTES
@terpene_bp.route('/terpenes/', methods=['GET'])
def terpenes():
    """
    RETURN LIST OF TERPENE INSTANCES.
    """
    return get_terpene_list()


@terpene_bp.route('/terpenes/add/', methods=['GET', 'POST'])
def add_terpene():
    return create_terpene()