from flask_wtf import FlaskForm
from wtforms import HiddenField, SubmitField, StringField
from wtforms.validators import DataRequired 


class CommentForm(FlaskForm): 
    news_id = HiddenField("ID news", validators=[DataRequired()])               
    comment_text = StringField("Текст комментария", validators=[DataRequired()], render_kw={"class": "form-control"})
    submit = SubmitField("Отправить", render_kw={"class": "btn btn-outline-info"})
    
