from celery import shared_task
from django.core.mail import send_mail


@shared_task
def background_send_email(email_list, model, version):
    subject = 'Robot is available'
    message = f'''
            Добрый день!
            Недавно вы интересовались нашим роботом модели {model}, версии {version}. 
            Этот робот теперь в наличии. Если вам подходит этот вариант - пожалуйста, свяжитесь с нами
        '''
    mail_sent = send_mail(subject,
                          message,
                          'yashenkov.q@gmail.com',
                          email_list)
    return mail_sent
            