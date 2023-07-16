from flask import Flask, render_template, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user, AnonymousUserMixin
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
from datetime import datetime, timedelta
import razorpay
import os
import yfinance as yf
#import talib as tb
import pandas as pd
from functools import lru_cache
from datagain import DataGain as dg
from indicators import IndicatorsApply as ia
from conditions import ConditionsApply as ca
import csv

db=SQLAlchemy()
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///database.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SECRET_KEY'] = 'papaBABUpapa_3_200220062010_4YGap'
db.init_app(app)
bcrypt = Bcrypt(app)

login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view="login"

sell_list=[]
buy_list=[]
candles = 20
symbols = ['GUJGASLTD', 'PERSISTENT', 'DIXON', 'IPCALAB', 'BEL', 'IDFCFIRSTB', 'PETRONET', 'MUTHOOTFIN', 'IDFC', 'PAGEIND', 'BHARTIARTL', 'DLF', 'LALPATHLAB', 'POWERGRID', 'JKCEMENT', 'DABUR', 'PEL', 'MGL', 'JINDALSTEL', 'PFC', 'CANBK', 'RAMCOCEM', 'KOTAKBANK', 'PVRINOX', 'MPHASIS', 'ALKEM', 'HINDALCO', 'LICHSGFIN', 'IGL', 'POLYCAB', 'WIPRO', 'ICICIPRULI', 'DELTACORP', 'INTELLECT', 'SIEMENS', 'TVSMOTOR', 'COFORGE', 'GODREJPROP', 'OBEROIRLTY', 'MCX', 'L&TFH', 'BRITANNIA', 'TCS', 'LAURUSLABS', 'SAIL', 'LTIM', 'TECHM', 'JUBLFOOD', 'SBILIFE', 'SBIN', 'HDFCAMC', 'ABBOTINDIA', 'IRCTC', 'BHEL', 'MARICO', 'GAIL', 'INDIAMART', 'CONCOR', 'TATAPOWER', 'TORNTPHARM', 'SBICARD', 'NTPC', 'TRENT', 'TITAN', 'CHAMBLFERT', 'BAJAJFINSV', 'DIVISLAB', 'ZYDUSLIFE', 'SHREECEM', 'ZEEL', 'RECLTD', 'SRF', 'IOC', 'MFSL', 'CANFINHOME', 'EICHERMOT', 'HAVELLS', 'HDFCLIFE', 'EXIDEIND', 'FSL', 'RAIN', 'GODREJCP', 'INDIACEM', 'IEX', 'IBULHSGFIN', 'TATAMOTORS', 'COALINDIA', 'ESCORTS', 'M&MFIN', 'CROMPTON', 'BPCL', 'AARTIIND', 'ASIANPAINT', 'PNB', 'ASTRAL', 'BALRAMCHIN', 'RELIANCE', 'COROMANDEL', 'NESTLEIND', 'PIDILITIND', 'GRASIM', 'LTTS', 'INDUSTOWER', 'HEROMOTOCO', 'RBLBANK', 'BIOCON', 'DEEPAKNTR', 'MANAPPURAM', 'ABB', 'TATACOMM', 'TATACONSUM', 'GRANULES', 'INDIGO', 'GMRINFRA', 'JSWSTEEL', 'HAL', 'ICICIGI', 'MRF', 'ICICIBANK', 'SUNPHARMA', 'HCLTECH', 'ITC', 'TATACHEM', 'ABCAPITAL', 'BATAINDIA', 'DRREDDY', 'NATIONALUM', 'DALBHARAT', 'INDHOTEL', 'M&M', 'VOLTAS', 'CHOLAFIN', 'ASHOKLEY', 'PIIND', 'INDUSINDBK', 'BANDHANBNK', 'ATUL', 'INFY', 'SUNTV', 'ULTRACEMCO', 'MOTHERSON', 'UBL', 'BHARATFORG', 'LT', 'AUROPHARMA', 'VEDL', 'NAVINFLUOR', 'TORNTPOWER', 'APOLLOTYRE', 'METROPOLIS', 'BAJAJ-AUTO', 'BSOFT', 'HONAUT', 'MCDOWELL-N', 'ABFRL', 'HINDUNILVR', 'FEDERALBNK', 'SYNGENE', 'ACC', 'OFSS', 'BOSCHLTD', 'CIPLA', 'TATASTEEL', 'APOLLOHOSP', 'AXISBANK', 'AMBUJACEM', 'UPL', 'BAJFINANCE', 'CUMMINSIND', 'HDFCBANK', 'MARUTI', 'HINDPETRO', 'GNFC', 'BANKBARODA', 'CUB', 'HDFC', 'LUPIN', 'SHRIRAMFIN', 'BALKRISIND', 'AUBANK', 'ONGC', 'COLPAL', 'NAUKRI', 'BERGEPAINT', 'NMDC', 'GLENMARK', 'HINDCOPPER', 'DMART', 'ANURAS', 'AVANTIFEED', 'CEATLTD', 'FINCABLES', 'PAYTM', 'THERMAX', 'VIPIND', 'ECLERX']
#symbols = ['GODREJPROP','DEEPAKNTR','GUJGASLTD', 'PERSISTENT', 'DIXON', 'IPCALAB', 'BEL', 'IDFCFIRSTB', 'PETRONET', 'MUTHOOTFIN', 'IDFC', 'PAGEIND', 'NTPC', 'TRENT', 'TITAN', 'CHAMBLFERT', 'BAJAJFINSV', 'DIVISLAB', 'ZYDUSLIFE']
symbols = [x+'.ns' for x in symbols]

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    reg_date =  db.Column(db.DateTime(timezone=True), default=datetime.now(), nullable=False)
    subscription_date = db.Column(db.DateTime(timezone=True), default=datetime.now(), nullable=False)
    expiry_date = db.Column(db.DateTime(timezone=True), default=datetime.now()+timedelta(days=45))
##    razorpay_payment_id = db.Column(db.String(120), nullable=True)
##    razorpay_order_id = db.Column(db.String(120), nullable=True)
##    razorpay_signature = db.Column(db.String(120), nullable=True)
        

class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder":"Username"})
    email = StringField(validators=[InputRequired(), Length(min=4, max=80)], render_kw={"placeholder":"Email"})
    password = StringField(validators=[InputRequired(), Length(min=4, max=80)], render_kw={"placeholder":"Password"})
    submit = SubmitField("Login")

    def validate_user(self, email):
        existing_user_email=User.query.filter_by(email=email.data).first()
        

class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder":"Username"})
    email = StringField(validators=[InputRequired(), Length(min=4, max=80)], render_kw={"placeholder":"Email"})
    password = StringField(validators=[InputRequired(), Length(min=4, max=80)], render_kw={"placeholder":"Password"})
    submit = SubmitField("Register")

    def validate_user(self, email):
        existing_user_email=User.query.filter_by(email=email.data).first()
        if existing_user_email:
            raise ValidationError("Email you entered is already exist. Please enter another Email")

class SubscriptionForm(FlaskForm):
    email = StringField(validators=[InputRequired(), Length(min=4, max=80)], render_kw={"placeholder":"Email"})
    submit = SubmitField("Subcribe")
    
    #def validate_user(self, email):
        #existing_user_email=User.query.filter_by(email=email.data).first()
        #if not existing_user_email:
            #raise ValidationError("Email you entered is not registered yet. Go to Register ...")
        
def save_list_to_csv(data_list, filename):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(data_list)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data) and user.expiry_date > datetime.now():
                login_user(user)
                return redirect(url_for('screener', user=current_user))
            else:
                return redirect(url_for('payment', id=user.id, user=current_user))
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    user = User.query.filter_by(email=form.email.data).first()
    if form.validate_on_submit():
        if user:
            return redirect(url_for('login'))
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username = form.username.data, email= form.email.data, password=hashed_password, expiry_date = datetime.now()+timedelta(days=2))
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
        
    return render_template('register.html', form=form)

@app.route('/screener', methods=['GET', 'POST'])
@login_required
def screener():
    filtered_data = []
    #try:
    for symbol in symbols:
        sf=dg.data_rec(symbol=symbol, period='60d', interval='15m')
        data_15 = ia.indicators(sf)
        data = ca.conditions(symbol, data_15)
        if data is not None:
            filtered_data.extend(data)
    #except:
        #pass
    return render_template('screener.html', data=sorted(filtered_data, key=lambda x: x[1], reverse=True))

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/payment<id>', methods=['GET', 'POST'])
def payment(id):
    global payment
    user = User.query.filter_by(id=id).first()
    key="rzp_test_2HpbR9UNCKlbAY"
    razorpay_client = razorpay.Client(auth=("rzp_test_2HpbR9UNCKlbAY", "qSM6vjcPprS5d3jwnGpxzy0V"))
    amount = 30
    data = {
        'amount':amount*100,
        'currency': 'INR',
        'receipt': 'AnuSmartTraders_receipt'
    }
    payment = razorpay_client.order.create(data=data)
    return render_template('payment.html', payment=payment, id=id, user=current_user)

@app.route('/payment_success<id>', methods=['GET', 'POST'])
def payment_success(id):
    razorpay_client = razorpay.Client(auth=("rzp_test_2HpbR9UNCKlbAY", "qSM6vjcPprS5d3jwnGpxzy0V"))
    #payment = request.args.get('payment')
    order_id = request.form.get('razorpay_order_id')
    payment_id = request.form.get('razorpay_payment_id')
    signature = request.form.get('razorpay_signature')
    params = {
        'razorpay_order_id': order_id,
        'razorpay_payment_id': payment_id,
        'razorpay_signature': signature
    }
    try:
        razorpay_client.utility.verify_payment_signature(params)
        usr = User.query.filter_by(id=id).first()
        usr.subscription_date = datetime.now()
        usr.expiry_date = datetime.now()+timedelta(days=30)
        db.session.commit()
        return "Payment Success"
    except razorpay.errors.BadRequestError as e:
        # Payment verification failed
        return "Payment verification failed."

@app.route('/success')
def success():
    return render_template('success.html')


if __name__ == '__main__':
    app.run(debug=True)
