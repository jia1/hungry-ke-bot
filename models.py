from manage import app, db

class MenuItem(db.Model):
    __tablename__ = 'menu_items'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    week = db.Column(db.String(32))
    day = db.Column(db.String(16))
    type_of_meal = db.Column(db.String(16))
    name = db.Column(db.String(64), nullable=False)
    # is_halal = db.Column(db.Boolean)
    # is_vegetarian = db.Column(db.Boolean)
    dishes = db.Column(db.String(512))

    def __repr__(self):
        return '<MenuItem(date=%r,name=%r,dishes=%r)>' % (self.date.strftime('%Y-%m-%d'), self.name, self.dishes.split(','))
