'''
Created on Jun 27, 2017

@author: sgorle
@summary: Email sending with the test report attachment utility.
'''
import email
import mimetypes
import os.path
import smtplib
from email.encoders import encode_base64
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.MIMEMultipart import MIMEMultipart
from email import MIMEAudio
from email.mime.image import MIMEImage

import test_properties as props
 
 
def email_report(subject, from_email, to_email_list, text_message = '', html_message = ''):
    """
    Sending email to the recipients.
    
    @param subject: 
            [string] mail subject
    @param from_email: 
            [string] from email address
    @param to_email_list: 
            [list] to email address list
    @param text_message: 
            [string] text mesage to send
    @param html_message: 
            [string] email body in html
    @return: None
    """
    COMMASPACE = ', '
      
    # Create the container (outer) email message.
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = COMMASPACE.join(to_email_list)
    text = text_message
    html = """\
    <html>
      <head></head>
      <body>
        %s
      </body>
    </html>
    """ % (html_message)
      
    body = MIMEMultipart('alternative')
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')
    body.attach(part1)
    body.attach(part2)
    msg.attach(body)
    
    if os.path.exists(props.project_dir + r"/" + props.report_name + '.zip') is not True:
        raise("{0}.zip file doesn't existed.".format(props.report_name))
                
    attach = _get_attachment(props.project_dir + r"/" + props.report_name + '.zip', props.report_name + '.zip')
    msg.attach(attach)  
      
    # Send the email via our own SMTP server.
    s = smtplib.SMTP()
    s.connect(props.mail_server)
    s.sendmail(from_email, to_email_list, msg.as_string())
    s.close()
    print "Report was sent to the recipients successfully"
  

def _get_attachment(path, filename):
    """
    Set and get the attachment to the email.
    
    @param path: 
            [string] file path
    @param filename: 
            [string] file name to be attached.
    @return: [MIMEText | MIMEImage | MIMEAudio | MIMEBase | string] returns the attachment.
    """
    ctype, encoding = mimetypes.guess_type(path)
    if ctype is None or encoding is not None:
        ctype = 'application/octet-stream'
    maintype, subtype = ctype.split('/', 1)
    fp = open(path, 'rb')
    if maintype == 'text':
        attach = MIMEText(fp.read(),_subtype=subtype)
    elif maintype == 'message':
        attach = email.message_from_file(fp)
    elif maintype == 'image':
        attach = MIMEImage(fp.read(),_subtype=subtype)
    elif maintype == 'audio':
        attach = MIMEAudio(fp.read(),_subtype=subtype)
    else:
        attach = MIMEBase(maintype, subtype)
        attach.set_payload(fp.read())
        encode_base64(attach)
    fp.close  #pylint: disable=pointless-statement
    attach.add_header('Content-Disposition', 'attachment', filename=filename)
    return attach

   
# if __name__ == '__main__':
#     email_report(props.subject, props.sender, props.to, html_message=props.email_body)
