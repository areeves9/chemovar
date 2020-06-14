from flask import Blueprint
from flask_security import roles_required
from .views import (
    create_compound,
    get_compound_list,
    get_compound_object
)


compound_bp = Blueprint(
    'compound_bp', __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/compounds',
)


#ROUTES
@roles_required('Superuser', 'Admin')
@compound_bp.route('/compounds/add/', methods=['POST', 'GET'])
def add_compound():
    """
    CREATE A COMPOUND AND SAVE TO THE DB.
    """
    return create_compound()


@compound_bp.route('/compounds/', methods=['GET'])
def compounds():
    """
    RETURNS LIST OF COMPOUND INSTANCES FROM DB.
    """
    return get_compound_list()


@compound_bp.route('/compound/<int:id>/', methods=['GET'])
def compound(id):
    """
    RETURN COMPOUND INSTANCE FROM DB.
    """
    return get_compound_object(id)
