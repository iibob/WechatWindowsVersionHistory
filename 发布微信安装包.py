import requests
from requests.auth import HTTPBasicAuth
import datetime
import base64
import json
import os


def create_release_and_upload_file(file_path, version, release_title, sha256):
    """创建一个新的 GitHub Release 并上传文件。
    :param file_path: 要上传的微信安装包文件路径
    :param version: 微信版本号
    :param release_title: Release 的标题
    :param sha256: 安装包文件的 SHA256
    """
    creation_time = os.path.getctime(file_path)
    readable_time = datetime.datetime.fromtimestamp(creation_time).strftime('%Y-%m-%d %H:%M:%S')
    release_body = f"""版本：v{version}\n下载时间：{readable_time}\nSHA256：{sha256}"""

    # 创建新发行版本的 URL
    release_url = f'https://api.github.com/repos/{username}/{repo_name}/releases'

    # 数据准备
    release_data = {
        'tag_name': f"v{version}",
        'name': release_title,
        'body': release_body,
        'draft': False,
        'prerelease': False
    }

    # 发送 POST 请求创建新的发行版本
    response = requests.post(release_url, json=release_data, auth=HTTPBasicAuth(username, token))

    if response.status_code == 201:
        print(f'成功创建发布 {release_title}，标签为 v{version}')
        # release_id = response.json()['id']
    else:
        print(f'创建发布失败。状态码: {response.status_code}, 响应: {response.text}')
        return

    print('正在上传安装包 ...')
    # 获取要上传文件的内容
    with open(file_path, 'rb') as f:
        content = f.read()

    # 上载资产到发行版的 URL
    upload_url = response.json()['upload_url'].replace('{?name,label}', '')

    # 设置请求头
    headers = {
        'Content-Type': 'application/octet-stream',
        'Authorization': f'token {token}'
    }

    # 发送 POST 请求上传文件到 Release
    upload_response = requests.post(
        f'{upload_url}?name=WeChatWin_{version}.exe',
        headers=headers,
        data=content
    )

    if upload_response.status_code == 201:
        print(f'成功上传 {file_path} 到发布 {release_title}')
    else:
        print(f'上传 {file_path} 失败。状态码: {upload_response.status_code}, 响应: {upload_response.text}')


def get_last_key_value_pair(json_file_path):
    """读取指定路径的 JSON 文件并返回最后一个键值对。
    :param json_file_path: JSON 文件的路径
    """
    try:
        with open(json_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # 获取最后一个键值对
        last_key = list(data.keys())[-1]
        last_value = data[last_key]

        return last_key, last_value

    except Exception as e:
        print(f"发生错误: {e}")
        return None, None


def read_and_clean_txt(file_path):
    """打开指定路径的 TXT 文件，获取文件中的文本内容
    :param file_path: 文件的路径
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return content.strip()

    except Exception as e:
        print(f"发生错误: {e}")
        return None


def base64_operation(input_string, is_encrypt=True):
    """Base64 编码和解码
    :param is_encrypt: True 加密；False 解密
    """
    if is_encrypt:
        result = base64.b64encode(input_string.encode('utf-8')).decode('utf-8')
    else:
        try:
            result = base64.b64decode(input_string.encode('utf-8')).decode('utf-8')
        except:
            result = None
    return result


if __name__ == "__main__":
    directory = r"E:\WeChat"
    json_path = rf"{directory}\version.json"
    token_path = rf"{directory}\token.txt"      # GitHub 访问令牌
    username = 'iibob'                          # GitHub 用户名
    repo_name = 'WechatWindowsVersionHistory'   # 仓库名称

    last_key, last_value = get_last_key_value_pair(json_path)

    if last_key is not None and last_value is not None:
        version = last_key.split("_")[1]
        WeChat_path = f"{directory}\WeChatWin_{version}.exe"

        base64_token = read_and_clean_txt(token_path)
        if base64_token is not None:
            token = base64_operation(base64_token, False)
            if os.path.isfile(WeChat_path):
                create_release_and_upload_file(file_path=WeChat_path, version=version, release_title=last_key, sha256=last_value)
            else:
                print(f'微信安装包文件路径错误')
    else:
        print('在 JSON 文件中获取内容出错')
