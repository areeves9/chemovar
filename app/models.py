import os
import requests
from sqlalchemy import JSON
from app.app import db

cannabis_reports_url = os.getenv('CANNABIS_REPORTS_URL')
headers = {
    'X-API-Key': os.getenv('CANNABIS_REPORTS_API'),
}

# the intermediate ("JOIN") table where Terpene and Strain
# table's rows have a fk-relation. The many-to-many relation
# is a fk-relation pair.
terpenes = db.Table(
    'tags',
    db.Column(
        'terpene_id', db.Integer,
        db.ForeignKey('terpene.id'),
        primary_key=True
    ),
    db.Column(
        'strain_id', db.Integer,
        db.ForeignKey('strain.id'),
        primary_key=True
    )
)


class Compound(db.Model):
    """
    A many-to-one relationship to Terpene. To account for
    variations in analytical testing, there can be many terpene
    instances for one compound. Test data can be stored on the
    terpene model.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(96), nullable=False)
    terpenes = db.relationship('Terpene', backref='compound', lazy=True)

    def __repr__(self):
        return f'<Compound {self.name}>'.format(self.name)


class Terpene(db.Model):
    """
    A model with a an fk relationship to Compound.
    This allows for future additions to the Terpene
    model such as %-composition (ie. testing COAs).
    """
    id = db.Column(db.Integer, primary_key=True)
    aroma = db.Column(db.String(255), nullable=False)
    compound_id = db.Column(db.Integer, db.ForeignKey('compound.id'), nullable=False)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'compound_id': self.compound.name
        }

    def __repr__(self):
        return f'<Terpene {self.compound.name}>'


class Strain(db.Model):
    """
    A model with a many-to-many relation set to the field
    terpenes. A strain can have many terpenes, and many 
    terpenes can belong to a strain.
    """
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(255), unique=False, nullable=True)
    genetics = db.Column(db.Text(), unique=False, nullable=True)
    lineage = db.Column(JSON, nullable=True)
    name = db.Column(db.String(96), unique=True, nullable=False)
    terpenes = db.relationship('Terpene', secondary=terpenes, lazy='subquery', backref=db.backref('strains', lazy=True))

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'terpenes': self.serialize_many2many,
        }

    @property
    def serialize_many2many(self):
        return [i.serialize for i in self.terpenes]

    def get_strain_data(self):
        """
        This method is a GET request to cannabisreports API
        passing strain name as a query param. The server returns
        JSON which is parsed and set to the strain instance attributes.
        """
        strain_query_url = cannabis_reports_url + "%s" % (self.name)
        r = requests.get(strain_query_url, headers)
        if r.status_code == 200:
            data = r.json()  # json strain object
            print(data)
            if len(data['data']) > 0:
                image_url = data['data'][0]['image']  # url property of object
                genetics = data['data'][0]['genetics']['names']
                lineage = data['data'][0]['lineage']
                self.image = image_url
                self.genetics = genetics
                self.lineage = lineage
                db.session.add(self)
            else:
                pass
            return db.session.commit()

    def __repr__(self):
        return '<Strain %r>' % self.name