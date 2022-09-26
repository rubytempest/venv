from flask import Flask, render_template, make_response, flash, request, redirect, url_for, send_file    #imports required to navigate through pages
from forms import LoginForm, RegistrationForm, POForm, LocationsForm, VendorsForm, ItemsForm, POItemsForm, BomForm, ReceivingForm                                #imports for WTForms
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash       #imports for password security
from flask_login import LoginManager, UserMixin                                 #imports required for user login
from flask_login import login_user, logout_user, current_user, login_required   #imports required for user login
import win32com.client                                                          #imports required to send emails
from datetime import date
import pandas as pd                                                             #imports required to manipulate excel files
import xlrd
import pdfkit
from pdfkit.api import configuration
from werkzeug.utils import secure_filename                                              
import pythoncom
import math
import csv                                                                      #import required to create csv files
import os                                                                       #import required to save files into server
from fractions import Fraction
import datetime 
from PyPDF2 import PdfMerger


UPLOAD_FOLDER = '/temp'
ALLOWED_EXTENSIONS = { 'xlsx', 'xls', 'csv', 'pdf'}


#Create the Flask object
app = Flask(__name__)



#Config to save uploads folder
app.config['UPLOAD FOLDER'] = UPLOAD_FOLDER

#Secret key to work with forms
app.config['SECRET_KEY'] = 'hardsecretkey'


#SQLAlchemy database connection with mysql
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/pomaindatabase'    #mysql://username:'password'@location/databasename
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
 
db = SQLAlchemy(app)

#Login code start
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'Login'

#CREATING DATABASE MODELS

class UserInfo(UserMixin, db.Model):                    #USERS MODEL
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(100), unique = True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))
    company = db.Column(db.String(100))
    phone = db.Column(db.String(50))
    email = db.Column(db.String(50))
    usertype = db.Column(db.String(100)) 
 
    def __init__(self, username, password, name, company, phone, email, usertype):
        self.username = username
        self.password = password
        self.name = name
        self.company = company
        self.phone = phone
        self.email = email
        self.usertype = usertype

class VendorsInfo(db.Model):                            #VENDORS MODELS
    id = db.Column(db.Integer, primary_key = True)
    vendorname = db.Column(db.String(100), unique = True)
    vendornumber = db.Column(db.String(100), unique = True)
    vendoraddress1 = db.Column(db.String(100))
    vendoraddress2 = db.Column(db.String(100))
    vendorcity = db.Column(db.String(100))
    vendorstate = db.Column(db.String(100))
    vendorzipcode = db.Column(db.String(100))
    vendorcontact = db.Column(db.String(100))
    vendorphone = db.Column(db.String(100))
    vendormemail = db.Column(db.String(100))
    vendortaxrate = db.Column(db.Float)
 
    def __init__(self, vendorname, vendornumber, vendoraddress1, vendoraddress2, vendorcity, vendorsate, vendorzipcode, vendorcontact, vendorphone, vendormemail, vendortaxrate):
        self.vendorname = vendorname
        self.vendornumber = vendornumber
        self.vendoraddress1 = vendoraddress1
        self.vendoraddress2 = vendoraddress2
        self.vendorcity = vendorcity
        self.vendorstate = vendorsate
        self.vendorzipcode = vendorzipcode
        self.vendorcontact = vendorcontact
        self.vendorphone = vendorphone
        self.vendormemail = vendormemail
        self.vendortaxrate = vendortaxrate

class LocationInfo(db.Model):           #LOCATION MODEL
    id = db.Column(db.Integer, primary_key = True)
    locationname = db.Column(db.String(100), unique = True)
    locationaddress = db.Column(db.String(100))
    locationcity = db.Column(db.String(100))
    locationstate = db.Column(db.String(100))
    locationzipcode = db.Column(db.String(20))
    locationcompany = db.Column(db.String(100))
    locationtaxrate = db.Column(db.Float)
    locationclient = db.Column(db.String(100))
    locationjobnumber = db.Column(db.String(100))

    def __init__(self, locationname, locationaddress, locationcity, locationstate, locationzipcode, locationcompany, locationtaxrate, locationclient, locationjobnumber):
        self.locationname = locationname
        self.locationaddress = locationaddress
        self.locationcity = locationcity
        self.locationstate = locationstate
        self.locationzipcode = locationzipcode
        self.locationcompany = locationcompany
        self.locationtaxrate = locationtaxrate
        self.locationclient = locationclient
        self.locationjobnumber = locationjobnumber

class ItemsInfo(db.Model):           #ITEMS MODEL
    id = db.Column(db.Integer, primary_key = True)
    itemvendor = db.Column(db.String(100))
    itemunit = db.Column(db.String(100))
    itemdescription = db.Column(db.String(300))
    itemprice = db.Column(db.String(20))
    itemminoqt = db.Column(db.String(100))
    itemcostcode = db.Column(db.String(100))
    itempart = db.Column(db.String(50))
    itemdatasheet = db.Column(db.Text)

    def __init__(self, itemvendor, itemunit, itemdescription, itemprice, itemminoqt, itemcostcode, itempart, itemdatasheet):
        self.itemvendor = itemvendor
        self.itemunit = itemunit
        self.itemdescription = itemdescription
        self.itemprice = itemprice
        self.itemminoqt = itemminoqt
        self.itemcostcode = itemcostcode
        self.itempart = itempart
        self.itemdatasheet = itemdatasheet

class RevisionsInfo(db.Model):           #POREVISIONS MODEL
    id = db.Column(db.Integer, primary_key = True)
    revisionspo = db.Column(db.String(100))
    revisionnumber = db.Column(db.String(100))
    revisionnotes = db.Column(db.String(300))
    revisiondate = db.Column (db.Date)

    def __init__(self, porevisionorigin, porevisionnumber, porevisionnotes, revisiondate):
        self.porevisionorigin = porevisionorigin
        self.poreporevisionnumber = porevisionnumber
        self.porevisionnotes = porevisionnotes
        self.revisiondate = revisiondate

class BackordersInfo(db.Model):           
    id = db.Column(db.Integer, primary_key = True)
    backorderpo = db.Column(db.String(100))
    backordernotes = db.Column(db.String(300))
    backorderdate = db.Column(db.Date)

    def __init__(self, backorderpo, backordernotes, backorderdate):
        self.backorderpo = backorderpo
        self.backordernotes = backordernotes
        self.backorderdate = backorderdate

class POItemsInfo(db.Model):          
    id = db.Column(db.Integer, primary_key = True)
    poitempo = db.Column(db.String(100))
    poitemdescription = db.Column(db.Text())
    poitemskid = db.Column(db.String(100))
    poitemtag = db.Column(db.String(100))
    poitemquantity = db.Column(db.Integer)
    poitemtotalprice = db.Column(db.Float)
    poitempromisseddate = db.Column(db.Date)
    poitemcarrier = db.Column(db.String(100))
    poitemtracking = db.Column(db.String(100))
    poitemnotes = db.Column(db.String(300))
    poitemvendor = db.Column(db.String(100))
    poitemprice = db.Column(db.Float)
    poitemdate = db.Column(db.Date)
    poitemunit = db.Column(db.String(100))
    poitemjobtype = db.Column(db.String(100))
    poitemcostcode = db.Column(db.String(10))
    poitemjobtypenumber = db.Column(db.String(10))
    poreceivedqty = db.Column(db.Integer)


    def __init__(self, poitempo, poitemdescription, poitemskid, poitemtag, poitemquantity, poitemtotalprice, poitempromisseddate, 
                poitemcarrier, poitemtracking, poitemnotes, poitemvendor, poitemprice, poitemdate, poitemunit, poitemjobtype, 
                poitemcostcode, poitemjobtypenumber, poreceivedqty):
        self.poitempo = poitempo
        self.poitemdescription = poitemdescription
        self.poitemskid = poitemskid
        self.poitemtag = poitemtag
        self.poitemquantity = poitemquantity
        self.poitemtotalprice = poitemtotalprice
        self.poitempromisseddate = poitempromisseddate
        self.poitemcarrier = poitemcarrier
        self.poitemtracking = poitemtracking
        self.poitemnotes = poitemnotes
        self.poitemvendor = poitemvendor
        self.poitemprice = poitemprice
        self.poitemdate = poitemdate
        self.poitemunit = poitemunit
        self.poitemjobtype = poitemjobtype
        self.poitemcostcode = poitemcostcode
        self.poitemjobtypenumber = poitemjobtypenumber
        self.poreceivedqty = poreceivedqty

class POInfo(db.Model):           
    id = db.Column(db.Integer, primary_key = True)
    ponumber = db.Column(db.String(100))
    pojob = db.Column(db.String(300))
    poacccode = db.Column(db.String(100))
    postatus= db.Column(db.String(100))
    pocreated = db.Column(db.Date)
    pobuyer = db.Column(db.String(100))
    povendor = db.Column(db.String(100))
    pobillto = db.Column(db.String(100))
    poshipto = db.Column(db.Text())
    popayment = db.Column(db.String(100))
    poshipping = db.Column(db.Float)
    potaxstatus = db.Column(db.String(50))
    potaxrate = db.Column(db.Float)
    posubtotal = db.Column(db.Float)
    pototal = db.Column(db.Float)
    pocreatedby = db.Column(db.String(100))
    poskid = db.Column(db.String(100))
    pojobtype = db.Column(db.String(100))
    pojobtypenum = db.Column(db.String(10))
    porejectednotes = db.Column(db.Text())


    def __init__(self, ponumber, pojob, postatus, poacccode, pocreated, pobuyer, povendor, pobillto, poshipto, popayment, poshipping, potaxstatus, potaxrate, posubtotal, pototal, pocreatedby, poskid, pojobtype, pojobtypenum, porejectednotes):
        self.ponumber = ponumber
        self.pojob = pojob
        self.poacccode = poacccode
        self.postatus = postatus
        self.pocreated = pocreated
        self.pobuyer = pobuyer
        self.povendor = povendor
        self.pobillto = pobillto
        self.poshipto = poshipto
        self.popayment = popayment
        self.poshipping = poshipping
        self.potaxstatus = potaxstatus
        self.potaxrate = potaxrate
        self.posubtotal = posubtotal
        self.poshipping = poshipping
        self.pototal = pototal
        self.pocreatedby = pocreatedby
        self.poskid = poskid
        self.pojobtype = pojobtype
        self.pojobtypenum = pojobtypenum
        self.porejectednotes = porejectednotes

class PurchasersInfo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    purchasername = db.Column(db.String(100), unique = True)
    purchaserjob = db.Column(db.String(20))
    purchasercompany = db.Column(db.String(100))
    purchaserphone = db.Column(db.String(50))
    purchaseremail = db.Column(db.String(100))
    purchaseremail2 = db.Column(db.String(100))
    purchaserposition = db.Column(db.String(100))

    def __init__(self, purchasername, purchaserjob, purchasercompany, purchaserphone, purchaseremail, purchaseremail2, purchaserposition):
        self.purchasername = purchasername
        self.purchaserjob = purchaserjob
        self.purchasercompany = purchasercompany
        self.purchaserphone = purchaserphone
        self.purchaseremail = purchaseremail
        self.purchaseremail2 = purchaseremail2
        self.purchaserposition = purchaserposition

class JobsInfo(db.Model):           
    id = db.Column(db.Integer, primary_key = True)
    jobnumber = db.Column(db.String(100))
    jobnotes = db.Column(db.Text())

    def __init__(self, jobnumber, jobnotes):
        self.jobnumber = jobnumber
        self.jobnotes = jobnotes

class BomInfo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    bomlinenumber = db.Column(db.String(50))
    bomsize = db.Column(db.String(50))
    bomquantity = db.Column(db.String(100))
    bomdescription = db.Column(db.String(300))
    bomtag = db.Column(db.String(50))
    bomunit = db.Column(db.String(50))
    bomfilename = db.Column(db.String(100))
    bomdatecreated = db.Column(db.Date)
    bomjobnumber = db.Column(db.String(50))
    bomstatus = db.Column(db.String(50))
    bomcostcode = db.Column(db.String(10))
    bomsearchterm = db.Column(db.String(50))

    def __init__(self, bomlinenumber, bomsize, bomquantity, bomdescription, bomtag, bomunit, bomfilename, bomdatecreated, bomjobnumber, bomstatus, bomcostcode, bomsearchterm):
        self.bomlinenumber = bomlinenumber
        self.bomsize = bomsize
        self.bomquantity = bomquantity
        self.bomdescription = bomdescription
        self.bomtag = bomtag
        self.bomunit = bomunit
        self.bomfilename = bomfilename
        self.bomdatecreated = bomdatecreated
        self.bomjobnumber = bomjobnumber
        self.bomstatus = bomstatus
        self.bomsearchterm = bomsearchterm
        self.bomcostcode = bomcostcode

class SecondaryLocationInfo(db.Model):           #LOCATION MODEL
    id = db.Column(db.Integer, primary_key = True)
    secondlocationname = db.Column(db.String(100), unique = True)
    secondlocationaddress = db.Column(db.String(100))
    secondlocationcity = db.Column(db.String(100))
    secondlocationstate = db.Column(db.String(100))
    secondlocationzipcode = db.Column(db.String(20))
    secondlocationtaxrate = db.Column(db.Float)
    secondlocationjobnumber = db.Column(db.String(100))
    secondlocationbelongs = db.Column(db.String(50))

    def __init__(self, secondlocationname, secondlocationaddress, secondlocationcity, secondlocationstate, secondlocationzipcode, secondlocationtaxrate, secondlocationjobnumber, secondlocationbelongs):
        self.secondlocationname = secondlocationname
        self.secondlocationaddress = secondlocationaddress
        self.secondlocationcity = secondlocationcity
        self.secondlocationstate = secondlocationstate
        self.secondlocationzipcode = secondlocationzipcode
        self.secondlocationtaxrate = secondlocationtaxrate
        self.secondlocationjobnumber = secondlocationjobnumber
        self.secondlocationbelongs = secondlocationbelongs

### LOGIN MANAGEMENT CODE ###
@login_manager.user_loader
def load_user(user_id):
    return UserInfo.query.get(int(user_id))    

#___START ROUTING INSIDE APP___#

### ROUTES FOR LOGIN USERS ###
@app.route('/', methods=["POST", "GET"])
@login_required                                                 #request user for login to access this route
def index():
    name = current_user.username
    return redirect(url_for('poitemscp'))                   #HOMEPAGE

## START RECEIVING ROUTES ##
#VIEW RECEIVING TABLE
@app.route("/receiving", methods=["POST", "GET"])
@login_required
def receiving():

    all_data = POInfo.query.order_by(POInfo.id.desc()).all()                        #List of PO retrieved and organize = newest first

    return render_template("receiving.html", pos = all_data)

#VIEW RECITEMSV2.HTML
@app.route("/recitemsv2/<ponumber>", methods=["POST", "GET"])
@login_required
def recitemsv2(ponumber):
    form = ReceivingForm()
    ponumber = ponumber                                       
    descending = POInfo.query.filter(POInfo.ponumber == ponumber)
    po = descending.first()

    vendor = VendorsInfo.query.filter_by(vendorname=po.povendor).first()
    shipto = LocationInfo.query.filter_by(locationname=po.poshipto).first()
    buyer = current_user

    poitems = POItemsInfo.query.order_by(POItemsInfo.id.desc()).all()
    all_data = ItemsInfo.query.filter_by(itemvendor=po.povendor).order_by(ItemsInfo.itemdescription.asc())

    return render_template("recitemsv2.html", items = all_data, poitems=poitems, po=po, vendor=vendor, shipto=shipto, buyer=buyer, form=form)

#UPDATE ALL RECITEMSV2
@app.route("/insertallrecitemsv2", methods=["POST", "GET"])
def insertallrecitemsv2():
    if request.method == 'POST':

        ponumber=request.form['ponumber']
        print(ponumber)
        my_data = POItemsInfo.query.filter_by(poitempo=ponumber)
        for each in my_data:
            each.poreceivedqty = each.poitemquantity
        db.session.commit()
        flash("Purchase Order Updated Successfully")
 
        return redirect(url_for('recitemsv2', ponumber=ponumber))

#INSERTSINGLERECITEMS V2
@app.route("/insertsinglerecitemsv2", methods=["POST", "GET"])
def insertsinglerecitemsv2():
    if request.method == 'POST':

        ponumber=request.form['ponumber']
        my_data = POItemsInfo.query.get(request.form.get('id')) 
        my_data.poreceivedqty = request.form['poreceivedqty']

        db.session.commit()
 
        return redirect(url_for('recitemsv2', ponumber=ponumber))

#MARK ITEMS AS RECEIVED
@app.route("/markreceived", methods=["POST", "GET"])
def markreceived():
    if request.method == 'POST':

        form = ReceivingForm()
        po = POInfo.query.get(request.form.get('id')) 
        my_data = POItemsInfo.query.filter_by(poitempo=po.ponumber)
        po.postatus = request.form['postatus']
        for each in my_data:
            print(each.poreceivedqty)
            print(each.poitemquantity)
            if each.poreceivedqty != each.poitemquantity:
                po.postatus = "Backorder"
                break
        
        db.session.commit()

        filename=secure_filename(form.receivingfile.data.filename)
        form.receivingfile.data.save('scans/received/' + filename)
        flash("Purchase Order Updated Successfully")
    return redirect(url_for('receiving'))

### PURCHASE ORDER ROUTES ###

#VIEW POLIST TABLE
@app.route("/polist", methods=["POST", "GET"])
@login_required
def polist():
    form= POForm()                                             #We declare here the form we'll use

    form.povendor.choices = [(povendor.vendorname) for povendor in VendorsInfo.query.all()]  #query to populate vendors box
    form.pobillto.choices = [(pobillto.locationname) for pobillto in LocationInfo.query.all()]   #form.field.choices = [(field.infofromtable) for field in DatabaseTable.query.all()]
    form.poshipto.choices = [(poshipto.locationname) for poshipto in LocationInfo.query.all()]
    form.pojob.choices = [(pojob.locationjobnumber) for pojob in LocationInfo.query.all()]

    all_data = POInfo.query.order_by(POInfo.id.desc()).all()                        #List of PO retrieved and organize = newest first
    buyer = current_user

    return render_template("polist.html", pos = all_data, form=form, buyer=buyer)

#DELETE PO TABLE
@app.route('/deletepo/<id>/', methods = ['GET', 'POST'])
def deletepo(id):
    my_data = POInfo.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Purchasing Order Deleted Successfully")
 
    return redirect(url_for('polist'))

#COPY PO RECORD
@app.route('/copypo', methods=['POST'])
def copypo():

    my_data = POInfo.query.get(request.form('id'))
    poitems = POItemsInfo.query.filter_by(poitempo=my_data.ponumber)

    ponumber = request.form['ponumber']
    pojob = request.form['pojob']
    postatus = "In Progress"
    poacccode = request.form['poacccode']
    pocreated = date.today()
    pobuyer = current_user.name
    povendor = my_data.povendor
    pobillto = my_data.pobillto
    poshipto = request.form['poshipto']
    popayment = request.form['popayment']
    poshipping = my_data.poshipping
    potaxstatus = request.form['potaxstatus']
    potaxrate = my_data.potaxrate
    posubtotal = my_data.posubtotal
    pototal = my_data.pototal
    pocreatedby = my_data.pocreatedby
    poskid = " "
    pojobtype = my_data.pojobtype
    pojobtypenum = my_data.pojobtypenum
    porejectednotes = " "

    for each in poitems:
        newpoitempo = ponumber
        newpoitemdate = date.today()
        copy_poitem = POItemsInfo( newpoitempo, each.poitemdescription, each.poitemskid, each.poitemtag, each.poitemquantity, each.poitemtotalprice, each.poitempromisseddate, each.poitemcarrier, each.poitemtracking, each.poitemnotes, each.poitemvendor, each.poitemprice, newpoitemdate, each.poitemunit, each.poitemjobtype, each.poitemcostcode, each.poitemjobtypenumber)
        db.session.add(copy_poitem)
        db.session.commit()


    new_data = POInfo(ponumber, pojob, postatus, poacccode, pocreated, pobuyer, povendor, pobillto, poshipto, popayment, poshipping, potaxstatus, potaxrate, posubtotal, pototal, pocreatedby, poskid, pojobtype, pojobtypenum, porejectednotes)
    db.session.add(new_data)
    db.session.commit()


    return redirect(url_for('poitemsv2', ponumber=ponumber))

#CREATE PO RECORD
@app.route('/insertpo', methods = ['POST'])
def insertpo():
    if request.method == 'POST':
        pojob = request.form['pojob']

        #Autofill PONUMBER
        lastpo = POInfo.query.filter_by(pojob=pojob).first()
        if lastpo == None:
            ponumber = pojob + '-001'
        else:
            format = lastpo.ponumber.replace("-","")
            nextpo = int(format) + 1
            nextpo = str(nextpo)
            ponumber = pojob + '-' + nextpo[4:]

        poskid = request.form['poskid']
        pocreated = request.form['pocreated']
        pobuyer = request.form['pobuyer']
        povendor = request.form['povendor']
        pojobtype = request.form['pojobtype']

        poacccode = request.form['poacccode']
        pobillto = "MATRIX LOCATION ADDRESS"
        poshipto = request.form['poshipto']
        popayment = request.form['popayment']
        potaxstatus = "Taxable"
        postatus = "In Progress"
        porejectednotes = ""

        if pojobtype == "Corporate Office":
            pojobtypenum = "10"
        elif pojobtype == "Fabrication Shop":
            pojobtypenum = "90"
        elif pojobtype == "Field\\Fabrication Job":
            pojobtypenum = "30"
        elif pojobtype == "Insulation":
            pojobtypenum = "50"
        elif pojobtype == "Paint Shop":
            pojobtypenum = "60"
        elif pojobtype == "Texas Office":
            pojobtypenum = "20"

        poshipping = 0

        posubtotal = 0
        pototal = 0
        pocreatedby = current_user.name

        #TAX RATE CALCULATION ROUTINE
        vendor = VendorsInfo.query.filter_by(vendorname=povendor).first()
        receiving = LocationInfo.query.filter_by(locationname=poshipto).first()
        if vendor.vendorstate == 'OK' and receiving.locationstate == 'TX':
            potaxrate = vendor.vendortaxrate
        elif vendor.vendorstate != 'OK' and receiving.locationstate == 'OK':
            potaxrate = receiving.locationtaxrate
        else: 
            potaxrate = receiving.locationtaxrate
        if receiving.locationtaxrate == 0:
            potaxrate = 0

        my_data = POInfo(ponumber, pojob, postatus, poacccode, pocreated, pobuyer, povendor, pobillto, poshipto, popayment, poshipping, potaxstatus, potaxrate, posubtotal, pototal, pocreatedby, poskid, pojobtype, pojobtypenum, porejectednotes)
        db.session.add(my_data)
        db.session.commit()
         
        inputtype = request.form['inputtype']
        if inputtype == "manual":
            return redirect(url_for('poitemsmanual', ponumber=ponumber))

        return redirect(url_for('poitemsv2', ponumber=ponumber))


#UPDATE PO RECORD
@app.route('/updatepo', methods = ['GET', 'POST'])
def updatepo():
    if request.method == 'GET':
        my_data = POInfo.query.get(request.form.get('id'))

    if request.method == 'POST':
        my_data = POInfo.query.get(request.form.get('id'))

        my_data.poacccode = request.form['poacccode']
        my_data.poshipto = request.form['poshipto']
        my_data.popayment = request.form['popayment']
        my_data.poskid = request.form['poskid']
        db.session.commit()
        flash("Purchase Order Updated Successfully")
 
        return redirect(url_for('poitemsv2', ponumber=my_data.ponumber))

#UPDATE POSTATUS RECORD
@app.route('/updatepostatus', methods = ['GET', 'POST'])
def updatepostatus():
 
    if request.method == 'POST':
        my_data = POInfo.query.get(request.form.get('id'))  
        my_data.postatus = request.form['postatus']
        if my_data.postatus == "Rejected":
            my_data.porejectednotes = request.form['rejectednotes']
        db.session.commit()
        if my_data.postatus == "Approved":              #only generate PO pdf if status changes to approved
            pdf(my_data.ponumber)
            print("PDF HAS BEEN CREATED")
            pdfnoprice(my_data.ponumber)
            print("receiving pdf copy created")


    return redirect(url_for('polist'))

### ROUTES FOR LOCATIONS ###

#VIEW LOCATIONS TABLE
@app.route("/locations", methods=["POST", "GET"])
@login_required
def locations():
    form= LocationsForm()                                                     #We declare here the form we'll use
    all_data = LocationInfo.query.all()
    states = [ 'AK', 'AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL', 'GA',
           'HI', 'IA', 'ID', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA', 'MD', 'ME',
           'MI', 'MN', 'MO', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH', 'NJ', 'NM',
           'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX',
           'UT', 'VA', 'VT', 'WA', 'WI', 'WV', 'WY']

    return render_template("locations.html", locations = all_data, form=form, states=states)

#DELETE LOCATION RECORD
@app.route('/deletelocation/<id>/', methods = ['GET', 'POST'])
def deletelocation(id):
    my_data = LocationInfo.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Location Deleted Successfully")
 
    return redirect(url_for('locations'))

#CREATE NEW LOCATION RECORD
@app.route('/insertlocation', methods = ['POST'])
def insertlocation():
    if request.method == 'POST':
 
        locationname = request.form['locationname']
        locationcompany = request.form['locationcompany']
        locationaddress = request.form['locationaddress']
        locationcity = request.form['locationcity']
        locationstate = request.form['locationstate']
        locationzipcode = request.form['locationzipcode']
        locationtaxrate = request.form['locationtaxrate']
        locationclient = request.form['locationclient']
        locationjobnumber = request.form['locationjobnumber']
 
        my_data = LocationInfo(locationname, locationaddress, locationcity, locationstate, locationzipcode, locationcompany, locationtaxrate, locationclient, locationjobnumber)
        db.session.add(my_data)
        db.session.commit()
 
        flash("Location Inserted Successfully")
 
        return redirect(url_for('locations'))

#UPDATE LOCATION RECORD
@app.route('/updatelocation', methods = ['GET', 'POST'])
def updatelocation():
 
    if request.method == 'POST':
        my_data = LocationInfo.query.get(request.form.get('id'))         #get information every entry by id from database
 
        my_data.locationname = request.form['locationname']              #request especific column from table in database
        my_data.locationcompany = request.form['locationcompany']
        my_data.locationaddress = request.form['locationaddress']
        my_data.locationcity = request.form['locationcity']
        my_data.locationstate = request.form['locationstate']
        my_data. locationzipcode = request.form['locationzipcode']
        my_data.locationtaxrate = request.form['locationtaxrate']
        my_data.locationclient = request.form['locationclient']
        my_data.locationjobnumber = request.form['locationjobnumber']
 
        db.session.commit()
        flash("Location Updated Successfully")
 
        return redirect(url_for('locations'))

##### MANUAL INPUT FOR POITEMS #####
####################################

#### VIEW POITEMSMANUAL TABLE ####
@app.route("/poitemsmanual/<ponumber>", methods=["POST", "GET"])
def poitemsmanual(ponumber):
    form= POItemsForm()                                                 #declaring what we'll use in the route
    formpo = POForm()

    ponumber = ponumber                                       
    descending = POInfo.query.filter(POInfo.ponumber == ponumber)
    po = descending.first()

    vendor = VendorsInfo.query.filter_by(vendorname=po.povendor).first()
    shipto = LocationInfo.query.filter_by(locationname=po.poshipto).first()
    buyer = current_user

    poitems = POItemsInfo.query.order_by(POItemsInfo.id.desc()).all()
    all_data = ItemsInfo.query.filter_by(itemvendor=po.povendor).order_by(ItemsInfo.itemdescription.asc())

    formpo.povendor.choices = [(povendor.vendorname) for povendor in VendorsInfo.query.all()]  #query to populate vendors box
    formpo.pobillto.choices = [(pobillto.locationname) for pobillto in LocationInfo.query.all()]   #form.field.choices = [(field.infofromtable) for field in DatabaseTable.query.all()]
    formpo.poshipto.choices = [(poshipto.locationname) for poshipto in LocationInfo.query.all()] 

    form.poitemdescription.choices = [(poitemdescription.itemdescription) for poitemdescription in ItemsInfo.query.order_by(ItemsInfo.itemdescription.name).all()]

    return render_template("poitemsmanual.html", items = all_data, poitems=poitems, form=form, po=po, vendor=vendor, shipto=shipto, buyer=buyer, formpo=formpo)

#CREATE POITEMSMANUAL.HTML
@app.route('/insertpoitemsmanual', methods = ['POST'])
def insertpoitemsmanual():
    if request.method == 'POST':
        poitemprice = request.form['itemprice']

        poitemdescription = request.form['poitemdescription']
        poitemquantity = request.form['poitemquantity']
        poitempo = request.form['ponumber']
        poitemtotalprice = int(poitemquantity) * float(poitemprice)
        poitemskid = request.form['poitemskid']
        poitemtag = request.form['itempart']
        poitempromisseddate = None
        poitemtracking = None
        poitemnotes = None
        poitemcarrier = None
        poitemvendor = request.form['itemvendor']
        poitemdate = request.form['pocreated']
        poitemjobtype = request.form['pojobtype']
        poitemjobtypenumber = request.form['pojobtypenum']
        if "GASKET" in poitemdescription:
            poitemcostcode = "640"
        elif "NIPPLE" in poitemdescription or "A105" in poitemdescription or "A234" in poitemdescription or "A312" in poitemdescription or "A182" in poitemdescription:
            poitemcostcode = "635"
        elif "VALVE" in poitemdescription:
            poitemcostcode = "655"
        elif "A36" in poitemdescription:
            poitemcostcode = "660"
        elif "A106" in poitemdescription:
            poitemcostcode = "630"
        elif "C105" in poitemdescription:
            poitemcostcode = "685"
        elif "STUD BOLT" in poitemdescription:
            poitemcostcode = "645"
        else:
            poitemcostcode = "NA"
        poreceivedqty = None

        if "A106" in poitemdescription:
            poitemunit = "ft."
        else:
            poitemunit = "ea."

        my_data = POItemsInfo( poitempo, poitemdescription, poitemskid, poitemtag, poitemquantity, poitemtotalprice, poitempromisseddate, poitemcarrier, poitemtracking, poitemnotes, poitemvendor, poitemprice, poitemdate, poitemunit, poitemjobtype, poitemcostcode, poitemjobtypenumber, poreceivedqty)
        db.session.add(my_data)
        db.session.commit()

        pdf(my_data.poitempo)
        print("PDF HAS BEEN CREATED")
        pdfnoprice(my_data.poitempo)
        print("receiving pdf copy created")
 
        return redirect(url_for('poitemscpp', ponumber=poitempo))
        #return redirect(url_for('poitemsmanual', ponumber=poitempo)) disabled manual mode redirect


#IMPORT-EXCEL POITEMSCPP MANUAL
@app.route('/importpoitemscpp', methods = ['GET','POST'])
def importpoitemscpp():
    
    poitempo = request.form['ponumber']
    formexcel = ItemsForm()

    filename=secure_filename(formexcel.itemfile.data.filename)
    print(filename)
    formexcel.itemfile.data.save('temp/' + filename)


    df = pd.read_excel('temp/' + filename, 0)

    index=18
    for i in range(200):
        print(df.iloc[index][11])
        if pd.isna(df.iloc[index][1]):
            break

        poitemprice = df.iloc[index][11]
        poitemdescription = df.iloc[index][3]
        poitemquantity = df.iloc[index][2]
        poitempo = poitempo
        poitemtotalprice = df.iloc[index][12]
        poitemskid = None
        poitemtag = ""
        poitempromisseddate = None

        poitemtracking = None
        poitemnotes = None
        poitemcarrier = None
        poitemvendor = request.form['povendor']
        poitemdate = request.form['pocreated']
        poitemjobtype = request.form['pojobtype']
        poitemjobtypenumber = request.form['pojobtypenum']
        poitemunit = "ea."
        if "GASKET" in poitemdescription:
            poitemcostcode = "640"
        elif "VALVE" in poitemdescription:
            poitemcostcode = "655"
        elif "NIPPLE" in poitemdescription or "A105" in poitemdescription or "A420" in poitemdescription or "A234" in poitemdescription or "A182" in poitemdescription or "TEE" in poitemdescription or "ELL" in poitemdescription or "A312" in poitemdescription or "PLUG" in poitemdescription:
            poitemcostcode = "635"
            poitemunit = "ea."
        elif "A36" in poitemdescription or "A992" in poitemdescription:  #COST CODE FOR STEEL
            poitemcostcode = "660"
        elif "PIPE" in poitemdescription:   #COST CODE FOR PIPE
            poitemcostcode = "630"
            poitemunit = "ft."
        elif "C105" in poitemdescription:
            poitemcostcode = "685"
        elif "STUD BOLT" in poitemdescription:
            poitemcostcode = "645"
        else:
            poitemcostcode = "635"
        poreceivedqty = None


        my_data = POItemsInfo( poitempo, poitemdescription, poitemskid, poitemtag, poitemquantity, poitemtotalprice, poitempromisseddate, poitemcarrier, poitemtracking, poitemnotes, poitemvendor, poitemprice, poitemdate, poitemunit, poitemjobtype, poitemcostcode, poitemjobtypenumber, poreceivedqty)
        db.session.add(my_data)
        db.session.commit()
        index += 1
    
    pdf(my_data.poitempo)
    print("PDF HAS BEEN CREATED")
    pdfnoprice(my_data.poitempo)
    print("receiving pdf copy created")

    return redirect(url_for('poitemscpp', ponumber=poitempo))

#DELETE POITEMS V2MANUAL
@app.route('/deletepoitemsmanual/<id>/', methods = ['GET', 'POST'])
def deletepoitemsmanual(id):
    my_data = POItemsInfo.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
 
    return redirect(url_for('poitemsmanual', ponumber=my_data.poitempo))


########################################################################################
##############################POITEMSCP ROUTES##########################################
########################################################################################

### VIEW POITEMSCP.HTML ###
@app.route("/poitemscp", methods=["POST", "GET"])
@login_required
def poitemscp():
    if request.method == 'GET':
        formpo = POForm()
        form=BomForm()
        form.bomjobnumber.choices = ["----"]+[(bomjobnumber.locationjobnumber) for bomjobnumber in LocationInfo.query.all()]
        today = date.today()
        required=today + datetime.timedelta(days=7)
        hide = 1
        vendor = VendorsInfo.query.filter_by(vendorname="Airgas USA  LLC").first()
        shipto = LocationInfo.query.filter_by(locationname="Battle Horse").first()
        buyer = current_user

        #Autofill PONUMBER
        lastpo = POInfo.query.order_by(POInfo.id.desc()).first()
        format = lastpo.ponumber.replace("-","")
        nextpo = int(format) + 1
        nextpo = str(nextpo)
        nextpo = nextpo[:4] + '-' + nextpo[4:]

        print(nextpo)

        formpo.povendor.choices = ['---']+[(povendor.vendorname) for povendor in VendorsInfo.query.all()]  #query to populate vendors box
        formpo.poshipto.choices = [(poshipto.locationname) for poshipto in LocationInfo.query.all()] 

        return render_template("poitemscp.html", hide=hide, form=form, formpo=formpo, nextpo=nextpo, vendor=vendor, shipto=shipto, buyer=buyer, today=today)

    if request.method == 'POST':
        jobnumber = request.form['bomjobnumber']

        hide = 0
        formpo = POForm()
        form=BomForm()
        form.bomjobnumber.choices = [(bomjobnumber.locationjobnumber) for bomjobnumber in LocationInfo.query.all()]
        vendor = request.form['povendor']
        print(vendor)

        today=date.today()
        required=today + datetime.timedelta(days=7)

        poitems = POItemsInfo.query.filter(POItemsInfo.poitempo == "90865092834750982").all()
        secondshipto = request.form['poshipto']

        print(jobnumber, secondshipto)

        shipto = LocationInfo.query.filter_by(locationjobnumber=jobnumber).first()

        if secondshipto != '-':
            shipto = LocationInfo.query.filter_by(locationjobnumber=secondshipto).first()
        
        buyer = current_user

        ponumber = request.form['ponumber']
        if ponumber == "000":
            #Autofill PONUMBER
            lastpo = POInfo.query.filter(POInfo.pojob == jobnumber).order_by(POInfo.ponumber.desc()).first()
            if lastpo == None:
                nextpo = jobnumber + '-001'
            else:
                format = lastpo.ponumber.replace("-","")
                nextpo = int(format) + 1
                print(format)
                print(nextpo)
                nextpo = str(nextpo)
                nextpo = jobnumber + '-' + nextpo[4:]
        else:
            nextpo= ponumber

        formpo.povendor.choices = ['---']+[(povendor.vendorname) for povendor in VendorsInfo.query.all()]  #query to populate vendors box
        formpo.poshipto.choices = [jobnumber]+[(poshipto.locationjobnumber) for poshipto in LocationInfo.query.all()] 


        return render_template("poitemscp.html",required=required,hide=hide, vendor=vendor, form=form, formpo=formpo, poitems=poitems, nextpo=nextpo, shipto=shipto, buyer=buyer, today=today, pojob=jobnumber)


#UNUSED ROUTE -- POITEMSCPP(LEGACY) - MANUAL COPY PASTE SINGLE LINE
@app.route("/poitemscpposave", methods=["POST", "GET"])
def poitemscpposave():
    if request.method == 'POST':
        ponumber = request.form['ponumber']

        exists = db.session.query(db.exists().where(POInfo.ponumber == ponumber)).scalar()    #QUERE TO CHECK IF PONUM. ALREADY EXISTS IN DATABASE
        if exists:
            return 'Selected PO# already exists in database'
        else:

            pojob = request.form['pojob']
            poskid = None
            pocreated = date.today()
            pobuyer = current_user.name
            povendor = request.form['povendor']
            pojobtype = None

            poacccode = None
            pobillto = "Premier Plant Services LLC"
            poshipto = request.form['poshipto']
            popayment = "NET 30"
            potaxstatus = "Taxable"
            postatus = "Approved"
            porejectednotes = ""

            pojobtype = "Field\\Fabrication Job"

            poshipping = 0

            posubtotal = 0
            pototal = 0
            pocreatedby = current_user.name

            if pojobtype == "Corporate Office":
                pojobtypenum = "10"
            elif pojobtype == "Fabrication Shop":
                pojobtypenum = "90"
            elif pojobtype == "Field\\Fabrication Job":
                pojobtypenum = "30"
            elif pojobtype == "Insulation":
                pojobtypenum = "50"
            elif pojobtype == "Paint Shop":
                pojobtypenum = "60"
            elif pojobtype == "Texas Office":
                pojobtypenum = "20"
            

            print(poshipto)
            #Calculate tax rate
            vendor = VendorsInfo.query.filter_by(vendorname=povendor).first()
            receiving = LocationInfo.query.filter_by(locationname=poshipto).first()

            if vendor.vendorstate == 'OK' and receiving.locationstate == 'TX':
                potaxrate = vendor.vendortaxrate
            elif vendor.vendorstate != 'OK' and receiving.locationstate == 'OK':
                potaxrate = receiving.locationtaxrate
            else: 
                potaxrate = receiving.locationtaxrate
            if receiving.locationtaxrate == 0:
                potaxrate = 0

            my_data = POInfo(ponumber, pojob, postatus, poacccode, pocreated, pobuyer, povendor, pobillto, poshipto, popayment, poshipping, potaxstatus, potaxrate, posubtotal, pototal, pocreatedby, poskid, pojobtype, pojobtypenum, porejectednotes)
            db.session.add(my_data)
            db.session.commit()
    
            
            return redirect(url_for('poitemscpp', ponumber=ponumber))

#DELETE POITEMSCPP
@app.route('/deletepoitemcpp/<id>/', methods = ['GET', 'POST'])
def deletepoitemcpp(id):
    my_data = POItemsInfo.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
 
    return redirect(url_for('poitemscpp', ponumber=my_data.poitempo))

####POITEMS REDIRECT
@app.route('/poitemsredirect', methods=["POST", "GET"])
@login_required
def poitemsredirect():
    ponumber = request.form['poredirect']
    exists = db.session.query(db.exists().where(POInfo.ponumber == ponumber)).scalar()    #Query to check if exists in database

    if exists:
        return redirect(url_for('poitemscpp', ponumber=ponumber))
    else:
        return 'The Selected PO does not exist'

####POITEMSCPP.HTML SCREEEN
@app.route('/poitemscpp/<ponumber>', methods=["POST", "GET"])
@login_required

def poitemscpp(ponumber):

    ponumber = ponumber                                       
    descending = POInfo.query.filter(POInfo.ponumber == ponumber)
    po = descending.first()

    formpo = POForm()
    form=BomForm()
    formexcel = ItemsForm()

    form.bomjobnumber.choices = [(bomjobnumber.locationjobnumber) for bomjobnumber in LocationInfo.query.all()]
    today=date.today()

    poitems = POItemsInfo.query.filter(POItemsInfo.poitempo == po.ponumber).all()
    
    subtotal = 0
    for each in poitems:
        subtotal = subtotal + each.poitemtotalprice
    subtotal = round(subtotal,2)    

    vendor = VendorsInfo.query.filter_by(vendorname=po.povendor).first()
    shipto = LocationInfo.query.filter_by(locationname=po.poshipto).first()
    buyer = current_user

    formpo.povendor.choices = [(povendor.vendorname) for povendor in VendorsInfo.query.all()]  #query to populate vendors box

    return render_template("poitemscpp.html", formexcel=formexcel, subtotal=subtotal, form=form, formpo=formpo, poitems=poitems, vendor=vendor, shipto=shipto, buyer=buyer, today=today, po=po)

### ADD POITEMSCPP ITEM SINGLE ###

@app.route("/poitemscpinsert", methods=["POST", "GET"])
def poitemscpinsert():
    excelpaste = request.form['excelpaste']
    excelpaste = excelpaste.split("\t")
    excelpaste = list(filter(None, excelpaste))
    print(excelpaste)   #QUANTITY - ITEMDESCRIPTION - PARTNUMBER - COST - UAM - TOTAL

    poitemquantity = excelpaste[0]
    poitemdescription = excelpaste[1]
    poitemtag = excelpaste[2]
    excelpaste[3] = excelpaste[3].replace('$','')
    excelpaste[3] = excelpaste[3].replace(',','')
    poitemprice = float(excelpaste[3])
    poitemunit = excelpaste[4]
    excelpaste[5] = excelpaste[5].replace('$','')
    excelpaste[5] = excelpaste[5].replace(',','')
    poitemtotalprice = float(excelpaste[5])         #NO LONGER CALCULATED
    poitempo = request.form['nextpo']
    poitemskid = None                       #REMOVED
    poitempromisseddate = None
    poitemtracking = None
    poitemnotes = None
    poitemcarrier = None
    poitemvendor = request.form['vendor']
    poitemdate = date.today()
    poitemjobtype = None                    #REMOVED
    poitemjobtypenumber = None              #REMOVED
    poitemcostcode = None                   #REMOVED
    poreceivedqty = None

    my_data = POItemsInfo( poitempo, poitemdescription, poitemskid, poitemtag, poitemquantity, poitemtotalprice, poitempromisseddate, poitemcarrier, poitemtracking, poitemnotes, poitemvendor, poitemprice, poitemdate, poitemunit, poitemjobtype, poitemcostcode, poitemjobtypenumber, poreceivedqty)
    db.session.add(my_data)
    db.session.commit()

    mypo = POInfo.query.get(request.form.get('id'))  

    pdf(mypo.ponumber)
    print("PDF HAS BEEN CREATED")
    pdfnoprice(mypo.ponumber)
    print("receiving pdf copy created")

    return redirect(url_for('poitemscpp', ponumber=poitempo))


###POITEMSCPINSERTCELL INITIALIZATION UPDATING QUANTITY FIELD
@app.route("/poitemscpinsertcell", methods=["POST", "GET"])
def poitemscpinsertcell():

    poitemquantity = request.form['poitemquantity']
    poitemdescription = " "
    poitemtag = ""
    poitemprice = 0
    poitemunit = " "
    poitemtotalprice = 0         #NO LONGER CALCULATED
    poitempo = request.form['nextpo']
    poitemskid = None                       #REMOVED
    poitempromisseddate = None
    poitemtracking = None
    poitemnotes = None
    poitemcarrier = None
    poitemvendor = request.form['vendor']
    poitemdate = date.today()
    poitemjobtype = None                    #REMOVED
    poitemjobtypenumber = None              #REMOVED
    poitemcostcode = None                   #REMOVED
    poreceivedqty = 0

    my_data = POItemsInfo( poitempo, poitemdescription, poitemskid, poitemtag, poitemquantity, poitemtotalprice, poitempromisseddate, poitemcarrier, poitemtracking, poitemnotes, poitemvendor, poitemprice, poitemdate, poitemunit, poitemjobtype, poitemcostcode, poitemjobtypenumber, poreceivedqty)
    db.session.add(my_data)
    db.session.commit()

    mypo = POInfo.query.get(request.form.get('id'))  

    pdf(mypo.ponumber)
    print("PDF HAS BEEN CREATED")
    pdfnoprice(mypo.ponumber)
    print("receiving pdf copy created")

    return redirect(url_for('poitemscpp', ponumber=poitempo))

#UPDATE POITEMEDITCELL
@app.route('/poitemeditcell', methods = ['GET', 'POST'])
def poitemeditcell():
    if request.method == 'POST':
        my_data = POItemsInfo.query.get(request.form.get('id'))

        poitempo=my_data.poitempo

        my_data.poitemquantity = request.form['poitemquantity']
        quantity = my_data.poitemquantity
        my_data.poitemdescription = request.form['poitemdescription']
        my_data.poitemprice = request.form['poitemprice']
        price = my_data.poitemprice
        my_data.poitemunit = request.form['poitemunit']
        my_data.poitemtotalprice = request.form['poitemtotalprice']
        my_data.poitemcostcode = request.form['poitemcostcode']
        my_data.poitemtag = request.form['poitemtag']
        total = int(quantity) * float(price)
        
        my_data.poitemtotalprice = total    
        db.session.commit()
        
        pdf(poitempo)
        print("PDF HAS BEEN CREATED")
        pdfnoprice(poitempo)
        print("receiving pdf copy created")
 
    return redirect(url_for('poitemscpp', ponumber=poitempo))


#### VIEW POITEMSV2 TABLE ####
@app.route("/poitemsv2/<ponumber>", methods=["POST", "GET"])
def poitemsv2(ponumber):
    form= POItemsForm()                                                 #declaring what we'll use in the route
    formpo = POForm()
    
    ponumber = ponumber                                       
    descending = POInfo.query.filter(POInfo.ponumber == ponumber)
    po = descending.first()
    vendor = VendorsInfo.query.filter_by(vendorname=po.povendor).first()
    shipto = LocationInfo.query.filter_by(locationname=po.poshipto).first()
    buyer = current_user

    poitems = POItemsInfo.query.order_by(POItemsInfo.id.desc()).all()
    all_data = ItemsInfo.query.filter_by(itemvendor=po.povendor).order_by(ItemsInfo.itemdescription.asc())

    formpo.povendor.choices = [(povendor.vendorname) for povendor in VendorsInfo.query.all()]  #query to populate vendors box
    formpo.pobillto.choices = [(pobillto.locationname) for pobillto in LocationInfo.query.all()]   #form.field.choices = [(field.infofromtable) for field in DatabaseTable.query.all()]
    formpo.poshipto.choices = [(poshipto.locationname) for poshipto in LocationInfo.query.all()] 

    form.poitemdescription.choices = [(poitemdescription.itemdescription) for poitemdescription in ItemsInfo.query.order_by(ItemsInfo.itemdescription.name).all()]

    return render_template("poitemsv2.html", items = all_data, poitems=poitems, form=form, po=po, vendor=vendor, shipto=shipto, buyer=buyer, formpo=formpo)

#CREATE POITEMSV2.HTML
@app.route('/insertpoitemv2', methods = ['POST'])
def insertpoitemv2():
    if request.method == 'POST':
        poitemprice = request.form['itemprice']

        poitemdescription = request.form['poitemdescription']
        poitemquantity = request.form['poitemquantity']
        poitempo = request.form['ponumber']
        poitemtotalprice = int(poitemquantity) * float(poitemprice)
        poitemskid = request.form['poitemskid']
        poitemtag = request.form['itempart']
        poitempromisseddate = None
        poitemunit = request.form['itemunit']
        poitemtracking = None
        poitemnotes = None
        poitemcarrier = None
        poitemvendor = request.form['itemvendor']
        poitemdate = request.form['pocreated']
        poitemjobtype = request.form['pojobtype']
        poitemjobtypenumber = request.form['pojobtypenum']
        poitemcostcode = request.form['itemcostcode']
        poreceivedqty = None

        my_data = POItemsInfo( poitempo, poitemdescription, poitemskid, poitemtag, poitemquantity, poitemtotalprice, poitempromisseddate, poitemcarrier, poitemtracking, poitemnotes, poitemvendor, poitemprice, poitemdate, poitemunit, poitemjobtype, poitemcostcode, poitemjobtypenumber, poreceivedqty)
        db.session.add(my_data)
        db.session.commit()
 
        flash("Item Added PO Successfully")

        return redirect(url_for('poitemsv2', ponumber=poitempo))

#DELETEPOITEMV2
@app.route('/deletepoitemv2/<id>/', methods = ['GET', 'POST'])
def deletepoitemv2(id):
    my_data = POItemsInfo.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Item Removed from PO Successfully")
 
    return redirect(url_for('poitemsv2', ponumber=my_data.poitempo))


### ROUTES FOR VENDORS.HTML ###

#VIEW VENDORS TABLE
@app.route("/vendors", methods=["POST", "GET"])
@login_required
def vendors():
    form= VendorsForm()                                                     #We declare here the form we'll use
    all_data = VendorsInfo.query.order_by(VendorsInfo.id).all()
    states = [ 'AK', 'AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL', 'GA',
        'HI', 'IA', 'ID', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA', 'MD', 'ME',
        'MI', 'MN', 'MO', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH', 'NJ', 'NM',
        'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX',
        'UT', 'VA', 'VT', 'WA', 'WI', 'WV', 'WY']

    return render_template("vendors.html", vendors = all_data, form=form, states=states)

#DELETE VENDOR TABLE
@app.route('/deletevendor/<id>/', methods = ['GET', 'POST'])
def deletevendor(id):
    my_data = VendorsInfo.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
 
    return redirect(url_for('vendors'))

#CREATE VENDOR RECORD
@app.route('/insertvendor', methods = ['POST'])
def insertvendor():
    if request.method == 'POST':
 
        vendorname = request.form['vendorname']
        vendornumber = request.form['vendornumber']
        vendoraddress1 = request.form['vendoraddress1']
        vendoraddress2 = request.form['vendoraddress2']
        vendorcity = request.form['vendorcity']
        vendorstate = request.form['vendorstate']
        vendorzipcode = request.form['vendorzipcode']
        vendorcontact = request.form['vendorcontact']
        vendorphone = request.form['vendorphone']
        vendormemail = request.form['vendormemail']
        vendortaxrate = request.form['vendortaxrate']
 
        my_data = VendorsInfo(vendorname, vendornumber, vendoraddress1, vendoraddress2, vendorcity, vendorstate, vendorzipcode, vendorcontact, vendorphone, vendormemail, vendortaxrate)
        db.session.add(my_data)
        db.session.commit()
 
 
        return redirect(url_for('vendors'))

#UPDATE VENDOR RECORD
@app.route('/updatevendor', methods = ['GET', 'POST'])
def updatevendor():
 
    if request.method == 'POST':
        my_data = VendorsInfo.query.get(request.form.get('id'))
 
        my_data.vendorname = request.form['vendorname']
        my_data.vendornumber = request.form['vendornumber']
        my_data.vendoraddress1 = request.form['vendoraddress1']
        my_data.vendoraddress2 = request.form['vendoraddress2']
        my_data.vendorcity = request.form['vendorcity']
        my_data.vendorstate = request.form['vendorstate']
        my_data.vendorzipcode = request.form['vendorzipcode']
        my_data.vendorcontact = request.form['vendorcontact']
        my_data.vendorphone = request.form['vendorphone']
        my_data.vendormemail = request.form['vendormemail']
        my_data.vendortaxrate = request.form['vendortaxrate']
 
        db.session.commit()
 
        return redirect(url_for('vendors'))

### ROUTES FOR ITEMS ###

#VIEW ITEMS TABLE
@app.route("/items", methods=["POST", "GET"])
@app.route("/items/<description>", methods=["POST", "GET"])
@login_required
def items(description=0):

    form= ItemsForm()                                                                               #We declare here the form we'll use
    all_data = ItemsInfo.query.order_by(ItemsInfo.id.desc()).all()                                  #Load database in reverse ID order (newest first)
    form.itemvendor.choices = [(itemvendor.vendorname) for itemvendor in VendorsInfo.query.order_by(VendorsInfo.vendorname.asc()).all()]   #Query to fill itemvendor combobox

    return render_template("items.html", items = all_data, form=form)

#DELETE ITEM TABLE
@app.route('/deleteitem/<id>/', methods = ['GET', 'POST'])
def deleteitem(id):
    my_data = ItemsInfo.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
 
    return redirect(url_for('items'))

#CREATE ITEM RECORD
@app.route('/insertitem', methods = ['POST'])
def insertitem():
    if request.method == 'POST':
 
        itemvendor = request.form['itemvendor']
        itemunit = request.form['itemunit']
        itemdescription = request.form['itemdescription']
        itemprice = request.form['itemprice']
        itemminoqt = request.form['itemminoqt']
        itemcostcode = request.form['itemcostcode']
        itempart = request.form['itempart']
        itemdatasheet = ""
 
        my_data = ItemsInfo(itemvendor, itemunit, itemdescription, itemprice, itemminoqt,itemcostcode, itempart, itemdatasheet)
        db.session.add(my_data)
        db.session.commit()
 
        flash("Item Inserted Successfully")
 
        return redirect(url_for('items'))

#UPDATE ITEM RECORD
@app.route('/updateitem', methods = ['GET', 'POST'])
def updateitem():
 
    if request.method == 'POST':
        my_data = ItemsInfo.query.get(request.form.get('id'))
        
        my_data.itemunit = request.form['itemunit']
        my_data.itemdescription = request.form['itemdescription']
        my_data.itemprice = request.form['itemprice']
        my_data.itemminoqt = request.form['itemminoqt']
        my_data.itemcostcode = request.form['itemcostcode']
        my_data.itempart = request.form['itempart']
        my_data.itemdatasheet = request.form['itemdatasheet']
 
        db.session.commit()
        flash("Item Updated Successfully")
 
        return redirect(url_for('items'))

### UPLOAD EXCEL FILE TO ITEMS LIST ###

@app.route('/listupload', methods = ['GET', 'POST'])
def listupload():
    if request.method == 'POST':
        form=ItemsForm()

        form.itemvendor.choices = [(itemvendor.vendorname) for itemvendor in VendorsInfo.query.all()]   #Query to fill itemvendor combobox

        filename=secure_filename(form.itemfile.data.filename)
        form.itemfile.data.save('temp/' + filename)

        print(filename)
        data = pd.read_excel('temp/' + filename)      #read excel file
        dict = data.to_dict()               #Convert excel data to dictionary

        itemvendor = request.form['itemvendor']
        index = 0                               #Index used to navigate dictionary
                                        #SELFNOTE add error alert for wrong file format uploaded
        for i in dict["Cost Code"]:       #SELFNOTE find alternative              #Dictionary iteration using limit of values in first key
            itemcostcode = dict["Cost Code"][index]             #Assign values to variables
            itempart = dict["Part #"][index]
            itempart = str(itempart)
            if pd.isna(itempart):
                itempart = "-"
            itempart = itempart.replace(u'\xa0', u'')
            itemdescription = dict["Product Description"][index]
            itemdescription = itemdescription.replace(u'\xa0', u'')
            itemunit = dict["Unit"][index]
            if math.isnan (dict["Min. OQ"][index]):
                itemminoqt = 1
            else:
                itemminoqt = dict["Min. OQ"][index]
            if math.isnan (dict["Cost"][index]):
                itemprice = 0
            else:
                itemprice = dict["Cost"][index]
            itemdatasheet = ""

            my_data = ItemsInfo(itemvendor, itemunit, itemdescription, itemprice, itemminoqt, itemcostcode, itempart, itemdatasheet)
            print(my_data)
            db.session.add(my_data)
            db.session.commit()

            index += 1
    flash(str(index) + " Items Added Successfully")
        
    return redirect(url_for('items'))

### BOM FILE READ AND DISPLAY ###
@app.route('/bom/<pojob>', methods = ['GET', 'POST'])
@app.route('/bom', methods = ['GET', 'POST'])
@login_required

def bom(pojob=""):

    form=BomForm()
    form.bomjobnumber.choices = ["----"]+[(bomjobnumber.locationjobnumber) for bomjobnumber in LocationInfo.query.all()]
    all_data = BomInfo.query.filter_by(bomjobnumber=pojob).all()
    #all_data = BomInfo.query.order_by(BomInfo.bomdescription.desc()).all()                                  #Load database in reverse ID order (newest first)

    return render_template("bom.html", form=form, bom=all_data, pojob=pojob)

@app.route('/bomredirect', methods = ['GET','POST'])
def bomredirect():
    bomjobnumber=request.form['bomjobnumber']
    return redirect(url_for('bom', pojob=bomjobnumber))

#Route to upload BOM xlsx file
@app.route('/bomread', methods = ['GET' , 'POST'])
def bomread():
    if request.method == 'POST':
        form=BomForm()
        
        filename=secure_filename(form.bomfile.data.filename)
        form.bomfile.data.save('temp/' + filename)
        data = pd.read_excel('temp/' + filename)      
        bom = data.to_dict()              

        index = 0

        for i in bom["Line Number"]:
            if math.isnan (bom["Line Number"][index]):
                bomlinenumber = ""
            else:
                bomlinenumber = bom["Line Number"][index]
            
            if math.isnan (bom["Size"][index]):
                bomsize = ""
            else:
                bomsize = bom["Size"][index]

            bomquantity = bom["Quantity"][index]
            bomquantity = math.ceil(bomquantity) 

            bomdescription = bom["Long Description"][index]

            if math.isnan (bom["Tag"][index]):
                bomtag = ""
            else:
                bomtag = bom["Tag"][index]

            if math.isnan (bom["Uom"][index]):
                bomunit = ""
            else:
                bomunit = bom["Uom"][index]

            bomfilename = form.bomfile.data.filename
            bomdatecreated = date.today()
            bomjobnumber = request.form['bomjobnumber']
            bomstatus = "UPL"
            bomcostcode = "635"

            if "GASKET" in bomdescription:       #BOM BUTTON 1
                bomsearchterm = "GASKET"
            elif "VALVE" in bomdescription:        #BOM BUTTON 3
                bomsearchterm = "VALVE"
            elif "BOLT" in bomdescription:         #BOM BUTTON 2
                bomsearchterm = "BOLT"
            elif "ELBOW" in bomdescription:           
                bomsearchterm = "FITTING"        #BOM BUTTON 4 PIPE&FITTINGS
            elif "REDUCER" in bomdescription:
                bomsearchterm = "FITTING"
            elif "TEE" in bomdescription:
                bomsearchterm = "FITTING"
            elif "Deg" in bomdescription:
                bomsearchterm = "FITTING"
            elif "OLET" in bomdescription:
                bomsearchterm = "FITTING"
            elif "CAP" in bomdescription:
                bomsearchterm = "FITTING"
            elif "PLUG" in bomdescription:
                bomsearchterm = "FITTING"
            elif "SWAGE" in bomdescription:
                bomsearchterm = "FITTING"
            elif "NIPPLE" in bomdescription:
                bomsearchterm = "FITTING"
            elif "FLANGE" in bomdescription:
                bomsearchterm = "FITTING"
            elif "BLEED" in bomdescription:
                bomsearchterm = "FITTING"
            elif "ORIFICE" in bomdescription:
                bomsearchterm = "FITTING"
            elif "PIPE" in bomdescription:
                bomsearchterm = "FITTING"
                bomcostcode = "630"
            else:
                bomsearchterm = "STEEL"
            #MISSING OUTLETS CATEGORY

            index = index + 1
            
            my_data = BomInfo(bomlinenumber, bomsize, bomquantity, bomdescription, bomtag, bomunit, bomfilename, bomdatecreated, bomjobnumber, bomstatus, bomcostcode, bomsearchterm)

            db.session.add(my_data)
            db.session.commit()

        flash(str(index) + " BOM Material Added Successfully")

        return redirect(url_for('bom', pojob=bomjobnumber))

#BOMREQUEST ROUTE
@app.route('/bomrequest', methods =['GET','POST'])
def bomrequest():
    material = request.form['material']
    bomjobnumber = request.form['bomjobnumber']
    print(bomjobnumber)

    #Filter the requested items
    bom = BomInfo.query.filter(BomInfo.bomsearchterm.contains(material),BomInfo.bomjobnumber.like(bomjobnumber),BomInfo.bomstatus.like("UPL")).order_by(BomInfo.bomdescription.desc())  #Filter if typed MAterial is in description

    #GROUP SIMILAR ITEMS TOGETHER
    unique = bom.group_by(BomInfo.bomdescription, BomInfo.bomsize).all()

    #CONVERT BOM ITEMS INTO PO ITEMS
    for each in unique:
        poitempo = str(each.bomjobnumber) + "0-0001"
        poitemdescription = each.bomdescription
        print(poitemdescription)
        poitemskid = None
        poitemtag = ""
        poitemquantity = each.bomquantity
        poitemtotalprice = 0
        poitempromisseddate = None
        poitemcarrier = None
        poitemtracking = None
        poitemtracking = None
        poitemnotes = None
        poitemvendor = None
        poitemprice = 0
        poitemdate = date.today()
        poitemunit = each.bomunit
        poitemjobtype = None
        poitemcostcode = each.bomcostcode
        poitemjobtypenumber = None
        poreceivedqty = 0 

        my_data = POItemsInfo( poitempo, poitemdescription, poitemskid, poitemtag, poitemquantity, poitemtotalprice, poitempromisseddate, poitemcarrier, poitemtracking, poitemnotes, poitemvendor, poitemprice, poitemdate, poitemunit, poitemjobtype, poitemcostcode, poitemjobtypenumber, poreceivedqty)
        db.session.add(my_data)
        db.session.commit()

    #CHANGE STATUS OF REQUESTED ITEMS IN JOB
    for each in bom:
        each.bomstatus = "RFQ"
        db.session.commit()

    #CREATE NEW PO TO STORE RFQ
    ponumber = poitempo
    pojob = bomjobnumber
    poacccode = None
    postatus = "REQUEST FOR QUOTE"
    pocreated = date.today()
    pobuyer = current_user.name
    povendor = None
    pobillto = None
    poshipto = None
    popayment = "NET 30"
    poshipping = None
    potaxstatus = None
    potaxrate = 0
    posubtotal = 0
    pototal = 0
    pocreatedby = current_user.name
    poskid = None
    pojobtype = None
    pojobtypenum = None
    porejectednotes = None

    my_podata = POInfo(ponumber, pojob, postatus, poacccode, pocreated, pobuyer, povendor, pobillto, poshipto, popayment, poshipping, potaxstatus, potaxrate, posubtotal, pototal, pocreatedby, poskid, pojobtype, pojobtypenum, porejectednotes)
    db.session.add(my_podata)
    db.session.commit()



    return redirect(url_for('bom', pojob=bomjobnumber))

#### BOMITEMSV2.HTML  ####
@app.route("/bomitemsv2/<ponumber>", methods=["POST", "GET"])
@login_required
def bomitemsv2(ponumber):
    form= POItemsForm()                                                 #declaring what we'll use in the route
    formpo = POForm()
    formexcel = ItemsForm()
    
    ponumber = ponumber                                       
    descending = POInfo.query.filter(POInfo.ponumber == ponumber)
    po = descending.first()
    vendor = VendorsInfo.query.filter_by(vendorname=po.povendor).first()
    shipto = LocationInfo.query.filter_by(locationname=po.poshipto).first()
    buyer = current_user

    poitems = POItemsInfo.query.order_by(POItemsInfo.id.asc()).all()

    formpo.povendor.choices = [po.povendor]+[(povendor.vendorname) for povendor in VendorsInfo.query.all()]
    formpo.poshipto.choices = [po.poshipto]+[(poshipto.locationname) for poshipto in LocationInfo.query.all()] 
    formpo.pojobtype2.choices = [po.pojobtype]+[('Field\\Fabrication Job'),('Corporate Office'),('Fabrication Shop'),('Insulation'),('Paint Shop'),('Texas Office')]

    form.poitemdescription.choices = [(poitemdescription.itemdescription) for poitemdescription in ItemsInfo.query.order_by(ItemsInfo.itemdescription.name).all()]

    return render_template("bomitemsv2.html", poitems=poitems, formexcel=formexcel, form=form, po=po, vendor=vendor, shipto=shipto, buyer=buyer, formpo=formpo)

##INITIALIZEBOMPO
@app.route("/initializebompo", methods=["POST", "GET"])
def initializebompo():
    my_data = POInfo.query.get(request.form.get('id'))
    ponumber = request.form['ponumber']

    my_data.pocreated = date.today()
    my_data.pojobtype = 'Field\\Fabrication Job'
    my_data.povendor = request.form['povendor']
    my_data.pojobtypenum = 30
    my_data.poshipto = request.form['poshipto']
    my_data.postatus = "Approved"
    nextpo = ponumber

    #TAX RATE CALCULATION ROUTINE
    vendor = VendorsInfo.query.filter_by(vendorname=my_data.povendor).first()
    receiving = LocationInfo.query.filter_by(locationname=my_data.poshipto).first()
    if vendor.vendorstate == 'OK' and receiving.locationstate == 'TX':
        my_data.potaxrate = vendor.vendortaxrate
    elif vendor.vendorstate != 'OK' and receiving.locationstate == 'OK':
        my_data.potaxrate = receiving.locationtaxrate
    else: 
        my_data.potaxrate = receiving.locationtaxrate
    if receiving.locationtaxrate == 0:
        my_data.potaxrate = 0

    subtotal = my_data.posubtotal
    taxrate = my_data.potaxrate
    my_data.pototal = subtotal + (subtotal * (taxrate/100))

    if my_data.postatus == "REQUEST FOR QUOTE":
        lastpo = POInfo.query.filter(POInfo.pojob == my_data.pojob).order_by(POInfo.ponumber.desc()).first()
        format = lastpo.ponumber.replace("-","")
        nextpo = int(format) + 1
        nextpo = str(nextpo)
        nextpo = my_data.pojob + '-' + nextpo[4:]
        my_data.ponumber=nextpo

    db.session.commit()

    poitems = POItemsInfo.query.filter_by(poitempo=ponumber).order_by(POItemsInfo.id.asc()).all()

    for each in poitems:
        each.poitempo = nextpo
        each.poitemvendor = my_data.povendor
        each.poitemjobtype = 'Field\\Fabrication Job'
        each.poitemjobtypenumber = 30
        db.session.commit()

    pdf(my_data.ponumber)
    print("PDF HAS BEEN CREATED")
    pdfnoprice(my_data.ponumber)
    print("receiving pdf copy created") 

    return redirect(url_for('bomitemsv2', ponumber=nextpo))

###BOMPO SINGLEPRICE UPDATE
@app.route('/singleprice', methods = ['GET', 'POST'])
def singleprice():
    if request.method == 'POST':
        my_data = POItemsInfo.query.get(request.form.get('id'))

        poitempo=my_data.poitempo
        my_data.poitemprice = request.form["poitemprice"]
        quantity = my_data.poitemquantity
        price = my_data.poitemprice

        total = int(quantity) * float(price)
        
        my_data.poitemtotalprice = total    
        db.session.commit()
        
        pdf(poitempo)
        print("PDF HAS BEEN CREATED")
        pdfnoprice(poitempo)
        print("receiving pdf copy created")
 
    return redirect(url_for('bomitemsv2', ponumber=poitempo))


##EXCELBOMPRICES
@app.route("/bomexcelprices", methods=["POST","GET"])
def bomexcelprices():
    ponumber = request.form['ponumber']                                                             #request ponumber to go back to previous page
    poitems = POItemsInfo.query.filter_by(poitempo=ponumber).order_by(POItemsInfo.id.asc()).all()  #filter only items that match current ponumber
    formexcel = ItemsForm()                                                                         #required to read file from form

    filename=secure_filename(formexcel.itemfile.data.filename)                                      #read data in excel file
    formexcel.itemfile.data.save('temp/' + filename)                                                #save file in server folder

    df = pd.read_excel('temp/' + filename, 0)                                                       #open saved file in sheet index0

    index=15
    posubtotal=0                                                                                         #declare counter variable to advance index
    for each in poitems: 
                                                                                  #for cycle every item on PO
        print(each.poitemdescription)                                                               #get description of each item
        print(df.iloc[index][3])                                                                    #get corresponding index value in pdf
        each.poitemprice = df.iloc[index][3]
        quantity = each.poitemquantity
        price = each.poitemprice 
        each.poitemtotalprice = quantity * price
        total = each.poitemtotalprice
        posubtotal = posubtotal + total
        db.session.commit()
        index+=1                                                                                    #autoincrement counter for index

    po = POInfo.query.filter_by(ponumber = ponumber).first()
    po.posubtotal = posubtotal
    db.session.commit()

    pdf(ponumber)
    print("PDF HAS BEEN CREATED")
    pdfnoprice(ponumber)
    print("receiving pdf copy created")

    return redirect(url_for('bomitemsv2', ponumber=ponumber))                                       #return to previous page


#BOM FILE PDF TEMPLATE
@app.route('/bom_pdf', methods = ['GET', 'POST'])
def bom_pdf():
    material = request.form['material']
    bomjobnumber = request.form['bomjobnumber']
    path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    pdfkit.from_url("http://127.0.0.1:5000/bom_template/" + str(material) + "/" + str(bomjobnumber), "c:/test/venv/pdf/bom_report" + str(material) + "-" + str(bomjobnumber) + ".pdf", configuration=config)
    filename = "bom_report" + str(material)

    path= "c:/test/venv/pdf/bom_report"+ str(material) + "-" + str(bomjobnumber) + ".pdf"
    #os.system(path)

    url = "http://127.0.0.1:5000/bom_excel/" + str(material) + "/" + str(bomjobnumber)
  
    # Assign the table data to a Pandas dataframe
    table = pd.read_html(url)[0]
    
    # Print the dataframe
    table.to_excel("/test/venv/bom/BOM-" + str(material) + "-" + bomjobnumber + ".xlsx")

    return send_file('/test/venv/bom/BOM-' + str(material) + "-" + bomjobnumber + ".xlsx", as_attachment=True)

    #return send_file('/test/venv/pdf/bom_report'+ str(material) + "-" + str(bomjobnumber) + ".pdf", as_attachment=True)

#BOM FILE HTML TEMPLATE
@app.route('/bom_template/<material>/<bomjobnumber>', methods = ['GET', 'POST'])
def bom_template(material,bomjobnumber):
    print(bomjobnumber)
    #Filter items in bom by requested query
    bom = BomInfo.query.filter(BomInfo.bomsearchterm.contains(material),BomInfo.bomjobnumber.like(bomjobnumber),BomInfo.bomstatus.like("RFQ")).order_by(BomInfo.bomdescription.desc())  #Filter if typed MAterial is in description    
    #Group items with unique descriptions
    unique = bom.group_by(BomInfo.bomdescription, BomInfo.bomsize).all()

    for i in bom:
        print(i.bomdescription)

    #initialize variables to store quantities
    quantity = 0
    qtotals = []            
    counter = 0
    feet=0
    inch=0
    fraction = Fraction(0,1)

    for i in unique:
        for full in bom:
            if full.bomdescription == i.bomdescription and full.bomsize == i.bomsize:
                if full.bomquantity.__contains__('"'):                              #REMEMBER ADD MORE CONDITIONS TO DIFFERIENTIATE
                    full = imperialstonumbers(full.bomquantity)
                    feet = feet + int(full[0])
                    inch = inch + int(full[1])
                    if inch >= 12:
                        inch= 0
                        feet = feet + 1
                    fraction = fraction + Fraction(int(full[2]),int(full[3]))
                    quantity = str(feet) + "'-" + str(inch) + '"' #+ str(fraction) + '"' ADD AND ROUND UP TO THE NEXT FEET
                else:   
                    quantity = quantity+ int(full.bomquantity)
            
        qtotals.append(quantity)                                                    #Add quantity to array
        quantity=0                                                                  #reinitialize variables
        feet=0
        inch=0
        fraction = Fraction(0,1)
        counter=counter+1
        
    print(qtotals)
    buyer = current_user

    return render_template("bom_template.html" , bom = unique, buyer=buyer, qtotals=qtotals)

def imperialstonumbers(imperials):
    if imperials.__contains__('-'):                  #cleanup pipe size input to get standard format
            start = imperials
    else:
        start= "-0 " + imperials
    cleaned = start.replace('-',"")
    fullclean = cleaned.replace("'"," ")
    ultra = fullclean.replace('"', "")
    if ultra.__contains__("/"):                                 #The string is ready to work separated in feet, inches, fractions
        ultra = ultra.replace("/"," ")
    else:
        ultra = ultra + " 0/1"
        ultra = ultra.replace("/", " ")

    fullnumbers = ultra.split(" ")
    return fullnumbers

#BOM FILE HTML TEMPLATE
@app.route('/bom_excel/<material>/<bomjobnumber>', methods = ['GET', 'POST'])
def bom_excel(material,bomjobnumber):
    print(bomjobnumber)
    #Filter items in bom by requested query
    bom = BomInfo.query.filter(BomInfo.bomsearchterm.contains(material),BomInfo.bomjobnumber.like(bomjobnumber),BomInfo.bomstatus.like("RFQ")).order_by(BomInfo.bomdescription.desc())  #Filter if typed MAterial is in description
    
    #Group items with unique descriptions
    unique = bom.group_by(BomInfo.bomdescription, BomInfo.bomsize).all()

    notes = JobsInfo.query.filter_by(jobnumber=bomjobnumber).all()
    
    notesqty = 0
    for k in notes:
        notesqty = notesqty + 1
    trueqty = 7 - notesqty    

    #initialize variables to store quantities
    quantity = 0
    qtotals = []            
    counter = 0
    feet=0
    inch=0
    fraction = Fraction(0,1)

    for i in unique:
        for full in bom:
            if full.bomdescription == i.bomdescription and full.bomsize == i.bomsize:
                if full.bomquantity.__contains__('"'):                              #REMEMBER ADD MORE CONDITIONS TO DIFFERIENTIATE
                    full = imperialstonumbers(full.bomquantity)
                    feet = feet + int(full[0])
                    inch = inch + int(full[1])
                    if inch >= 12:
                        inch= 0
                        feet = feet + 1
                    fraction = fraction + Fraction(int(full[2]),int(full[3]))
                    quantity = str(feet) + "'-" + str(inch) + '"' #+ str(fraction) + '"' ADD AND ROUND UP TO THE NEXT FEET
                else:   
                    quantity = quantity+ int(full.bomquantity)
            
        qtotals.append(quantity)                                                    #Add quantity to array
        quantity=0                                                                  #reinitialize variables
        feet=0
        inch=0
        fraction = Fraction(0,1)
        counter=counter+1
        today = date.today()
        
    print(qtotals)
    buyer = current_user

    return render_template("bom_excel.html" , bom = unique, buyer=buyer, qtotals=qtotals, notes=notes, bomjobnumber=bomjobnumber, today=today, trueqty=trueqty)

def imperialstonumbers(imperials):
    if imperials.__contains__('-'):                  #cleanup pipe size input to get standard format
            start = imperials
    else:
        start= "-0 " + imperials
    cleaned = start.replace('-',"")
    fullclean = cleaned.replace("'"," ")
    ultra = fullclean.replace('"', "")
    if ultra.__contains__("/"):                                 #The string is ready to work separated in feet, inches, fractions
        ultra = ultra.replace("/"," ")
    else:
        ultra = ultra + " 0/1"
        ultra = ultra.replace("/", " ")

    fullnumbers = ultra.split(" ")
    return fullnumbers


### GENERATE FLATFILE ####
@app.route('/flatfile')
@login_required
def flatfile():

    poitems = POItemsInfo.query.order_by(POItemsInfo.id.desc()).all()
    return render_template("flatfile.html", poitems=poitems)   

# FLATFILE GENERATION BY DATE
@app.route('/flatfile/export', methods = ['GET', 'POST'])
def flatfileexport():

    flatfiledate = request.form['flatfiledate']
    poitems = POItemsInfo.query.filter_by(poitemdate = flatfiledate).all()

    header =  ["Vendor","Job","Date","PO No.","Item","Description","Qty.","Rate","Unit","Amount","Tax","","","Job","","Item"]    

    with open('flatfile_' + str(flatfiledate) + '.csv', 'w', encoding='UTF8', newline='') as f:                      #Generate CSV file, writing mode, dont skip in new line
        writer = csv.writer(f)                                                  #Start writer mode

        writer.writerow(header)                                                 #Add a row to the csv

        for row in poitems:
            data = [row.poitemvendor,row.poitemjobtype,row.poitemdate,row.poitempo,str(row.poitemjobtypenumber) + str(row.poitemcostcode), row.poitemdescription, row.poitemquantity, "$" + str(row.poitemprice), row.poitemunit, "$" + str(row.poitemtotalprice),"5%" ,"","" , row.poitemjobtype ,row.poitemjobtypenumber, row.poitemcostcode]
            writer.writerow(data)
    
    flash("FlatFile for " + str(flatfiledate) + " has been generated!")

    return send_file('flatfile_' + str(flatfiledate) + '.csv', as_attachment=True)

# FLATFILE GENERATION BY PO-NUMBER
@app.route('/flatfilepo/export', methods = ['GET', 'POST'])
def flatfilepoexport():

    flatfileponumber = request.form['flatfileponumber']
    poitems = POItemsInfo.query.filter_by(poitempo = flatfileponumber).all()
    po = POInfo.query.filter_by(ponumber = flatfileponumber).first()

    header =  ["Vendor","Job","Date","PO No.","Item","Description","Qty.","Rate","Unit","Amount","Tax"]    

    with open(str(flatfileponumber) + " FF" + '.csv', 'w', encoding='UTF8', newline='') as f:                      #Generate CSV file, writing mode, dont skip in new line
        writer = csv.writer(f)                                                  #Start writer mode

        writer.writerow(header)                                                 #Add a row to the csv

        formattaxrate = format(po.potaxrate, '.4f')                         #Add 4 decimal places to tax rate
        print(formattaxrate)
        for row in poitems:
            data = [row.poitemvendor,row.poitemjobtype,row.poitemdate,row.poitempo,str(row.poitemjobtypenumber) + str(row.poitemcostcode), row.poitemdescription, row.poitemquantity, "$" + str(row.poitemprice), row.poitemunit, "$" + str(row.poitemtotalprice), str(formattaxrate) + "%"]
            writer.writerow(data)
    
    #Code to convert csv file to xlsx
    read_file = pd.read_csv (str(flatfileponumber) + " FF" + '.csv')
    read_file.to_excel (str(flatfileponumber) + " FF" + '.xlsx', index=None, header=True)

    flash("FlatFile for " + str(flatfileponumber) + " has been generated!")

    return send_file(str(flatfileponumber) + " FF" + '.xlsx', as_attachment=True)

### GENERATE SEND EMAIL ###
#Email pdf formats are generated in the server as soon as the PO gets approved
@app.route('/email', methods = ['GET', 'POST'])
def email():
    if request.method == 'POST':
        id = request.form['id']
        sendto = request.form['sendto']

        my_data = POInfo.query.get(id)
        print(my_data)
        outlook = win32com.client.Dispatch("outlook.application",pythoncom.CoInitialize())
        mail = outlook.CreateItem(0)
        
        mail.To = ''
        mail.Subject = 'PO #' + str(my_data.ponumber) + " " + str(my_data.povendor) + " " + str(my_data.pocreated)
        mail.HTMLBody = ''
        mail.Body = ''
        if sendto == "vendor":
            mail.Attachments.Add("c:/test/venv/pdf/po_report"+ str(my_data.ponumber) + ".pdf")
        elif sendto == "receiving":
            mail.Attachments.Add("c:/test/venv/pdf/po_receiving"+ str(my_data.ponumber) + ".pdf")
        mail.CC = ''

        mail.display(True)
        
        flash("PO Email generation for " + sendto + " successful")

        return redirect(url_for('poitemsv2', ponumber=my_data.ponumber))

#PORECEIVING
@app.route('/poreceiving', methods = ['GET', 'POST'])
def poreceiving():
    if request.method == 'POST':
        id = request.form['id']
        my_data = POInfo.query.get(id)
        return send_file("/test/venv/pdf/po_receiving"+ str(my_data.ponumber) + ".pdf", as_attachment=True)

#PODOWNLOAD
@app.route('/podownload', methods = ['GET', 'POST'])
def podownload():
    if request.method == 'POST':
        id = request.form['id']
        my_data = POInfo.query.get(id)
        return send_file("/test/venv/pdf/po_report"+ str(my_data.ponumber) + ".pdf", as_attachment=True)

#PODOWNLOADATTACHMENT
@app.route('/podownloadattachment', methods = ['GET', 'POST'])
def podownloadattachment():
    if request.method == 'POST':
        id = request.form['id']
        my_data = POInfo.query.get(id)

        path = "C:/test/venv/jobattachments/" + str(my_data.pojob)          #Path to find files in attachment folder
        dir_list = []
        try:                                                            #error handling in case folder does not exists                   
            dir_list=os.listdir(path)
            print(dir_list)
        except OSError as error:                                
            print(error)

        pdfs = dir_list

        merger = PdfMerger()

        merger.append("/test/venv/pdf/po_report"+ str(my_data.ponumber) + ".pdf")
        for pdf in pdfs:
            merger.append(path + "/" + pdf)

        merger.write("PO-MERGED.pdf")
        merger.close()

        return send_file("PO-MERGED.pdf", as_attachment=True)


### ROUTES FOR JOBNOTES AND JOBATTACHMENTS ###

@app.route('/jobnotes/<jobnumber>', methods = ["POST","GET"])
@app.route('/jobnotes', methods = ["POST","GET"])
@login_required
def jobnotes(jobnumber=""):
    form = LocationsForm()
    form.locationjobnumber.choices = [jobnumber]+[(locationjobnumber.locationjobnumber) for locationjobnumber in LocationInfo.query.all()] 

    path = "C:/test/venv/jobattachments/" + str(jobnumber)          #Path to find files in attachment folder
    dir_list = []
    try:                                                            #error handling in case folder does not exists                   
        dir_list=os.listdir(path)
        print(dir_list)
    except OSError as error:                                
        print(error)

    notes = JobsInfo.query.filter_by(jobnumber=jobnumber).all()

    return render_template("jobnotes.html", form=form, jobnumber=jobnumber, notes=notes, dir_list=dir_list)

@app.route('/jobredirect', methods=['POST','GET'])
def jobredirect():
    jobnumber=request.form['locationjobnumber']
    return redirect(url_for('jobnotes', jobnumber=jobnumber))

#ADD JOB NOTES
@app.route('/addjobnotes', methods=['POST','GET'])
def addjobnotes():
    jobnumber=request.form['jobnumber']
    jobnotes=request.form['jobnotes']

    my_data = JobsInfo( jobnumber, jobnotes)
    db.session.add(my_data)
    db.session.commit()

    return redirect(url_for('jobnotes', jobnumber=jobnumber))

#DELETE JOB NOTES
@app.route('/deletejobnotes/<id>/', methods = ['GET', 'POST'])
def deletejobnotes(id):
    my_data = JobsInfo.query.get(id)
    jobnumber = my_data.jobnumber
    db.session.delete(my_data)
    db.session.commit()

    return redirect(url_for('jobnotes', jobnumber=jobnumber))

#ADD INSERT ATTACHMENTS TO JOBS
@app.route('/addattachment', methods=['POST','GET'])
def addattachment():
    form = LocationsForm()
    jobnumber=request.form['jobnumber']

    #CODE TO create new folder in server
    directory = str(jobnumber)                              #Create new folder name
    parent_dir = "C:/test/venv/jobattachments/"             #Path where to put the folder
    path = os.path.join(parent_dir,directory)               

    try:                                                    #Error handling to avoid server error
        os.mkdir(path)
        print("Directory '%s' created" % directory) 
    except OSError as error:                                
        print(error)

    filename=secure_filename(form.locationattachment.data.filename)
    print(filename)
    form.locationattachment.data.save(path + "/" + filename)
    print("%s HAS BEEN SAVED SUCCESSFULLY" % filename)

    return redirect(url_for('jobnotes', jobnumber=jobnumber))

#DELETE ATTACHMENTS IN JOB FOLDERS
@app.route('/deletejobattachment/<filename>/<jobnumber>/', methods=['POST','GET'])
def deletejobattachment(filename,jobnumber):
    parent_dir = "C:/test/venv/jobattachments/" 

    os.remove(parent_dir + jobnumber + "/" + filename)
    print("%s has been removed from server" % filename)

    return redirect(url_for('jobnotes', jobnumber=jobnumber))

#DOWNLOAD JOB ATTACHMENT
@app.route('/downloadjobattachment/<filename>/<jobnumber>/', methods=['POST','GET'])
def downloadjobattachment(filename,jobnumber):
    parent_dir = "C:/test/venv/jobattachments/" 

    return send_file(parent_dir + jobnumber + "/" + filename, as_attachment=True)


### GENERATE A DYNAMIC PDF FOR PO ###

@app.route('/isti_po_format1/<ponumber>/pdf', methods = ['GET', 'POST'])
def pdf(ponumber):
    path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    pdfkit.from_url("http://127.0.0.1:5000/isti_po_format1/" + str(ponumber), "c:/test/venv/pdf/po_report"+ str(ponumber) + ".pdf", configuration=config)
    
    return redirect(url_for('poitemsv2', ponumber=ponumber))


### GENERATING DYNAMIC FINAL HTML REPORT ###
@app.route('/isti_po_format1/<ponumber>')
def isti_po_format1(ponumber):
    po = POInfo.query.filter_by(ponumber=ponumber).first()

    vendor = VendorsInfo.query.filter_by(vendorname=po.povendor).first()
    shipto = LocationInfo.query.filter_by(locationname=po.poshipto).first()
    buyer = current_user

    notes = JobsInfo.query.filter_by(jobnumber=po.pojob).all()

    all_data = POItemsInfo.query.order_by(POItemsInfo.id.asc()).all()  #Change all to only those who belong to po number
    itemslisted = POItemsInfo.query.filter_by(poitempo=po.ponumber).all()
    subtotal=0

    for each in itemslisted:         
        subtotal += each.poitemtotalprice

    taxed = subtotal * (po.potaxrate/100)
    taxed= round(taxed,2)
    total = subtotal + taxed
    subtotal = round(subtotal,2)
    total = round(total, 2)

    return render_template("isti_po_format1.html" , poitems = all_data, po=po, vendor=vendor, shipto=shipto, buyer=buyer, subtotal=subtotal, taxed=taxed, total=total, notes=notes)

### GENERATING RECEIVING PDF COPY OF PO ####
@app.route('/isti_po_format_priceless/<ponumber>')
def isti_po_format_priceless(ponumber):
    po = POInfo.query.filter_by(ponumber=ponumber).first()

    vendor = VendorsInfo.query.filter_by(vendorname=po.povendor).first()
    shipto = LocationInfo.query.filter_by(locationname=po.poshipto).first()
    buyer = current_user

    all_data = POItemsInfo.query.order_by(POItemsInfo.id.asc()).all()  #Change all to only those who belong to po number

    return render_template("isti_po_format_priceless.html" , poitems = all_data, po=po, vendor=vendor, shipto=shipto, buyer=buyer)

### USER LOGIN ROUTE ###
@app.route('/login' , methods = ['GET', 'POST'])
def Login():
    form = LoginForm()
 
    if request.method == 'POST':
        if form.validate_on_submit():
            user = UserInfo.query.filter_by(username=form.username.data).first()     #first() refers to the id field matching that username
 
            if user:                                                                #if the user exists, check for the password
                if check_password_hash(user.password, form.password.data):
                    login_user(user)
 
                    return redirect(url_for('poitemscp'))           #HOMEPAGE
  
                flash("Invalid Credentials")
 
    return render_template('login.html', form = form)
 
### USER LOGOUT ROUTE ####
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('Login'))

### USER REGISTRATION ROUTE ###
@app.route('/register' , methods = ['GET', 'POST'])
def register():
    form = RegistrationForm()
 
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method = 'sha256')
        username = form.username.data
        password = hashed_password
        name = form.name.data
        company=form.company.data
        usertype=form.usertype.data
        phone=form.phone.data
        email=form.email.data
  
        new_register =UserInfo(username=username, password=password, name=name, company=company, usertype=usertype, phone=phone, email=email)
        print(new_register)
        db.session.add(new_register)
 
        db.session.commit()
 
        flash("Registration was successfull, please login")
 
        return redirect(url_for('Login'))
 
    return render_template('register.html', form=form)

### BETA FEEDBACK.HTML ###
@app.route('/feedback', methods = ['GET','POST'])
def feedback():
    return render_template("feedback.html")

@app.errorhandler(404)
def not_found(e):
    return render_template("404.html")

#NOT SO GLOBAL FUNCTIONS

#FUNCTION TO PRINT PDF REPORT PRICED & PRICELESS
def pdf(ponumber):                                      #Function to print report pdf once it gets approved
    path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    pdfkit.from_url("http://127.0.0.1:5000/isti_po_format1/" + str(ponumber), "C:/test/venv/pdf/po_report"+ str(ponumber) + ".pdf", configuration=config)
    #pdfkit.from_url("LOCATION OF URL TO TRANSFORM", LOCATION+NAME OF NEW FILE (IN ROOT IF ONLY NAME PROVIDED), CONFIGURATION)

def pdfnoprice(ponumber):                                      #Function to print report pdf once it gets approved
    path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    pdfkit.from_url("http://127.0.0.1:5000/isti_po_format_priceless/" + str(ponumber), "C:/test/venv/pdf/po_receiving"+ str(ponumber) + ".pdf", configuration=config)
    #pdfkit.from_url("LOCATION OF URL TO TRANSFORM", LOCATION+NAME OF NEW FILE (IN ROOT IF ONLY NAME PROVIDED), CONFIGURATION)

