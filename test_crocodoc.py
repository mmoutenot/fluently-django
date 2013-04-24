import os
import sys
import time

import crocodoc
from crocodoc import CrocodocError

crocodoc.api_token = 'Tw6f4QKEneJ8qiHzCRL7bOlF'

"""
Example #1

Upload a file to Crocodoc. We're uploading Form W4 from the IRS by URL.
"""
print 'Example #1 - Upload Form W4 from the IRS by URL.'
form_w4_url = 'http://www.irs.gov/pub/irs-pdf/fw4.pdf'
sys.stdout.write('  Uploading... ')
uuid = None

try:
    uuid = crocodoc.document.upload(url=form_w4_url)
    print 'success :)'
    print '  UUID is ' + uuid
except CrocodocError as e:
    print 'failed :('
    print '  Error Code: ' + str(e.status_code)
    print '  Error Message: ' + e.error_message
