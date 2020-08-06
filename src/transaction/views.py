from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from finin_test.gmail_client import EmailFn
import re
from finin_test.utils import removeHtmlTag
from bs4 import BeautifulSoup


def test_view(request, *args, **kwargs):

    e_client = EmailFn()
    messages = e_client.send_email_test()

    data1 = []

    for x in messages:
        for key, value in x.items():
            if len(value) != 0:     
                for y in value:
                    context = {}
                    body = removeHtmlTag(request, y['body'])
                    y['body'] = body    

    data = {
        'data': messages
    }

    return JsonResponse(data)
