mandrill_api_key = "qIjK_MqTNHaoGT5kiIhIJg"

"""
*sends email over mandrill
*template_name = immutable slug representing a template
*template_content = list of dictionaries with name and content representing an editable field in the template
*tags = string representing the topic (for tracking on mandrill
"""
def email_template(template_name, template_content, recipient_email, recipient_name, tag):
  request = {
    "key": mandrill_api_key,
    "template_name": template_name,
    "template_content": template_content,
    "message": {
      "from_email": "jack@fluentlynow.com",
      "from_name": "Fluently",
      "to": [
        {
          "email": recipient_email,
          "name": recipient_name
        }
      ],
      "headers": {
        "Reply-To": "jack@fluentlynow.com"
      },
      "important": False,
      "track_opens": None,
      "track_clicks": None,
      "auto_text": None,
      "auto_html": None,
      "inline_css": None,
      "url_strip_qs": None,
      "preserve_recipients": None,
      "tracking_domain": None,
      "signing_domain": None,
      "tags": [
        tag
      ],
      "metadata": {
        "website": "www.fluentlynow.com"
      },
      "recipient_metadata": [
        {
          "rcpt": recipient_email,
        }
      ],
      "attachments": None,
      "images": None,
    },
    "async": False
  }

