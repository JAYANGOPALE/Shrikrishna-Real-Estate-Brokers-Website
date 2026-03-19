from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, DecimalField, SubmitField
from wtforms.validators import DataRequired, Optional, NumberRange, Length

class RequirementForm(FlaskForm):
    requirement_type = SelectField('Requirement Type', 
                                  choices=[('Buy', 'Buy'), ('Rent', 'Rent'), ('Lease', 'Lease')],
                                  validators=[DataRequired()])
    
    property_type = SelectField('Property Type',
                               choices=[('Flat', 'Flat'), ('House', 'House'), ('Land', 'Land'), ('Commercial', 'Commercial')],
                               validators=[DataRequired()])
    
    location = StringField('Location (City / Area)', 
                          validators=[DataRequired(), Length(min=2, max=100)])
    
    budget_min = DecimalField('Min Budget (₹)', 
                             validators=[DataRequired(), NumberRange(min=0)])
    
    budget_max = DecimalField('Max Budget (₹)', 
                             validators=[DataRequired(), NumberRange(min=0)])
    
    bhk = SelectField('BHK',
                     choices=[('1BHK', '1BHK'), ('2BHK', '2BHK'), ('3BHK', '3BHK'), ('4BHK', '4BHK+')],
                     validators=[Optional()])
    
    description = TextAreaField('Description (extra details)', 
                               validators=[Optional(), Length(max=500)])
    
    contact_preference = SelectField('Contact Preference',
                                    choices=[('Call', 'Call'), ('Email', 'Email'), ('Both', 'Both')],
                                    validators=[DataRequired()])
    
    submit = SubmitField('Submit Requirement')

    def validate(self, extra_validators=None):
        if not super().validate(extra_validators=extra_validators):
            return False
        if self.budget_max.data < self.budget_min.data:
            self.budget_max.errors.append('Max budget cannot be less than min budget.')
            return False
        return True
