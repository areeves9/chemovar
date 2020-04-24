from chemovar import db


class Assay(db.Model):
    """
    An assay has one terpene, a terpene can belong to 
    many assays.
    """
    id = db.Column(db.Integer, primary_key=True)
    conc = db.Column(db.Float(asdecimal=True, precision=3, decimal_return_scale=None), nullable=False)
    strain = db.Column(db.Integer, db.ForeignKey('strain.id'), nullable=False)
    terpene = db.Column(db.Integer, db.ForeignKey('terpene.id'), nullable=False)

    def __repr__(self):
        return f"<{self.terpene_assays} {round(self.conc, 3)}%>"
