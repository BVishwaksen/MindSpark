import subprocess
import sys
import os
import mysql.connector

mydb = mysql.connector.connect(host ="localhost",user="vishwa",passwd="1234",database="mindspark")

mycursor = mydb.cursor()




class RunCCode(object):
    
    def __init__(self, code=None):
        self.code = code
        self.compiler = "gcc"
        if not os.path.exists('running'):
            os.mkdir('running')
    
    def _compile_c_code(self, filename, prog="./running/a.out"):
        cmd = [self.compiler, filename, "-Wall", "-o", prog]
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        result = p.wait()
        a, b = p.communicate()
        self.stdout, self.stderr = a.decode("utf-8"), b.decode("utf-8")
        return result

    def _run_c_prog(self,qno):
        mycursor.execute("select samplei from questions")
        result = mycursor.fetchall()
        p = subprocess.Popen(['a.out'],stdin=subprocess.PIPE,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        values = result[qno-1]
        for i in values:
            value = str(i)+'\n'
            value = bytes(value,'utf-8')
            p.stdin.write(value)
            p.stdin.flush()
        result = p.wait()
        a, b = p.communicate()
        self.stdout, self.stderr = a.decode("utf-8"), b.decode("utf-8")
        return result
    
    def run_c_code(self,qno, code=None):
        filename = "./running/test.c"
        if not code:
            code = self.code
        result_run = "No run done"
        with open(filename, "w") as f:
            f.write(code)
        res = self._compile_c_code(filename)
        result_compilation = self.stdout + self.stderr
        if res == 0:
            self._run_c_prog(qno)
            result_run = self.stdout + self.stderr
        return result_compilation, result_run


class RunCppCode(object):

    def __init__(self, code=None):
        self.code = code
        self.compiler = "g++"
        if not os.path.exists('running'):
            os.mkdir('running')

    def _compile_cpp_code(self, filename, prog="./running/a.out"):
        cmd = [self.compiler, filename, "-Wall", "-o", prog]
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        result = p.wait()
        a, b = p.communicate()
        self.stdout, self.stderr = a.decode("utf-8"), b.decode("utf-8")
        return result

    def _run_cpp_prog(self,qno):
        mycursor.execute("select samplei from questions")
        result = mycursor.fetchall()
        p = subprocess.Popen('a.out',stdin=subprocess.PIPE,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        values = result[qno-1]
        for i in values:
            value = str(i)+'\n'
            value = bytes(value,'utf-8')
            p.stdin.write(value)
            p.stdin.flush()
        result = p.wait()
        a, b = p.communicate()
        self.stdout, self.stderr = a.decode("utf-8"), b.decode("utf-8")
        return result

    def run_cpp_code(self,qno,code=None):
        filename = "./running/test.cpp"
        if not code:
            code = self.code
        result_run = "No run done"
        with open(filename, "w") as f:
            f.write(code)
        res = self._compile_cpp_code(filename)
        result_compilation = self.stdout + self.stderr
        if res == 0:
            self._run_cpp_prog(qno)
            result_run = self.stdout + self.stderr
        return result_compilation, result_run

class RunPyCode(object):
    
    def __init__(self, code=None):
        self.code = code
        if not os.path.exists('running'):
            os.mkdir('running')

    def _run_py_prog(self,qno,cmd="a.py"):
        cmd = [sys.executable, cmd]
        mycursor.execute("select samplei from questions")
        result = mycursor.fetchall()
        p = subprocess.Popen(cmd,stdin=subprocess.PIPE,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        values = result[qno-1]
        for i in values:
            value = str(i)+'\n'
            value = bytes(value,'utf-8')
            p.stdin.write(value)
            p.stdin.flush()
        result = p.wait()
        a, b = p.communicate()
        self.stdout, self.stderr = a.decode("utf-8"), b.decode("utf-8")
        return result
    
    def run_py_code(self,qno, code=None):
        filename = "./running/a.py"
        if not code:
            code = self.code
        with open(filename, "w") as f:
            f.write(code)
        self._run_py_prog(qno,filename)
        return self.stderr, self.stdout

    
class RunJavaCode(object):

    def __init__(self, code=None):
        self.code = code
        self.compiler = "javac"
        if not os.path.exists('running'):
            os.mkdir('running')

    def _compile_java_code(self, filename):
        cmd = [self.compiler, filename]
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        result = p.wait()
        a, b = p.communicate()
        self.stdout, self.stderr = a.decode("utf-8"), b.decode("utf-8")
        return result

    def _run_java_prog(self,qno):
        mycursor.execute("select samplei from questions")
        result = mycursor.fetchall()
        p = subprocess.Popen(['java','Solution'],stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        values = result[qno-1]
        for i in values:
            value = str(i)+'\n'
            value = bytes(value,'utf-8')
            p.stdin.write(value)
            p.stdin.flush()
        result = p.wait()
        a, b = p.communicate()
        self.stdout, self.stderr = a.decode("utf-8"), b.decode("utf-8")
        return result

    def run_java_code(self,qno,code=None):
        filename = "./running/Solution.java"
        if not code:
            code = self.code
        result_run = "No run done"
        with open(filename, "w") as f:
            f.write(code)
        res = self._compile_java_code(filename)
        result_compilation = self.stdout + self.stderr
        if res == 0:
            self._run_java_prog(qno)
            result_run = self.stdout + self.stderr
        return result_compilation, result_run

