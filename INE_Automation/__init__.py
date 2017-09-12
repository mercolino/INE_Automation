from flask import Flask, render_template
import telnetlib
import os
import threading
import time

app = Flask(__name__)
USERNAME = 'cisco'
PASSWORD = 'cisco'
TIMEOUT = 20


def send_commands(file):
    device_config = file.split('/')[-1]
    if (device_config)[:-4].lower() == 'r1':
        ip = '10.254.254.1'
    elif (device_config)[:-4].lower() == 'r2':
        ip = '10.254.254.2'
    elif (device_config)[:-4].lower() == 'r3':
        ip = '10.254.254.3'
    elif (device_config)[:-4].lower() == 'r4':
        ip = '10.254.254.4'
    elif (device_config)[:-4].lower() == 'r5':
        ip = '10.254.254.5'
    elif (device_config)[:-4].lower() == 'r6':
        ip = '10.254.254.6'
    elif (device_config)[:-4].lower() == 'r7':
        ip = '10.254.254.7'
    elif (device_config)[:-4].lower() == 'r8':
        ip = '10.254.254.8'
    elif (device_config)[:-4].lower() == 'r9':
        ip = '10.254.254.9'
    elif (device_config)[:-4].lower() == 'r10':
        ip = '10.254.254.10'
    elif (device_config)[:-4].lower() == 'r11':
        ip = '10.254.254.11'
    elif (device_config)[:-4].lower() == 'r12':
        ip = '10.254.254.12'
    elif (device_config)[:-4].lower() == 'r13':
        ip = '10.254.254.13'
    elif (device_config)[:-4].lower() == 'r14':
        ip = '10.254.254.14'
    elif (device_config)[:-4].lower() == 'r15':
        ip = '10.254.254.15'
    elif (device_config)[:-4].lower() == 'r16':
        ip = '10.254.254.16'
    elif (device_config)[:-4].lower() == 'r17':
        ip = '10.254.254.17'
    elif (device_config)[:-4].lower() == 'r18':
        ip = '10.254.254.18'
    elif (device_config)[:-4].lower() == 'r19':
        ip = '10.254.254.19'
    elif (device_config)[:-4].lower() == 'r20':
        ip = '10.254.254.20'
    elif (device_config)[:-4].lower() == 'sw1':
        ip = '10.254.254.51'
    elif (device_config)[:-4].lower() == 'sw2':
        ip = '10.254.254.52'
    elif (device_config)[:-4].lower() == 'sw3':
        ip = '10.254.254.53'
    elif (device_config)[:-4].lower() == 'sw4':
        ip = '10.254.254.54'

    # Connect to device
    telnet = telnetlib.Telnet(ip, 23, timeout=TIMEOUT)
    # Send Username
    telnet.write(USERNAME + '\n')
    time.sleep(1)
    # Send Password
    telnet.write(PASSWORD + '\n')
    time.sleep(1)
    # Reset configuration
    telnet.write('config replace bootflash:/configs/blank.cfg' + '\n')
    time.sleep(1)
    telnet.write('\n')
    time.sleep(1)
    telnet.write('copy tftp://10.254.254.100/' + file + '\n')
    time.sleep(1)
    telnet.write('\n')
    telnet.write('\n')
    telnet.write('\n')
    telnet.write('\n')
    telnet.close()
    return


def get_files(path):
    path = 'tftproot/' + path
    files = []
    for f in os.listdir(path):
        if os.path.isfile(os.path.join(path, f)):
            files.append(os.path.join(path,f))
    return files


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
    threads = []
    for file in get_files(lab_split[0] + '/' +lab_split[1]):
        t = threading.Thread(target=send_commands, args=(file[10:],))
        threads.append(t)
        t.start()
    return render_template('main.html', list=list, loading=loading)


#Main function to show the details of iridium Calls
@app.route('/')
def main():
    list = create_lab_list()
    return render_template('main.html', list = list, loading=None)


#Start the Flask application, WARNING: BEFORE PRODUCTION DEPLOYMENT CHANGE DEBUG TO FALSE
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)