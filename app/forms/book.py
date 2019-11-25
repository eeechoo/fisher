from wtforms import Form, StringField, IntegerField
from wtforms.validators import NumberRange, Length


class SearchForm(Form):
    q = StringField(validators=[Length(min=1, max=30)])
    page = IntegerField(validators=[NumberRange(min=1, max=99)], default=1)
