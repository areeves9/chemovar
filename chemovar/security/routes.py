from flask_security import security
from flask import (
    render_template,
)


@security.route('/register', methods=['GET'])
def register():
    return render_template('security/register_user.html')
    