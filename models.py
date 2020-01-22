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
    percent_concentration = db.Column(db.Numeric(precision=10, scale=20), nullable=True)
    terpenes = db.relationship('Terpene', backref='compound', lazy=True)

    def __repr__(self):
        return f'<Compound {self.name} @{self.percent_concentration}%>'.format(self.name, self.percent_concentration)


class Terpene(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    compound_id = db.Column(db.Integer, db.ForeignKey('compound.id'), nullable=False)

    def __repr__(self):
        return '<Terpene %r>' % self.compound_id


class Strain(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(96), unique=True, nullable=False)
    terpenes = db.relationship('Terpene', secondary=terpenes, lazy='subquery', backref=db.backref('strains', lazy=True))

    def __repr__(self):
        return '<Strain %r>' % self.name
