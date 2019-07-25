from app import app, db
from app.models import User, Task

if __name__ == '__main__':
    db.create_all(app=app)
    #user = User(username='palo', email='pavol.jurak1@gmail.com')
    #user.set_password('palo01')
    #db.session.add(Task())
    #db.session.commit()