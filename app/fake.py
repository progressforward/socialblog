from sqlalchemy.exc import IntegrityError
from random import seed, randint
import forgery_py
from .models import User, Post
from . import db
        
def users(count=100):
    seed()
    #r = Role.query.filter_by(name='User').first()
    for i in range(count):
        u = User(email=forgery_py.internet.email_address(),
            username=forgery_py.internet.user_name(True),
            password=forgery_py.lorem_ipsum.word(),
            #role= r,
            confirmed=True,
            name=forgery_py.name.full_name(),
            location=forgery_py.address.city(),
            about_me=forgery_py.lorem_ipsum.sentence(),
            member_since=forgery_py.date.date(True))
        db.session.add(u)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            
def posts(count=100):     
    seed()
    user_count = User.query.count()
    for i in range(count):
        u = User.query.offset(randint(0, user_count - 1)).first()
        p = Post(body=forgery_py.lorem_ipsum.sentences(randint(1, 3)),
            timestamp=forgery_py.date.date(True),
            author=u)
        db.session.add(p)
        db.session.commit()