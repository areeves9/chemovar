from chemovar import db


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
        return f"{self.compound.name}"

