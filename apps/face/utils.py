mandrill_api_key = "qIjK_MqTNHaoGT5kiIhIJg"

"""
*sends email over mandrill
*template_name = immutable slug representing a template
*template_content = list of dictionaries with name and content representing an editable field in the template
*tags = string representing the topic (for tracking on mandrill
"""
def send_email_using_template(template_name, template_content, recipient_email, recipient_name, tag):
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
      "important": false,
      "track_opens": null,
      "track_clicks": null,
      "auto_text": null,
      "auto_html": null,
      "inline_css": null,
      "url_strip_qs": null,
      "preserve_recipients": null,
      "tracking_domain": null,
      "signing_domain": null,
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
      "attachments": null,
      "images": null,
    },
    "async": false
  }

