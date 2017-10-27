'''
Created on Jun 28, 2017

@author: sgorle
@summary: zip APIs
'''
import os
import shutil

import test_properties as props

def create_zip():
    """
    Creates zip file
    
    @return: None
    """
    shutil.make_archive(os.path.join(props.project_dir, 'report'), 'zip', props.reports_dir)
    
def final_report_zip():
    """
    Creates final report zip archive.
    
    @return: None
    """
    shutil.make_archive(os.path.join(props.project_dir, props.report_name), 'zip', props.final_report_dir)