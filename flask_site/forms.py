from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import Form, StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_site.models import User


class RegistrationForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=3, max=20)]
    )
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        """
      FUNCTION: Ensures username is unique
      username: field name that would be validated
      user: from flaskblog.models; queries if username is already in the database (if no user, returns none)
      If "user" is none, username is unique and won't trigger the error. Otherwise, will raise a validation error
      """
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Username is taken. Please choose another one.")

    def validate_email(self, email):
        """
      FUNCTION: Ensures email is unique
      username: field name that would be validated
      user: from flaskblog.models; queries if email address is already in the database (if no user, returns none)
      If "user" is none, user email is unique and won't trigger the error. Otherwise, will raise a validation error
      """
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("That email is taken. Please choose another one.")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember me")
    submit = SubmitField("Login")


class UpdateAccountForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=3, max=20)]
    )
    email = StringField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Update")

    def validate_username(self, username):
        """
      FUNCTION: Updates username if entered update is different from current
      username.data: username selected that is different from entered in the form 
      current_user.username: the current username of the user, as seen from the db
      If "user" is none, user email is unique and won't trigger the error. Otherwise, will raise a validation error
      """
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError("Username is taken. Please choose another one.")

    def validate_email(self, email):
        """
      FUNCTION: Updates email if entered update is different from current
      email.data: email selected that is different from entered in the form 
      current_user.email: the current email of the user, as seen from the db If "user" is none, user email is unique and won't trigger the error. Otherwise, will raise a validation error
      """
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError("That email is taken. Please choose another one.")
