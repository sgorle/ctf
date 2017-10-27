'''
Created on Jul 25, 2017

@author: sgorle
@summary: Utility to updates the json files with the required report content.
'''
import fnmatch
import glob
import json
import re
import os

import test_properties as tp


current_dir = os.getcwd()

def get_test_names():
    """
    Gets the test script names in a given test project directory i config file.
    
    @return: [list] test script names in the given project directory.
    """   
    tests = [] 
    for root, dirnames, filenames in os.walk(tp.tests_to_run_dir):  # @UnusedVariable
        for filename in fnmatch.filter(filenames, 'test_*.py'):
            tests.append(os.path.join(root, filename))
    return tests

def get_rsult_jsons():
    """
    Gets the test results json files.
    
    @return: [list] list of result json file in the reports directory.
    """
    json_file_names = []
    os.chdir(tp.reports_dir + '/results')
    for f in glob.glob("test_*.json"):
        json_file_names.append(f)
    os.chdir(current_dir)
    return json_file_names

def get_test_doc_info():
    """
    Gets the test scripts doc info.
    
    @return: None
    """
    test_names = get_test_names()
    for name in test_names:
        print name
        with open(os.path.join(tp.project_dir, name)) as f:
            print f.read().split('"""')[1].split(';')[0]
            
def get_test_file_path_from_test_suite_file(test_name):
    """
    Gets the file path from test suite file
    
    @param test_name: 
            [string] test script name
    @return: [string] test script file path
    """
    f = open(os.path.join(tp.test_suite_path + "/test_suite.txt"), 'r')
    lines = f.readlines()
    for line in lines:      
        matchObj = re.search(test_name, line, re.M|re.I)
        if matchObj is not None:
            return line.strip()
    return None

def get_test_file_path(test_name):
    """
    Gets the test script file path from project directory.
    
    @param test_name: 
            [string] test script name
    @return: [string] test script file path
    """
    test_names = get_test_names()
    for test in test_names:
        matchObj = re.search(test_name, test, re.M|re.I)
        if matchObj is not None:
            return test
    return None
    

def json_update(test_suite=None):
    """
    Updates the json files in the report directory.
    
    @param test_suite: 
            [boolean] True then executes tests from test_suite.txt else executes tests from the given path.
    @return: None
    """
    json_files = get_rsult_jsons()    
    for filename in json_files:
        with open(os.path.join(tp.reports_dir, "results", filename), 'r+') as fd:
            test_file_name = filename.replace('.json', '.py')
            if test_suite is None:
                file_path = get_test_file_path(test_file_name)
            else:
                file_path = get_test_file_path_from_test_suite_file(test_file_name)
            if file_path is None:
                raise Exception("Test script {} doesn't exists.".format(test_file_name))
            with open(file_path) as f:
                jira_link = None
                doc_info = f.read().split('"""')[1].split('"""')[0]
                req_tc = doc_info.split(';')[0]
                if 'JIRA:' in doc_info:
                    jira_ticket = doc_info.split('JIRA:')[1].split(';')[0]
                    if 'jira.cirrus.com' in jira_ticket:
                        jira_link = jira_ticket
                    else:
                        jira_link = 'https://jira.cirrus.com/browse/' + jira_ticket
                                         
            json_data = json.load(fd)
            outcome = json_data['report']['tests'][0]['outcome']
            duration =  json_data['report']['summary']['duration']
            total = json_data['report']['summary']['num_tests']
                         
            if str(outcome) == "passed":
                failed = 0
                pending = 0
                passed = 1
                 
            elif str(outcome) == "failed":
                failed = 1
                pending = 0
                passed = 0
             
            elif str(outcome) == "skipped":
                pending = 1
                failed = 0
                passed = 0
             
             
            if passed is 1:
                json_data['examples'] = [{"full_description" : req_tc}]
            if failed is 1:
                exception_msg = json_data['report']['tests'][0]['call']['longrepr']
                json_data['examples'] = [{"full_description" : req_tc, "exception" : {"message" : exception_msg}}]
            if pending is 1:
                skp_info = json_data['report']['tests'][0]['setup']['longrepr'].split('Skipped:')[-1]
                if 'Not suitable with selected labels' in skp_info:
                    skp_info = '("Skipped:' + json_data['report']['tests'][0]['setup']['longrepr'].split('Skipped:')[-1]
                else:
                    skp_info = "('Skipped:" + json_data['report']['tests'][0]['setup']['longrepr'].split('Skipped:')[-1]
                exception_msg = skp_info
                json_data['examples'] = [{"full_description" : req_tc, "exception" : {"message" : exception_msg}}]
            if jira_link is not None:
                json_data['summary'] = {"duration" : duration, "example_count" : total, "failure_count" : failed, 
                                    "pending_count" : pending, "jira_link": jira_link}
            else:
                json_data['summary'] = {"duration" : duration, "example_count" : total, "failure_count" : failed, 
                                    "pending_count" : pending}
                    
            
            fd.seek(0)
            json.dump(json_data, fd, indent=4)
            fd.truncate()
            