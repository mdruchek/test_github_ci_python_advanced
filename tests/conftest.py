import sys
from datetime import datetime, timedelta

import pytest
sys.path.append('../test_github_ci_python_advanced')

from test_github_ci_python_advanced.app import create_app
from test_github_ci_python_advanced.app.database import db as _db
from test_github_ci_python_advanced.app.models import Client, Parking, ClientParking


@pytest.fixture
def app():
    _app = create_app()
    _app.config['SQLALCHEMY_ECHO'] = True
    _app.config['TESTING'] = True
    _app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'

    with _app.app_context():
        _db.create_all()

        client = Client(
            name='test_name_client',
            surname='test_surname_client',
            credit_card='test_credit_card_client',
            car_number='test_car_number'
        )

        parking = Parking(
            address='test_address_parking',
            opened=True,
            count_places=100,
            count_available_places=100
        )

        client_parking = ClientParking(
            client_id=1,
            parking_id=1,
            time_in=datetime.now(),
            time_out=datetime.now() + timedelta(minutes=10)
        )

        _db.session.add(client)
        _db.session.add(parking)
        _db.session.add(client_parking)
        _db.session.commit()

        yield _app

        _db.session.close()
        _db.drop_all()


@pytest.fixture
def web_client(app):
    client = app.test_client()
    return client


@pytest.fixture
def db(app):
    with app.app_context():
        yield _db
