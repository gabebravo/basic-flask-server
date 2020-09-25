from flask import Flask
from flask import request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://<user>:<password>@localhost:5432/<db_name>'
db = SQLAlchemy(app)


class Person(db.Model):
    __tablename__ = 'persons'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return f'<Person ID: {self.id}, name: {self.name}>'

    def getPerson(self, person):
        return f'<div>ID: {person.id}, name: {person.name}</div>'


db.create_all()


@app.route('/')
def index():
    person = Person.query.first()
    return f'Hello, {person.name}!'


@app.route('/all')
def all():
    str = ''
    for person in Person.query.all():
        str += person.getPerson(person)
    return f'info: {str}'


# http://localhost:5000/find-person?name=nicole
@app.route('/find-person')
def findPerson():
    person_name = request.args.get('name')
    person = Person.query.filter_by(name=person_name).all()
    return f'user: {person[0].getPerson(person[0])}' if len(person) > 0 else 'N/A'


@app.route('/add-person')  # http://localhost:5000/add-person?name=greg
def addPerson():
    person_name = request.args.get('name')
    person = Person(name=person_name)
    db.session.add(person)
    db.session.commit()
    return 'person was added successfully'


# http://localhost:5000/add-multiple?people=don,jon
@app.route('/add-multiple')
def addMultiple():
    people = request.args.get('people').split(',')
    all_people = [Person(name=person) for person in people]
    db.session.add_all(all_people)
    db.session.commit()
    return 'multiple peope were added successfully'


# http://localhost:5000/delete-person?name=solomon
@app.route('/delete-person')
def deletePerson():
    person_name = request.args.get('name')
    person = Person.query.filter_by(name=person_name).all()
    if len(person) > 0:
        db.session.delete(person[0])
        db.session.commit()
        return f'user: {person[0].name} was deleted'
    else:
        return f'woops that person couldnt be found'


# Implement a LIKE query to filter the users for records with a name that includes the letter "B" :
# Person.query.filter(Person.name.like('%B%')) >> exact character match

# Re-implement the LIKE query using case-insensitive search.
# Person.query.filter(Person.name.ilike('%b%')) >> case insensative

# Return only the first 5 records of the query above.
# Person.query.limit(100).all()

# Return the number of records of users with name 'Bob'.
# Person.query.filter(Person.name.like('Bob')) >> exact character match

if __name__ == '__main__':
    app.run()

# RUN THE APP WITH TERMINAL COMMAND :
# FLASK_DEBUG=true python3 flask-hello.py
