import csv
import os
from sqlalchemy.exc import SQLAlchemyError as e
from app import db
from models import Strain

direc = os.path.dirname(os.path.abspath(__file__))


def create_strain_instance(row):
    print(row['terpenes'])
    strain = Strain(
        name=row['name'],
        terpenes=row['terpenes'],
    )
    print(f"...adding Strain #{strain.name}, Strain ID: {strain.id}")


def seed_db():
    try:
        print("Seeding database, this will take several minutes...")
        with open('strains.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                create_strain_instance(row)
            print("Database seeded!")
    except e:
        print("Database error. Update aborted.")
        db.session.rollback()


seed_db()