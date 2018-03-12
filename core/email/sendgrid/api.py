import sendgrid
from django.conf import settings


def send_email(from_addr, to_addr, subject, content, content_type='text/html'):
    sg = sendgrid.SendGridAPIClient(apikey=settings.SENDGRID_API_KEY)
    data = {
        "personalizations": [
            {
                "to": [
                    {
                        "email": to_addr
                    }
                ],
                "subject": subject
            }
        ],
        "from": {
            "email": from_addr
        },
        "content": [
            {
                "type": content_type,
                "value": content
            }
        ]
    }
    response = sg.client.mail.send.post(request_body=data)
    print(response.status_code)
    print(response.body)
    print(response.headers)
