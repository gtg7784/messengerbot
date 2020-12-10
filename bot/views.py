import os, json
from django.http import HttpResponse
from django.shortcuts import render
from django.core.mail import send_mail
from django.http.response import BadHeaderError
from django.core.exceptions import ImproperlyConfigured
from django.conf import settings
from .utils import vertify_token, send_message, choice_message
from .models import MailList

secret_file = os.path.join(settings.BASE_DIR, 'secrets.json')

with open(secret_file) as f:
    secrets = json.loads(f.read())

def get_secret(setting, secrets=secrets):
    try:
        return secrets[setting]
    except KeyError:
        error_msg = "Set the {} environment variable".format(setting)
        raise ImproperlyConfigured(error_msg)

VERIFY_TOKEN = get_secret("VERIFY_TOKEN")
PAGE_ACCESS_TOKEN = get_secret("ACCESS_TOKEN")

SCHOOL_NAME = "선린인터넷고등학교"

def chat(request):
  if request.method == 'GET':
    token_sent = request.GET.get('hub.verify_token', '')
    return vertify_token(token_sent)
  else:
    output = request.get_json()
    for event in output['entry']:
      messaging = event['messaging']
      for message in messaging:
        if message.get('message'):
          recipient_id = message['sender']['id']
          if message['message'].get('text'):
            text = message['message'].get('text')
            response_sent_text = choice_message(text)
            send_message(recipient_id, response_sent_text)
          if message['message'].get('attachments'):
            response_sent_nontext = "attach"
            send_message(recipient_id, response_sent_nontext)
  return HttpResponse("Message Processed")

def index(request):
  if request.method == "POST":
    email = request.POST.get("email", "")
    try:
      send_mail(
      '선린인터넷고등학교 메신저 봇, 선린봇에 당신을 초대합니다!',
      '안녕하세요, 선린인터넷고등학교 메신저 봇에 관심을 가져 주셔서 감사합니다.\n페이스북 페이지 링크는 다음과 같습니다.\n\nhttps://fb.me/sunrinbot\n많은 사랑 부탁드립니다. 감사합니다.',
      to=[email],
      fail_silently=False,)
      mail = MailList(sender="tae.gun7784@gmail.com", receiver=email)
      mail.save()
    except BadHeaderError:
      return HttpResponse('Invalid header found.')
    
  return render(request, "index.html", {})
