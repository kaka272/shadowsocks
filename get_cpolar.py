
import re
import requests

def extract_csrf_token(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        csrf_token_pattern = r'<input type="hidden" name="csrf_token" value="([^"]+)" />'
        matches = re.search(csrf_token_pattern, response.text)
        if matches:
            csrf_token = matches.group(1)
            return csrf_token
        else:
            return None
    except Exception as e:
        return None

login_url = 'https://dashboard.cpolar.com/login'
csrf_token = extract_csrf_token(login_url)
if csrf_token:
    print("CSRF 令牌:", csrf_token)
else:
    print("未找到 CSRF 令牌或发生错误")
