from app import myapp, db
from app.database import *

@myapp.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User}