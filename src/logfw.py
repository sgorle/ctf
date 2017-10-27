'''
Created on Jul 17, 2017

@author: sgorle
@summary: Logging implementation
'''
import logging
import os
import sys
from ctf.src.configure import Configure as conf

logger = logging.getLogger('test')
logger.setLevel(logging.DEBUG)


script = sys.argv[3].split("\\")[-1].split(".")[0]
if r'/' in script:
    script = script.split(r'/')[-1]

# Create log dir if not exists
log_dir = conf.property("log_path", "")
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

fh = logging.FileHandler(os.path.join(log_dir, script + ".log"), mode='w')
fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(module)s - %(levelname)s - %(message)s', datefmt="%Y-%m-%d %H:%M:%S")
ch.setFormatter(formatter)
fh.setFormatter(formatter)
# add the handlers to logger
logger.addHandler(ch)
logger.addHandler(fh)