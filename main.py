from flask import Flask , render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
db= SQLAlchemy(app)


class Card(db.Model):
    sno= db.Column(db.Integer, primary_key=True)
    ques=db.Column(db.String(200), nullable=False)
    ans= db.Column(db.String(500), nullable=False)
    date_created=db.Column(db.DateTime(), default= datetime.utcnow())

    def __repr__(self)-> str:
        return f"{self.sno} - {self.ques}"

@app.route("/", methods=['GET','POST'])
def homepage():

    if request.method == "POST":
        ques=request.form['ques']
        ans= request.form['ans']
        card = Card(ques=ques, ans=ans)
        db.session.add(card)
        db.session.commit() 
    
    allTodo=Card.query.all()
    return render_template('home.html', at= allTodo)





@app.route('/delete/<int:sno>')
def delete(sno):
    card = Card.query.filter_by(sno=sno).first()
    db.session.delete(card)
    db.session.commit()
    return redirect('/')

@app.route('/update/<int:sno>', methods=['GET','POST'])
def update(sno):
    if request.method == 'POST':
        ques=request.form['ques']
        ans= request.form['ans']
        card = Card.query.filter_by(sno=sno).first()
        card.ques = ques
        card.ans = ans
        card.date_created= datetime.utcnow()
        db.session.add(card)
        db.session.commit()
        return redirect('/')

    card = Card.query.filter_by(sno=sno).first()
    return render_template("update.html",card=card)


@app.route('/show/<int:sno>', methods=['GET','POST'])
def show(sno):
    if request.method == 'POST':
        return redirect('/')
    
    card = Card.query.filter_by(sno=sno).first()
    return render_template("show.html", card=card)



if  __name__ == '__main__':
    app.run(debug=True)