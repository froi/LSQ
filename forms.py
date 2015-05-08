from flask_wtf import Form
from wtforms import TextField, PasswordField, TextAreaField, SelectField, HiddenField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class LoginForm(Form):
    username = TextField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])


class RegisterForm(Form):
    username = TextField(
        'username',
        validators=[DataRequired(), Length(min=3, max=25)]
    )
    email = TextField(
        'email',
        validators=[DataRequired(), Email(message=None), Length(min=6, max=40)]
    )
    password = PasswordField(
        'password',
        validators=[DataRequired(), Length(min=6, max=25)]
    )
    confirm = PasswordField(
        'Repeat password',
        validators=[
            DataRequired(), EqualTo('password', message='Passwords must match.')
        ]
    )


class SnippetForm(Form):
    snippet_id = HiddenField('snippet_id')
    title = TextField('Title', validators=[DataRequired()])
    code = TextAreaField('Code', validators=[DataRequired()])
    desc = TextAreaField('Description')
    snippet_type = SelectField(
        'Type', 
        choices=[
            ('apache', 'Apache'),
            ('bash', 'Bash'),
            ('c#', 'C#'),
            ('c++', 'C++'),
            ('cSS', 'CSS'),
            ('coffeeScript', 'CoffeeScript'),
            ('diff', 'Diff'),
            ('dockerfile', 'Dockerfile'),
            ('go', 'Go'),
            ('gradle', 'Gradle'),
            ('html', 'HTML, XML'),
            ('hTTP', 'HTTP'),
            ('ini', 'Ini'),
            ('jSON', 'JSON'),
            ('java', 'Java'),
            ('javaScript', 'JavaScript'),
            ('lua', 'Lua'),
            ('makefile', 'Makefile'),
            ('markdown', 'Markdown'),
            ('nginx', 'Nginx'),
            ('objective C', 'Objective C'),
            ('pHP', 'PHP'),
            ('perl', 'Perl'),
            ('python', 'Python'),
            ('ruby', 'Ruby'),
            ('sql', 'SQL'),
            ('stylus', 'Stylus'),
            ('swift', 'Swift'),
        ],
        validators=[DataRequired()])
    tags = TextField('Tags')
