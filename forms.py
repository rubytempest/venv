#This file contains all the forms used in the program

from datetime import datetime
from tkinter.tix import Select
from tokenize import String
from flask import Flask
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField, PasswordField, DateField, SelectField, EmailField, IntegerField, FloatField
from wtforms.validators import InputRequired, DataRequired, Email
from random import random

 
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])        #nameofformfield = TypeofField('displayname', addvalidators)
    password = PasswordField('Password', validators=[InputRequired()])

class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    email = EmailField('Email', validators=[InputRequired(), Email()])    #email field with format validation
    phone = StringField('Phone', validators=[InputRequired()])
    company = SelectField('Company', choices=[('ISTI'),('SELECT'),('PREMIER PLANT SERVICES'),('PAYNE-HUBER')] ,validators=[InputRequired()])
    usertype = StringField('User Type', validators=[InputRequired()])

class POForm(FlaskForm):
    pojob = SelectField('Job #', validators=[InputRequired()], choices=[])
    ponumber = StringField('PO #', default=random() , validators=[DataRequired()])
    poacccode = SelectField("Account Code", choices=[('Construction Equipment'),('Fuel'),('Repairs & Maintenance'),('Dyed Diesel Fuel'),('1.41.97-LowIncome')])
    pocreated = DateField("Creation Date", default=datetime.today, validators=[DataRequired()])  #date field default today
    pobuyer = SelectField('Buyer', choices=[])
    povendor = SelectField('Vendor', choices=[], validators=[DataRequired()])  #choices are left empty if intended to be filled with database information
    pobillto = SelectField('Bill To', choices=[])
    poshipto = SelectField('Ship To', choices=[])
    popayment= SelectField('Payment Terms', choices=[('NET 15'),('NET 30'),('NET 60')], default='NET 30')
    potaxstatus = SelectField('Tax Status', choices=[('Taxable'),('Non Taxable')], default='Taxable')
    potaxrate = StringField('Tax Rate', validators=[InputRequired()])
    postatus = StringField('Tax Rate', validators=[InputRequired()])
    posubtotal = StringField('Subtotal', validators=[InputRequired()])
    poshipping = StringField('Shipping & Handling', validators=[InputRequired()])
    pototal = StringField('Total', validators=[InputRequired()])
    pocreatedby = StringField('Created By', validators=[InputRequired()])
    poskid = StringField('Skid #')
    pojobtype = SelectField("Job Type", choices=[('Field\\Fabrication Job'),('Corporate Office'),('Fabrication Shop'),('Insulation'),('Paint Shop'),('Texas Office')], validators=[DataRequired()])
    pojobtype2 = SelectField("Job Type", choices=[], validators=[DataRequired()])


class LocationsForm(FlaskForm):
    locationname = StringField('Name', validators=[InputRequired()])  
    locationaddress= StringField('Address', validators=[InputRequired()])
    locationcity= StringField('City', validators=[InputRequired()])
    locationstate = StringField('State', validators=[InputRequired()])
    locationzipcode= StringField('Zip Code', validators=[InputRequired()])
    locationcompany= StringField('Company', validators=[InputRequired()])
    locationjobnumber = SelectField("Job #", choices=[], validators=[DataRequired()])
    locationattachment = FileField(validators=[FileRequired()])


class JobsForm(FlaskForm):
    jobnumber = StringField('Job #', validators=[InputRequired()])

class BackordersForm(FlaskForm):
    ponumber = StringField('Vendor #', validators=[InputRequired()])
    bonotes = StringField('Vendor #', validators=[InputRequired()])
    bodate = DateField("Backorder Date", default=datetime.today, validators=[DataRequired()])

class RevisionsForm(FlaskForm):
    revisionpo = StringField('Vendor #', validators=[InputRequired()])
    revisionnumber = StringField('Vendor #', validators=[InputRequired()])
    revisionnotes = StringField('Vendor #', validators=[InputRequired()])
    revisiondate = DateField("Creation Date", default=datetime.today, validators=[DataRequired()])

class BuyersForm(FlaskForm):
    buyername = StringField('Name', validators=[InputRequired()])  
    buyeraddress1 = StringField('Address', validators=[InputRequired()])
    buyeraddress2= StringField('Address 2', validators=[InputRequired()])
    buyercity = StringField('City', validators=[InputRequired()])
    buyerstate= StringField('State', validators=[InputRequired()])
    buyerzipcode= StringField('Zip Code', validators=[InputRequired()])
    buyercontact= StringField('Contact', validators=[InputRequired()])
    buyerphone= StringField('Phone', validators=[InputRequired()])
    buyermemail= EmailField('Email', validators=[InputRequired()])

class VendorsForm(FlaskForm):
    vendorname = StringField('Name', validators=[InputRequired()])  
    vendornumber = StringField('Vendor#', validators=[InputRequired()]) 
    vendoraddress1 = StringField('Address', validators=[InputRequired()])
    vendoraddress2= StringField('Address 2', validators=[InputRequired()])
    vendorcity = StringField('City', validators=[InputRequired()])
    vendorstate = StringField('State', validators=[InputRequired()])
    vendorzipcode = StringField('Zip Code', validators=[InputRequired()])
    vendorcontact= StringField('Contact', validators=[InputRequired()])
    vendorphone = StringField('Phone', validators=[InputRequired()])
    vendoremail = EmailField('Email', validators=[InputRequired()])

class ItemsForm(FlaskForm):
    itemvendor = SelectField('Vendor', choices=[])
    itemunit= StringField('Unit', validators=[InputRequired()])
    itemdescription = StringField('Description', validators=[InputRequired()])
    itemprice= StringField('Price', validators=[InputRequired()])
    itemminoqt= IntegerField('Min. O Qt.', validators=[InputRequired()])
    itemcostcode= IntegerField('Cost Code', validators=[InputRequired()])
    itempart = StringField('Part #', validators=[InputRequired()])   
    itemfile = FileField(validators=[FileRequired()])

class BomForm(FlaskForm):
    bomfile = FileField(validators=[FileRequired()], render_kw={"placeholder": "Select Job#"})
    bomjobnumber = SelectField('Add to Job:', choices=[])

class POItemsForm(FlaskForm):
    poitempo = StringField('PO#', validators=[InputRequired()])  
    poitemdescription = SelectField('Item', choices=[])  
    poitemskid= StringField('Skid/Task', validators=[InputRequired()])
    poitemtag = StringField('Tag#', validators=[InputRequired()])
    poitemquantity= IntegerField('Quantity', validators=[InputRequired()], default=1)
    poitemtotalprice= FloatField('Total Price', validators=[InputRequired()])
    #Only in edit window
    poitempromiseddate= DateField("Promised Date")
    poitemcarrier= StringField('Carrier')
    poitemtracking = StringField('Tracking#')
    poitemnotes = StringField('Notes:')

class ReceivingForm(FlaskForm):
    receivingfile = FileField(validators=[FileRequired()])