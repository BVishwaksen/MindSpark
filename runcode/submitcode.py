from subprocess import Popen,PIPE
import mysql.connector

mydb = mysql.connector.connect(host ="localhost",user="vishwa",passwd="1234",database="mindspark")

mycursor = mydb.cursor()


no_tests = 3



def submitC(qno):
    counter = 0
    values = []
    inputs=[]
    outputs=[]
    mycursor.execute("select * from testcases")
    result = mycursor.fetchall()
    for i in range(0,7):
        values.append(result[qno-1][i])
    for i in range(1,7):
        if i%2 == 0:
            outputs.append(values[i])
        else:
            inputs.append(values[i])
    for i in range(0,3):
        p = Popen(['a.out'],shell=True,stdout=PIPE,stdin=PIPE,stderr=PIPE)
        check_list = []
        out_list = []
        for ele in inputs[i].split():
            temp = str(ele)+"\n"
            temp = bytes(temp,'UTF-8')
            p.stdin.write(temp)
            p.stdin.flush()
        result,err = p.communicate()
        for j in result.decode('UTF-8'):
            check_list.append(j)
        if len(check_list)>=2:
            if check_list[-1] in ['\r','\n']:
                check_list.pop(-1)
            if check_list[-1] in ['\r','\n']:
                check_list.pop(-1)
        for k in outputs[i]:
            out_list.append(k)
        if check_list == out_list:
            counter = counter+1
    out_str = "Out of {} testcases {} are passed".format(no_tests,counter)
    return out_str,counter




def submitCpp(qno):
    counter = 0
    values = []
    inputs=[]
    outputs=[]
    mycursor.execute("select * from testcases")
    result = mycursor.fetchall()
    for i in range(0,7):
        values.append(result[qno-1][i])
    for i in range(1,7):
        if i%2 == 0:
            outputs.append(values[i])
        else:
            inputs.append(values[i])
    for i in range(0,no_tests):
        p = Popen(['a.out'],shell=True,stdout=PIPE,stdin=PIPE,stderr=PIPE)
        check_list = []
        out_list = []
        for ele in inputs[i].split():
            temp = str(ele)+"\n"
            temp = bytes(temp,'UTF-8')
            p.stdin.write(temp)
            p.stdin.flush()
        result,err = p.communicate()
        for j in result.decode('UTF-8'):
            check_list.append(j)
        if len(check_list)>=2:
            if check_list[-1] in ['\r','\n']:
                check_list.pop(-1)
            if check_list[-1] in ['\r','\n']:
                check_list.pop(-1)
        for k in outputs[i]:
            out_list.append(k)
        if check_list == out_list:
            counter = counter+1
    out_str = "Out of {} testcases {} are passed".format(no_tests,counter)
    return out_str,counter
          



def submitPy(qno):
    counter = 0
    values=[]
    inputs=[]
    outputs=[]
    mycursor.execute("select * from testcases")
    result = mycursor.fetchall()
    for i in range(0,7):
        values.append(result[qno-1][i])
    for i in range(1,7):
        if i%2 == 0:
            outputs.append(values[i])
        else:
            inputs.append(values[i])
    for i in range(0,3):
        p = Popen(['a.py'],shell=True,stdout=PIPE,stdin=PIPE,stderr=PIPE)
        check_list = []
        out_list = []
        for ele in inputs[i]:
            temp = str(ele)
            temp = bytes(temp,'UTF-8')
            p.stdin.write(temp)
            p.stdin.flush()
        result,err = p.communicate()
        for j in result.decode('UTF-8'):
            check_list.append(j)
        if len(check_list)>=2:
            if check_list[-1] in ['\r','\n']:
                check_list.pop(-1)
            if check_list[-1] in ['\r','\n']:
                check_list.pop(-1)
        for k in outputs[i]:
            out_list.append(k)
        if check_list == out_list:
            counter = counter+1
    out_str = "Out of {} testcases {} are passed".format(no_tests,counter)
    return out_str,counter



def submitJava(qno):
    counter = 0
    values=[]
    inputs=[]
    outputs=[]
    mycursor.execute("select * from testcases")
    result = mycursor.fetchall()
    for i in range(0,7):
        values.append(result[qno-1][i])
    for i in range(1,7):
        if i%2 == 0:
            outputs.append(values[i])
        else:
            inputs.append(values[i])
    for i in range(0,3):
        p = Popen(['java','Solution'],shell=True,stdout=PIPE,stdin=PIPE,stderr=PIPE)
        check_list = []
        out_list = []
        for ele in inputs[i].split():
            temp = str(ele)+"\n"
            temp = bytes(temp,'UTF-8')
            p.stdin.write(temp)
            p.stdin.flush()
        result,err = p.communicate()
        for j in result.decode('UTF-8'):
            check_list.append(j)
        if len(check_list)>=2:
            if check_list[-1] in ['\r','\n']:
                check_list.pop(-1)
            if check_list[-1] in ['\r','\n']:
                check_list.pop(-1)
        for k in outputs[i]:
            out_list.append(k)
        if check_list == out_list:
            counter = counter+1
    out_str = "Out of {} testcases {} are passed".format(no_tests,counter)
    return out_str,counter



