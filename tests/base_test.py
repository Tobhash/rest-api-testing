"""
Base Test

This class should be the parent class to each non-unit test.
It allows for instantiation of the database dynamically
and make sure that it is a new, blank database each time.
"""

from unittest import TestCase
from app import app
from db import db

class BaseTest(TestCase):
    @classmethod
    def setUpClass(cls):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'
        app.config['DEBUG'] = False
        app.config['PROPAGATE_EXCEPTIONS'] = True   # when exception occurs its bubbled up through the hierarchy
                                                    # and is not handle on the way
        with app.app_context():
            db.init_app(app)

    def setUp(self):
        # Make sure that db exists
        with app.app_context():
            db.create_all()
        # Get a test client
        self.app = app.test_client
        self.app_context = app.app_context()

    def tearDown(self):
        # Database is blank
        with app.app_context():
            db.session.remove()
            db.drop_all()


