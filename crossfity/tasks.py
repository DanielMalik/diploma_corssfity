from celery.task import Task

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

class SendEmailTask(Task):

    def run(self, user, email, role):

        subject = 'Welcome %s' % role
        from_mail = 'djangocrossfitytest@gmail.com'
        to = str(email)
        html_content = render_to_string('crossfity/welcome_email.html', {'user': user, 'role': role})
        text_content = strip_tags(html_content)

        msg = EmailMultiAlternatives(subject, text_content, from_mail, [to,])
        msg.attach_alternative(html_content, 'text/html')
        msg.send()

        # send_mail(
        #     'MAIL TITLE',
        #     'MAIL CONTENT',
        #     'djangocrossfitytest@gmail.com',
        #     [user.email],
        #     fail_silently=False,
        # )


