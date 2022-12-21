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
    povendor = SelectField(u'-- Select a Vendor --', choices=[], validators=[InputRequired()])  #choices are left empty if intended to be filled with database information
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
    povendornotes = SelectField('Standard Notes', choices=[])
    poaccountcode = SelectField(u'Acc. Code', choices=[('105','Construction Equipment'), ('110','Fuel'), ('115','Repairs & Maintenance'), ('120','Dyed (Off-Road) Diesel Fuel'), ('125','Gasoline/Diesel Fuel'), ('130','Form Rental'), ('135','Scaffolding Rental'), ('140','Office/Storage Rental'), ('145','Portable Toilets'), ('150','Cleaning Supplies'), ('155','Office Supplies'), ('160','Water/Ice'), ('165','Shipping Fee'), ('170','Consumables'), ('175','Gases'), ('180','Welding Rod'), ('185','Welding Consumables'), ('190','Safety Supplies'), ('195','Paint/Blast Consumables'), ('200','Maintenance-Improvements'), ('205','Uniform/Tools'), ('305','Utilities'), ('310','Waste/Dumpster'), ('315','Service Contacts'), ('320','Cell Phone'), ('325','Telephone'), ('330','Office Furniture'), ('335','Computer Purchases'), ('340','Computer Software-Accessories'), ('345','IT-Computer Services'), ('350','Postage'), ('355','Entertainment & Meals'), ('360','Travel'), ('361','Travel Meal'), ('365','Licenses & Fees'), ('367','Insurance & Bonds'), ('370','Building Rent'), ('375','Property Taxes'), ('380','Small Tools'), ('381','Equipment'), ('505','Drilling'), ('506','Screw Piles'), ('507','Concrete Testing'), ('510','NDE (X-Ray)'), ('511','Inspection Services'), ('515','Pump Truck'), ('520','Building Contractor'), ('521','Engineering Services'), ('522','Instrumentation & Electrical'), ('523','Fabrication Services'), ('524','Slug Catcher Fab-Install'), ('525','Survey'), ('530','Dozer-Dirt Work'), ('532','Civil Construction Services'), ('535','Freight/Shipping'), ('540','Grout'), ('545','Nitrogen Testing'), ('550','Torquing'), ('555','Rig Welder'), ('560','Rig Welder - Equipment Rental'), ('565','Rig Welder - Per Diem'), ('570','Crane Services'), ('575','Stress Relief'), ('576','Galvanizing Services'), ('580','Maintenance Services'), ('585','Environmental Analytical Testing'), ('586','Facility Permits'), ('587','Hazardous Waste Transportaion - Disposal'), ('588','EHS Training'), ('589','Professional Services'), ('590','Contract Labor'), ('605','Concrete'), ('610','Form Material'), ('615','Rebar'), ('620','Anchor Bolts-Embeds'), ('625','Backfill'), ('630','Pipe'), ('635','Pipe Fittings'), ('640','Gaskets'), ('645','Stud Bolts'), ('650','Pipe Coating'), ('655','Hand-Manual Valves'), ('660','Structural'), ('665','Structural Bolts'), ('670','Grout'), ('675','Insulation'), ('680','Metal'), ('685','Insul. Accessories'), ('690','Paint & Coating'), ('695','Blasting Material'), ('700','Electrical'), ('705','Conduit - Fittings'), ('710','Tubing & Tube Fittings'), ('715','Analyzers'), ('716','Control Panels-DCS-PLC'), ('717','Control Valves - Regulators'), ('718','Flow Instruments'), ('719','Level Instruments'), ('720','Pressure Instruments'), ('721','Temperature Instruments'), ('722','Relief Valves - Rupture Discs'), ('723','Shutdown - Switching - Solenoid Valves'), ('724','Strainers'), ('725','Vessels & Tanks'), ('726','Heat Exchanger'), ('727','Air Cooled Heat Exchanger'), ('728','Heater'), ('729','Flare'), ('730','Thermal Oxidizer'), ('731','Pumps (Including Seal Flush Systems)'), ('732','Blower'), ('733','Compressor'), ('734','Expander'), ('735','Filter'), ('736','Separator'), ('737','Packaged Equipment'), ('799','Warranty Items'), ('805','Accounting Fees'), ('810','Advertising'), ('815','Dental Insurance'), ('820','Health Insurance'), ('825','Legal Fees'), ('830','Note Payable'), ('835','Interest Expense'), ('840','Medical Expense'), ('845','Vehicle Purchase'), ('850','General Liablity'), ('851','General Liablity'), ('855','Workmans Comp'), ('856','Workmans Comp'), ('860','Bank Charges'), ('865','Contributions'), ('900','Corporate Office Depreciation'), ('905','Shop Depreciation'), ('910','Accumulated Depreciation'), ('915','Prepaid Insurance'), ('920','Accrued Insurance'), ('925','Employee Insurance Contribution'), ('930','Misc. Income'), ('935','Earnings Accrual'), ('940','Accrued Payroll'), ('945','Cost In Excess of Billing'), ('950','Revenue-POC'), ('955','Billings in Excess of Cost'), ('960','Prepaid Expense'), ('965','Buildings and Land'), ('970','Employee Advances')])

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
    vendoracccode = SelectField(u'Acc. Code', choices=[('Construction Equipment'), ('Fuel'), ('Repairs & Maintenance'), ('Dyed (Off-Road) Diesel Fuel'), ('Gasoline/Diesel Fuel'), ('Form Rental'), ('Scaffolding Rental'), ('Office/Storage Rental'), ('Portable Toilets'), ('Cleaning Supplies'), ('Office Supplies'), ('Water/Ice'), ('Shipping Fee'), ('Consumables'), ('Gases'), ('Welding Rod'), ('Welding Consumables'), ('Safety Supplies'), ('Paint/Blast Consumables'), ('Maintenance-Improvements'), ('Uniform/Tools'), ('Utilities'), ('Waste/Dumpster'), ('Service Contacts'), ('Cell Phone'), ('Telephone'), ('Office Furniture'), ('Computer Purchases'), ('Computer Software-Accessories'), ('IT-Computer Services'), ('Postage'), ('Entertainment & Meals'), ('Travel'), ('Travel Meal'), ('Licenses & Fees'), ('Insurance & Bonds'), ('Building Rent'), ('Property Taxes'), ('Small Tools'), ('Equipment'), ('Drilling'), ('Screw Piles'), ('Concrete Testing'), ('NDE (X-Ray)'), ('Inspection Services'), ('Pump Truck'), ('Building Contractor'), ('Engineering Services'), ('Instrumentation & Electrical'), ('Fabrication Services'), ('Slug Catcher Fab-Install'), ('Survey'), ('Dozer-Dirt Work'), ('Civil Construction Services'), ('Freight/Shipping'), ('Grout'), ('Nitrogen Testing'), ('Torquing'), ('Rig Welder'), ('Rig Welder - Equipment Rental'), ('Rig Welder - Per Diem'), ('Crane Services'), ('Stress Relief'), ('Galvanizing Services'), ('Maintenance Services'), ('Environmental Analytical Testing'), ('Facility Permits'), ('Hazardous Waste Transportaion - Disposal'), ('EHS Training'), ('Professional Services'), ('Contract Labor'), ('Concrete'), ('Form Material'), ('Rebar'), ('Anchor Bolts-Embeds'), ('Backfill'), ('Pipe'), ('Pipe Fittings'), ('Gaskets'), ('Stud Bolts'), ('Pipe Coating'), ('Hand-Manual Valves'), ('Structural'), ('Structural Bolts'), ('Grout'), ('Insulation'), ('Metal'), ('Insul. Accessories'), ('Paint & Coating'), ('Blasting Material'), ('Electrical'), ('Conduit - Fittings'), ('Tubing & Tube Fittings'), ('Analyzers'), ('Control Panels-DCS-PLC'), ('Control Valves - Regulators'), ('Flow Instruments'), ('Level Instruments'), ('Pressure Instruments'), ('Temperature Instruments'), ('Relief Valves - Rupture Discs'), ('Shutdown - Switching - Solenoid Valves'), ('Strainers'), ('Vessels & Tanks'), ('Heat Exchanger'), ('Air Cooled Heat Exchanger'), ('Heater'), ('Flare'), ('Thermal Oxidizer'), ('Pumps (Including Seal Flush Systems)'), ('Blower'), ('Compressor'), ('Expander'), ('Filter'), ('Separator'), ('Packaged Equipment'), ('Warranty Items'), ('Accounting Fees'), ('Advertising'), ('Dental Insurance'), ('Health Insurance'), ('Legal Fees'), ('Note Payable'), ('Interest Expense'), ('Medical Expense'), ('Vehicle Purchase'), ('General Liablity'), ('General Liablity'), ('Workmans Comp'), ('Workmans Comp'), ('Bank Charges'), ('Contributions'), ('Corporate Office Depreciation'), ('Shop Depreciation'), ('Accumulated Depreciation'), ('Prepaid Insurance'), ('Accrued Insurance'), ('Employee Insurance Contribution'), ('Misc. Income'), ('Earnings Accrual'), ('Accrued Payroll'), ('Cost In Excess of Billing'), ('Revenue-POC'), ('Billings in Excess of Cost'), ('Prepaid Expense'), ('Buildings and Land'), ('Employee Advances')])

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