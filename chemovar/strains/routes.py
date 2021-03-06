# Import views
from .views import (
    get_autocomplete,
    get_index,
    create_strain,
    get_search_results,
    get_strain_list,
    get_strain_object,
)
# Import package dependencies
from flask import (
    Blueprint,
    request,
)

from flask_security import roles_required


# Create Flask Blueprint object
strain_bp = Blueprint(
    'strain_bp',
    __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/strains'
)


# Routes
@strain_bp.route('/', methods=['GET'])
def index():
    return get_index()


@strain_bp.route('/autocomplete', methods=['GET'])
def autocomplete():
    return get_autocomplete()


@strain_bp.route('/success', methods=['GET', 'POST'])
def success():
    strain = request.form['strain']
    return get_search_results(strain)


@strain_bp.route('/strains/', methods=['GET'])
def strains():
    """
    RETURNS UNORDERED LIST OF STRAINS FROM THE DB.
    """
    return get_strain_list()


@strain_bp.route('/strains/<int:id>/', methods=['GET'])
def strain(id):
    """
    RETURNS STRAIN INSTANCE DETAIL TEMPLATE.
    """
    return get_strain_object(id)


@roles_required('Superuser', 'Admin')
@strain_bp.route('/strains/add/', methods=['GET', 'POST'])
def add_strain():
    """
    CREATE A COMPOUND AND SAVE TO THE DB.
    """
    return create_strain()
