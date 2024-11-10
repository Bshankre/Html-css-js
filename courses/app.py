from flask import Flask ,render_template,request
from flask_mail import Mail
# from flask import flask_sqlalchemy
import json
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

with open('templates/config.json','r') as c:
    params = json.load(c)["params"]


local_server = True
app = Flask(__name__)

app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = '465',
    MAIL_USE_SSL = True ,
    MAIL_UERNAME = params['gmail-user'],
    MAIL_PASSWORD = params['gmail-password']
)

mail = Mail(app)

if(local_server):
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']

# app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:@localhost/courses"
db = SQLAlchemy(app)

class Contact(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(20),nullable=False)
    email=db.Column(db.String(20),nullable=False)
    phone_no=db.Column(db.String(12),nullable=False)
    msg=db.Column(db.String(500),nullable=False)
    date=db.Column(db.DateTime, default=datetime.utcnow)

  
@app.route("/",methods=["GET","POST"])
def course():
    if request.method=="POST":
        # fetching data from database
        name=request.form.get("name")
        email=request.form.get("email")
        phone=request.form.get("phone")
        message=request.form.get("message")
        # adding entry to database
        entry = Contact(name=name,phone_no=phone,msg=message,email=email)
        db.session.add(entry)
        db.session.commit()
        mail.send_message('New message from Contact'+ name,
                          sender=email,
                          recipients=[params['gmail-user']],
                          body =message +"\n" + phone 
                          )

    return render_template('python.html',params=params)
# @app.route("/contact")
# def Contact():
#     return render_template('contact.html')
if __name__ == '__main__':
    app.run(debug=True,port=8000)