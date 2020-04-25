from app.db import db
from datetime import datetime
from sqlalchemy.orm import relationship

class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False) 
    url = db.Column(db.String, nullable=False, unique=True)
    published = db.Column(db.DateTime, nullable=False)
    text = db.Column(db.Text, nullable=True)
 
    def comments_count(self):
        return Comment.query.filter(Comment.news_id == self.id).count()


    def __repr__(self):
        return f"<News {self.title}, {self.url}>"

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=True)
    published = db.Column(db.DateTime, nullable=False, default=datetime.now())

    # after relationship will need to make migration db
    # export (set) FLASK_APP = app && flask db migrate && flask db upgrade
    news_id = db.Column(db.Integer, db.ForeignKey("news.id", ondelete="CASCADE"), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), index=True)

    
    news = relationship("News", backref="comments") 
    user = relationship("User", backref="comments")

    def __repr__(self): 
        return f"<Comment {self.id}>"


