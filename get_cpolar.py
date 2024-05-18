import re
import requests
import sys

def extract_csrf_token(url):
    try:
        # 发送 GET 请求获取网页内容
        response = requests.get(url)
        response.raise_for_status()

        # 使用正则表达式查找 CSRF 令牌
        csrf_token_pattern = r'<input type="hidden" name="csrf_token" value="([^"]+)" />'
        matches = re.search(csrf_token_pattern, response.text)

        # 获取 CSRF 令牌的值
        if matches:
            csrf_token = matches.group(1)
            return csrf_token
        else:
            return None
    except Exception as e:
        print("提取 CSRF 令牌时出错:", e)
        return None

def login(username, password, url):
    try:
        # 获取登录页面的 CSRF 令牌
        csrf_token = extract_csrf_token(url)
        if not csrf_token:
            print("无法获取 CSRF 令牌")
            return

        # 构造登录请求的数据
        login_data = {
            'login': username,
            'password': password,
            'csrf_token': csrf_token
        }

        # 创建会话对象
        session = requests.Session()

        # 发送 POST 请求进行登录，并保存会话信息
        response = session.post(url, data=login_data)
        response.raise_for_status()

        return session  # 返回保存登录会话信息的对象
    except Exception as e:
        print("登录时出错:", e)
        return None

def get_content_after_login(session, url):
    try:
        # 使用保存的会话信息发送 GET 请求获取内容
        response = session.get(url)
        response.raise_for_status()

        # 使用正则表达式匹配特定格式的文本
        regex_pattern = r'tcp://([^:]+):([0-9]+)'
        matches = re.findall(regex_pattern, response.text)

        # 返回匹配到的内容列表
        return matches
    except Exception as e:
        print("获取内容时出错:", e)
        return None

def save_content_to_file(content_list, filename):
    try:
        script_dir = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(script_dir, filename)
        with open(file_path, 'w', encoding='utf-8') as f:
            for item in content_list:
                f.write(f"{item[0]}:{item[1]}\n")
        print("内容已保存到文件:", filename)
    except Exception as e:
        print("保存内容时出错:", e)

def get_first_line_content(filename):
    try:
        script_dir = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(script_dir, filename)
        with open(file_path, 'r', encoding='utf-8') as f:
            first_line = f.readline().strip()
            return first_line.split(':')
    except Exception as e:
        print("读取文件时出错:", e)
        return None

def main():
    login_url = "https://dashboard.cpolar.com/login"
    other_url = "https://dashboard.cpolar.com/status"
    
    if len(sys.argv) > 1:
        if sys.argv[1] == '2':
            if len(sys.argv) > 2:
                choice = sys.argv[2]
                if choice == '1':
                    print(get_first_line_content('output.txt')[0])
                elif choice == '2':
                    print(get_first_line_content('output.txt')[1])
                else:
                    print("无效的选项")
            else:
                print("缺少参数")
        else:
            print("无效的选项")
    else:
        while True:
            choice = input("请输入数字 1（获取网页内容并保存）, 2（显示上次获取的内容）, 或 3（退出）: ")
            
            if choice == '1':
                username = input("请输入用户名: ")
                password = input("请输入密码: ")

                # 登录
                session = login(username, password, login_url)
                if session:
                    # 登录成功后获取其他页面的内容
                    content_list = get_content_after_login(session, other_url)
                    if content_list:
                        # 保存内容到文件
                        save_content_to_file(content_list, 'output.txt')
                else:
                    print("登录失败或发生错误")
            elif choice == '2':
                try:
                    script_dir = os.path.dirname(os.path.realpath(__file__))
                    file_path = os.path.join(script_dir, 'output.txt')
                    with open(file_path, 'r', encoding='utf-8') as f:
                        print("上次获取的内容:")
                        print(f.read())
                except FileNotFoundError:
                    print("文件不存在，请先执行选项1获取内容。")
            elif choice == '3':
                print("已退出程序。")
                break
            else:
                print("无效的选项，请重新输入。")

if __name__ == "__main__":
    main()
