from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class NameForm(FlaskForm):
    username = StringField("이름", validators=[DataRequired(), Length(min=2, max=10)])
    submit = SubmitField("제출")
class VisAnsForm(FlaskForm):
    answer = StringField("답변", validators=[DataRequired(), Length(min=0, max=100)])
    submit = SubmitField("제출")

class ScoreForm(FlaskForm):
    score_0=RadioField("0")
    score_5=RadioField("5")
    score_10=RadioField("10")
    score_15=RadioField("15")
    score_20=RadioField("20")
    score_25=RadioField("25")
    score_30=RadioField("30")
    score_35=RadioField("35")
    score_40=RadioField("40")
    score_45=RadioField("45")
    score_50=RadioField("50")
    score_55=RadioField("55")
    score_60=RadioField("60")
    score_65=RadioField("65")
    score_70=RadioField("70")
    score_75=RadioField("75")
    score_80=RadioField("80")
    score_85=RadioField("85")
    score_90=RadioField("90")
    score_95=RadioField("95")
    score_100=RadioField("100")
    submit = SubmitField()

