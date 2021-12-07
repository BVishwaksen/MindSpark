from flask import Flask,render_template,request
import mysql.connector

mydb = mysql.connector.connect(host ="localhost",user="vishwa",passwd="1234",database="mindspark")

mycursor = mydb.cursor()


app = Flask(__name__)

@app.route('/',methods=['GET','POST'])
def index():
    if request.method == 'POST':
        sql = "INSERT INTO questions (qno,qname,description,inputf,outputf,constraints,samplei,sampleo,explanation) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        val = (request.form['qno'],request.form['name'],request.form['desc'],request.form['inputf'],request.form['outputf'],request.form['cons'],request.form['si'],request.form['so'],request.form['explanation'])
        mycursor.execute(sql, val)
        mydb.commit()
        sql = "INSERT INTO testcases(qno,inp_one,out_one,inp_two,out_two,inp_three,out_three) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        val = (request.form['qno'],request.form['inp_one'],request.form['out_one'],request.form['inp_two'],request.form['out_two'],
               request.form['inp_three'],request.form['out_three'])
        mycursor.execute(sql,val)
        mydb.commit()
        return "Data Insertion Successfull"
    return render_template('qpaper.html')

if __name__ == "__main__":
    app.run(debug=True)
