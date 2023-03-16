from .models import Post, Category
from django.contrib.auth.models import User
import datetime
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


def send_email_7days():
    print('try_to_send_news')
    now = datetime.datetime.now() - datetime.timedelta(days=7)
    now_format = now.strftime("%Y-%m-%d %H:%M:%S")

    post_detail = {}
    posts = Post.objects.filter(date__gt=now_format).order_by('-date').values('title', 'date', 'pk', 'author_id')
    print(posts)
    for post in posts:
        email = User.objects.get(pk=post['author_id']).email
        print('EMAIL', email)
        post_info = {
            'title': post['title'],
            'link': post['pk'],
            'date': post['date'].strftime('%Y-%m-%d %H:%M'),
        }
        if email not in post_detail:
            post_detail[email] = []
        post_detail[email].append(post_info)

    send_to_list = post_detail.keys()
    subject = 'Новости за прошедшую неделю'
    for user_id, user in enumerate(list(send_to_list)):
        post_list_to_html = []
        for idx, post in enumerate(post_detail[user]):
            if len(post_detail[user]) > 1:
                if post['title'] != post_detail[user][idx-1]['title']:
                    post_list_to_html.append(post)
            else:
                post_list_to_html.append(post)

        user_email = [list(send_to_list)[user_id]]

        html_content = render_to_string(
            'mail/news_list.html',
            {
                'msg': post_list_to_html,
            }
        )

        msg_prop = EmailMultiAlternatives(
            subject=subject,
            body='Список новостей',
            from_email='help@psymphony.ru',
            to=user_email,
        )
        msg_prop.attach_alternative(html_content, "text/html")

        print(f'email sended to {user_email}')
        print(html_content)
        msg_prop.send()

