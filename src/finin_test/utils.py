import re

def removeHtmlTag(request, text):
    clean = re.compile(r'<[^>]+>')
    body = re.sub(clean, ' ', text)
    body = re.split(r'[\r\n=]', body)
    body = ''.join(body)

    return body