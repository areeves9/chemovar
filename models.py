from app import db


terpenes = db.Table('tags',
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


class Terpene(db.Model):
    id = db.Column(db.Integer, primary_key=True)
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

    def __repr__(self):
        return '<Strain %r>' % self.name
