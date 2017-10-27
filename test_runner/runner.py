'''
Created on Jul 18, 2017

@author: sgorle
@summary: Test runner for running the pytests and generated custom html report.
'''
from datetime import datetime
from optparse import OptionParser
import os
import re
import sys
import shutil
import time

from ctf.src.configure import Configure as conf
from email_send import email_report
from result_update import json_update, get_test_names
from zip import create_zip, final_report_zip
from sw_setup import install_python, install_studio_link
import test_properties as tp
        
 
def clean_dir(directory):
    """
    Removed the given directory.
    
    @param directory: 
            [string] directory path
    @return: None
    """
    shutil.rmtree(directory, ignore_errors = True)
    
def remove_file(file_path):
    """
    Removes the given file
    
    @param file_path: 
            [string] file name including path.
    @return:  None
    """
    if os.path.exists(file_path):
        os.remove(file_path)
    
    
usage = "usage: %prog [options] arg"
parser = OptionParser(usage)

parser.add_option("-s", "--setup", action="store_true", dest="setup", 
                  help="Checks for whether python and studio link installed and install them if not installed.")

parser.add_option("-t", "--tests", action="store_true", dest="tests", 
                  help="Runs the tests in a given path. Path should be given in the field tests_to_run_dir \
                  under test.properties.py file.")

parser.add_option("-r", "--report", action="store_true", dest="report", 
                  help="Generates the html report based on the configurations provided in yaml and test.properties.py")

parser.add_option("-e", "--email", action="store_true", dest="email", 
                  help="Sends out an email to the mentioned stake holders in the test.properties file.")

parser.add_option("-c", "--clean", action="store_true", dest="clean", 
                  help="Removes the generated logs, result and report files")

parser.add_option("-i", "--tag", action="store", type="string", dest="type",
                  help="type of test to perform eg: sanity, regression, basic, functional")
parser.add_option("-m", "--mentioned", action="store_true", dest="mentioned", 
                  help="Runs the tests mentioned in the test_suite.txt file under tests directory.")


(options, args) = parser.parse_args()

if len(sys.argv) < 2:
    parser.print_usage()
    sys.exit(1)

print "Started at {}".format(time.asctime(time.localtime(time.time())))    

if options.setup:
    install_python()
    install_studio_link()
    
if options.mentioned:
    clean_dir(tp.reports_dir)
    clean_dir(tp.final_report_dir)
    tests_to_run = []
    f = open(os.path.join(tp.test_suite_path + "/test_suite.txt"), 'r')
    lines = f.readlines()
    for line in lines:        
        matchObj = re.match(r'#.*', line, re.M|re.I)
        if matchObj is None:
            tests_to_run.append(line.strip())
            
    if len(tests_to_run) == 0:
        print "There are no tests existed in the tests/test_suite.txt file"
        exit()
    if not os.path.exists(tp.json_dir):
        os.makedirs(tp.json_dir)
    # start running now
    print "Running the selected tests..."
    start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    for test in tests_to_run:
        test_name = test.split('.py')[0].split('/')[-1]
        os.system("py.test -v -s {0} --json={1}/reports/results/{2}.json".format(test, tp.project_dir, test_name))
    
    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # Update yaml
    if tp.config is not None:
        conf.set_source(tp.config)
        conf.update_key('start_time', start_time)
        conf.update_key('end_time', end_time)

if options.tests:
    print "Running the tests..."
    clean_dir(tp.reports_dir)
    clean_dir(tp.final_report_dir)
    tests = get_test_names()
    if len(tests) == 0:
        print "There are no tests existed in the project directory {0}".format(tp.tests_to_run_dir)
        exit()
    if not os.path.exists(tp.json_dir):
        os.makedirs(tp.json_dir)
    start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    for test in tests:
        test_name = test.split('.py')[0].split('\\')[-1]       
        if options.type:
            os.system("py.test -v -s {0} --json={1}/reports/results/{2}.json --allure_features={3}".format(test, tp.project_dir, test_name, options.type))
        else:           
            os.system("py.test -v -s {0} --json={1}/reports/results/{2}.json".format(test, tp.project_dir, test_name))
    
    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # Update yaml
    if tp.config is not None:
        conf.set_source(tp.config)
        conf.update_key('start_time', start_time)
        conf.update_key('end_time', end_time)
    
if options.report:
    if options.tests:
        json_update()
    else:
        json_update(True) # means running tests from test_suite
    create_zip()
    # Generate HTML Report
    os.system(r'java -jar ctf\test_runner\lib\reportgen.jar -d {0} -z {1}/report.zip -y {2}'.format(tp.final_report_dir, tp.project_dir, tp.config))
    
if options.email:
    # Remove the result json file as these are not used in the report.
    clean_dir(tp.final_report_dir + "/data")
    remove_file(tp.final_report_dir + "/assets/report.vm")
    remove_file(tp.final_report_dir + "/assets/template.vm")
    final_report_zip()
    email_report(tp.subject, tp.sender, tp.to, html_message=tp.email_body)
    
if options.clean:
    print "cleaning reports, logs, results"
    clean_dir(tp.reports_dir)
    clean_dir(tp.final_report_dir)
    os.remove(tp.project_dir + r'/report.zip')
    print "Cleaning Done!!"

        