from celery.task import Task

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth.models import User

class SendEmailTask(Task):

    def run(self, user_username, role):
        user = User.objects.get(username=user_username)
        subject = 'Welcome %s' % role
        from_mail = 'djangocrossfitytest@gmail.com'
        to = user.email
        html_content = render_to_string('crossfity/welcome_email.html', {'user': user.username, 'role': role})
        text_content = strip_tags(html_content)

        msg = EmailMultiAlternatives(subject, text_content, from_mail, [to])
        msg.attach_alternative(html_content, 'text/html')
        msg.send()
