from flask import Flask,render_template,request,session,logging,url_for,redirect,flash,g
import mysql.connector
from runcode import runcode,submitcode
import subprocess
import sys
import os


mydb = mysql.connector.connect(host ="localhost",user="vishwa",passwd="1234",database="mindspark")

mycursor = mydb.cursor()

app = Flask(__name__)
app.secret_key = os.urandom(24)

default_c_code = """#include <stdio.h>

int main(int argc, char **argv)
{
    printf("Hello C World!!\\n");
    return 0;
}    
"""

default_cpp_code = """#include <iostream>

using namespace std;

int main(int argc, char **argv)
{
    cout << "Hello C++ World" << endl;
    return 0;
}
"""

default_py_code = """import sys
import os

if __name__ == "__main__":
    print ("Hello Python World!!")
"""
default_java_code = """import java.lang.*;
import java.util.*;
public class Solution
{
    public static void main(String args[])
    {
      System.out.println("Hello Java World");
    }
}

"""

default_rows = "15"
default_cols = "60"


@app.route("/",methods=['GET','POST'])
def login():
    user_list = []
    error = None
    if request.method == 'POST':
      session.pop('user',None)
      mycursor.execute("select * from student")
      result = mycursor.fetchall()
      for student in result:
        user_list.append(student[0])
      if request.form['username'] not in user_list  or  request.form['password'] != request.form['username']:
        error = 'Invalid Credentials,Please try again'
      else:
        session['user'] = request.form['username']
        return redirect(url_for('landing'))
    return render_template('login.html',error=error)

@app.before_request
def before_request():
  g.user = None
  if 'user' in session:
    g.user = session['user']

@app.route('/getsession')
def getsession():
  if 'user' in session:
    return session['user']
  return 'Not logged in'

@app.route('/dropsession')
def dropsession():
  session.pop('user',None)
  return render_template('logout.html')


@app.route("/landing",methods=['POST','GET'])
def landing():
  if g.user:
    if request.method == 'POST':
      if request.form['butto_n']=='test':
        return redirect(url_for('terms'))
      else:
        return redirect(url_for('dropsession'))
    
    return render_template("land.html")
  return redirect("")

@app.route("/terms",methods=['POST','GET'])
def terms():
    if request.method == 'POST':
      if request.form['submit'] == 'accept':
        return redirect(url_for('questions'))
      else:
        return redirect(url_for('dropsession'))
    return render_template("newterms.html")

@app.route("/questions",methods=['GET','POST'])
def questions():
    mycursor.execute("select * from questions")
    result = mycursor.fetchall()
    no_of_questions = len(result)
    
    name = []
    desc = []
    inputf = []
    outputf = []
    cons = []
    si = []
    so = []
    explanation = []
    for i in range(0,no_of_questions):
        name.append(result[i][1])
        desc.append(result[i][2])
        inputf.append(result[i][3])
        outputf.append(result[i][4])
        cons.append(result[i][5])
        si.append(result[i][6])
        so.append(result[i][7])
        explanation.append(result[i][8])
    if request.method == 'POST':
        if request.form['editor']=='Go To Editor':
            return redirect(url_for('runc'))
        else:
            return redirect(url_for('questions'))
    return render_template("ques.html",no_of_questions=no_of_questions,name=name,
                           desc=desc,inputf=inputf,outputf=outputf,cons=cons,si=si,so=so,explanation=explanation,target="runc")


@app.route("/editor")
@app.route("/runc", methods=['POST', 'GET'])
def runc():
    if request.method == 'POST':
        if request.form['submit'] == 'Run':
            mycursor.execute("select * from questions")
            result = mycursor.fetchall()
            no_of_questions = len(result)
            q = request.form['qno']
            qno = int(q)
            code = request.form['code']
            if qno>0 and qno<=no_of_questions:
                run = runcode.RunCCode(code)
                rescompil, resrun = run.run_c_code(qno)
                if not resrun:
                    resrun = 'No result!'
            else:
                rescompil = ''
                resrun = "Invalied Question Number"
        else:
            q = request.form['qno']
            qno = int(q)
            code = request.form['code']
            resrun,count = submitcode.submitC(qno)
            rescompil = ''
    else:
        qno = ''
        code = default_c_code
        resrun = 'No result!'
        rescompil = ''
    return render_template("newmain.html",
                           code=code,
                           target="runc",
                           resrun=resrun,
                           rescomp=rescompil,
                           rows=default_rows, cols=default_cols,value=qno)

@app.route("/cpp")
@app.route("/runcpp", methods=['POST', 'GET'])
def runcpp():
    if request.method == 'POST':
        if request.form['submit'] == 'Run':
            mycursor.execute("select * from questions")
            result = mycursor.fetchall()
            no_of_questions = len(result)
            q = request.form['qno']
            qno = int(q)
            code = request.form['code']
            if qno>0 and qno<=no_of_questions:
                run = runcode.RunCppCode(code)
                rescompil, resrun = run.run_cpp_code(qno)
                if not resrun:
                    resrun = 'No result!'
            else:
                rescompil = ''
                resrun = "Invalied Question Number"
        else:
            q = request.form['qno']
            qno = int(q)
            code = request.form['code']
            resrun,count = submitcode.submitCpp(qno)
            rescompil = ''
    else:
        qno = ''
        code = default_cpp_code
        resrun = 'No result!'
        rescompil = ''
    return render_template("newmain.html",
                           code=code,
                           target="runcpp",
                           resrun=resrun,
                           rescomp=rescompil,
                           rows=default_rows, cols=default_cols,value=qno)
    

@app.route("/py")
@app.route("/runpy", methods=['POST', 'GET'])
def runpy():
    if request.method == 'POST':
        if request.form['submit'] == 'Run':
            mycursor.execute("select * from questions")
            result = mycursor.fetchall()
            no_of_questions = len(result)
            q = request.form['qno']
            qno = int(q)
            code = request.form['code']
            if qno>=0 and qno<=no_of_questions:
                run = runcode.RunPyCode(code)
                rescompil, resrun = run.run_py_code(qno)
                if not resrun:
                    resrun = 'No result!'
            else:
                rescompil = ''
                resrun = "Invalied Question Number"
        else:
            q = request.form['qno']
            qno = int(q)
            code = request.form['code']
            resrun,count = submitcode.submitPy(qno)
            rescompil = ''
    else:
        qno = ''
        code = default_py_code
        resrun = 'No result!'
        rescompil = "No compilation for Python"
        
    return render_template("newmain.html",
                           code=code,
                           target="runpy",
                           resrun=resrun,
                           rescomp=rescompil,#"No compilation for Python",
                           rows=default_rows, cols=default_cols,value=qno)
@app.route("/java")
@app.route("/runjava", methods=['POST', 'GET'])
def runjava():
    if request.method == 'POST':
        if request.form['submit'] == 'Run':
            mycursor.execute("select * from questions")
            result = mycursor.fetchall()
            no_of_questions = len(result)
            q = request.form['qno']
            qno = int(q)
            code = request.form['code']
            if qno>=0 and qno<=no_of_questions:            
                run = runcode.RunJavaCode(code)
                rescompil, resrun = run.run_java_code(qno)
                if not resrun:
                    resrun = 'No result!'
            else:
                rescompil = ''
                resrun = "Invalied Question Number"
        else:
            q = request.form['qno']
            qno = int(q)
            code = request.form['code']
            resrun,count = submitcode.submitJava(qno)
            rescompil = ''
    else:
        qno = ''
        code = default_java_code
        resrun = 'No result!'
        rescompil = ''
    return render_template("newmain.html",
                           code=code,
                           target="runjava",
                           resrun=resrun,
                           rescomp=rescompil,
                           rows=default_rows, cols=default_cols,value=qno)

if __name__== "__main__":
    app.run(debug=True)
