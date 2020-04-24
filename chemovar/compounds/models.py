from chemovar import db


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
        return f"<Compound {self.name}>"
