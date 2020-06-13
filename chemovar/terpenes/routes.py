from flask import Blueprint
from flask_security import login_required
from .views import create_terpene, get_terpene_list


terpene_bp = Blueprint(
    'terpene_bp', __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/terpenes'
)



# ROUTES
@terpene_bp.route('/terpenes/', methods=['GET'])
def terpenes():
    """
    RETURN LIST OF TERPENE INSTANCES.
    """
    return get_terpene_list()


@terpene_bp.route('/terpenes/add/', methods=['GET', 'POST'])
@login_required
def add_terpene():
    return create_terpene()