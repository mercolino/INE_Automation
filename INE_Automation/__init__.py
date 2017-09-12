from flask import Flask, render_template
import telnetlib
import os

app = Flask(__name__)

def create_lab_list():
    list = []
    for x in os.walk('tftproot'):
        path = x[0].split('/')
        if len(path) > 2:
            list.append(path[1] + ' --> ' + path[2])
    return list

@app.route('/load/<lab>/')
def load_lab(lab):
    list = create_lab_list()
    lab_split = lab.split(' --> ')
    loading = "Commands sent to load INE LAB '%s' from '%s'" % (lab_split[1], lab_split[0])
    return render_template('main.html', list=list, loading=loading)

#Main function to show the details of iridium Calls
@app.route('/')
def main():
    list = create_lab_list()
    return render_template('main.html', list = list, loading=None)


#Start the Flask application, WARNING: BEFORE PRODUCTION DEPLOYMENT CHANGE DEBUG TO FALSE
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

