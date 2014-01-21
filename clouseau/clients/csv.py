from abstract import AbstractClient
from jinja2 import Template, Environment, PackageLoader
from colors import *
import re
import subprocess
import sys
import os

class CSVClient(AbstractClient):
    """
    CSV-line client for Clouseau
    """

    def __init__(self):
        pass

    def render(self, terms, data):
        """
         
        """
        env = Environment(loader=PackageLoader('clouseau', 'templates'))
        template = env.get_template('csv.html')
        data_to_render = template.render(data=data)

        #temp to see output on cmd line
        try:
            pager = subprocess.Popen(['less', '-F', '-R', '-S', '-X', '-K'], stdin=subprocess.PIPE, stdout=sys.stdout)
            lines = data_to_render.split('\n')
            for line in lines:
                pager.stdin.write( line.encode('utf-8') + '\n' )
            pager.stdin.close()
            pager.wait()
        except KeyboardInterrupt:
            pass




