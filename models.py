import os
import enum
import requests
from sqlalchemy import JSON
from app import db

cannabis_reports_url = "https://www.cannabisreports.com/api/v1.0/strains/search/"
headers = {
    'X-API-Key': os.getenv('CANNABIS_REPORTS_API'),
}

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
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(96), nullable=False)
    terpenes = db.relationship('Terpene', backref='compound', lazy=True)

    def __repr__(self):
        return f'<Compound {self.name}>'.format(self.name)


class TerpeneAromas(enum.Enum):
    herbal = 'Herbal'
    pine = 'Pine'
    peppery = 'Peppery'
    citrus = 'Citrus'
    fruity = 'Fruity'
    Sweet = 'Sweet'


class Terpene(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    aroma = db.Column(db.Enum(TerpeneAromas), nullable=False)
    compound_id = db.Column(db.Integer, db.ForeignKey('compound.id'), nullable=False)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'compound_id': self.compound.name
        }

    def __repr__(self):
        return '<Terpene %r>' % self.compound_id


class Strain(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(255), unique=False, nullable=True)
    genetics = db.Column(db.Text(), unique=True, nullable=True)
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
        REQUEST TO CANNABIS REPORTS API FOR IMAGE URL.
        """
        strain_query_url = cannabis_reports_url + "%s" % (self.name)
        r = requests.get(strain_query_url, headers)
        if r.status_code == 200:
            data = r.json()  # json strain object
            image_url = data['data'][0]['image']  # url property of object
            genetics = data['data'][0]['genetics']['names']
            lineage = data['data'][0]['lineage']
            self.image = image_url
            self.genetics = genetics
            self.lineage = lineage
            db.session.add(self)
            return db.session.commit()


    def __repr__(self):
        return '<Strain %r>' % self.name
