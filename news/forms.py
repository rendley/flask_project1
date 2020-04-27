from flask_wtf import FlaskForm
from wtforms import HiddenField, SubmitField, StringField
from wtforms.validators import DataRequired , ValidationError
from app.news.models import News


class CommentForm(FlaskForm): 
    news_id = HiddenField("ID news", validators=[DataRequired()])               
    comment_text = StringField("Текст комментария", validators=[DataRequired()], render_kw={"class": "form-control"})
    submit = SubmitField("Отправить", render_kw={"class": "btn btn-outline-info"})
    
    # security
    def validate_news_id(self, news_id):
        if not News.query.get(news_id.data): 
            raise ValidationError("Вы пытаетесь прокоментировать несуществующую новость!")