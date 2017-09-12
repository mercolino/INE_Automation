import sys
import logging

logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/ine_automation/")

from INE_Automation import app as application
application.secret_key = 'kdfjkJHGJFSDjfhglasdjhg'