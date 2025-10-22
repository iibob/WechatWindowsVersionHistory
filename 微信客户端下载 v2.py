import requests
import os
import subprocess
import locale
import re
from pathlib import Path
import shutil
from send2trash import send2trash
import hashlib
import json
from time import sleep
from bs4 import BeautifulSoup


def get_wechat_download_url(page_url):
    """获取微信PC版下载按钮对应的URL"""
    try:
        # 发送请求获取网页内容
        response = requests.get(page_url, timeout=10)
        response.raise_for_status()  # 检查请求是否成功
        response.encoding = response.apparent_encoding  # 自动识别编码
        html = response.text

        # 解析HTML
        soup = BeautifulSoup(html, "html.parser")

        # 定位下载按钮并提取URL
        download_button = soup.find(
            "a",
            class_="download-button",
            id="downloadButton"
        )

        if download_button:
            download_url = download_button.get("href")
            return download_url if download_url else None
        else:
            print("未找到目标下载按钮")
            return None

    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        return None
    except Exception as e:
        print(f"处理过程出错: {e}")
        return None


def download_file(url, save_path):
    path = Path(save_path)
    if path.exists():
        print(f'{save_path} 已存在，正在删除')
        move_to_recycle_bin(save_path)

    print('文件下载中 ...')

    try:
        # 发送HTTP GET请求
        response = requests.get(url, stream=True)
        response.raise_for_status()  # 检查请求是否成功

        # 以二进制写入模式打开文件
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"文件已保存到: {save_path}")
        return True

    except requests.exceptions.RequestException as e:
        print(f"下载文件时出错: {e}")
        return False


def calculate_sha256(file_path):
    sha256_hash = hashlib.sha256()  # 创建 SHA256 哈希对象

    try:
        # 以二进制模式打开文件
        with open(file_path, "rb") as f:
            # 逐块读取文件内容并更新哈希值
            for chunk in iter(lambda: f.read(4096), b""):
                if not chunk:
                    break
                sha256_hash.update(chunk)

        sha256 = sha256_hash.hexdigest()
        # print(f"文件 '{file_path}' 的 SHA256 值为: {sha256}")
        return sha256
    except Exception as e:
        print(f"计算 SHA256 时出错: {e}")
        return None


def compare_hash_values(json_path, target_hash):
    path = Path(json_path)
    if path.exists():
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            json_data = data
        except Exception as e:
            print(f"加载 JSON 文件时出错: {e}")
            return False

        # 遍历 JSON 数据
        for file_name, hash_value in json_data.items():
            # print(f"文件: {file_name}, 哈希值: {hash_value}")
            if hash_value == target_hash:
                # print(f"匹配成功！文件 '{file_name}' 的哈希值与目标值一致。")
                print(f'已存在相同版本安装包：{file_name}')
                print('任务完成')
                move_to_recycle_bin(WeChat_path)
                return False

        return True

    else:
        print(f'{json_path} 文件不存在')
        return True


def save_to_json(file_name, sha256_hash, json_path):
    data = {}

    # 如果 JSON 文件已存在，加载现有数据
    if os.path.exists(json_path):
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            print(f"加载 JSON 文件时出错: {e}")
            return

    # 更新数据
    data[file_name] = sha256_hash

    # 保存数据到 JSON 文件
    try:
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"数据已保存到 '{json_path}'。")
    except Exception as e:
        print(f"保存 JSON 文件时出错: {e}")


def get_the_content_of_archive_files(zip_path, source_file):
    """获取压缩包的第一层级内容"""
    try:
        # 调用 7z 命令行工具列出压缩包内容
        result = subprocess.run(
            [zip_path, 'l', source_file],  # 7z l 是列出压缩包内容的命令
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if result.returncode == 0:
            # 解析输出内容，提取第一层级内容
            lines = result.stdout.splitlines()
            first_level_contents = []
            start_parsing = False  # 标志是否开始解析文件列表

            for line in lines:
                # 找到文件列表的开始行
                if line.startswith("------------------- ----- ------------ ------------  ------------------------"):
                    start_parsing = True
                    continue

                # 找到文件列表的结束行
                if start_parsing and line.startswith("------------------- ----- ------------ ------------  ------------------------"):
                    break

                # 解析文件列表
                if start_parsing and line.strip():
                    parts = line.split()
                    # 获取文件名（最后一列是文件名）
                    file_name = parts[-1]
                    # 只保留第一层级内容（不包含子目录）
                    if '/' not in file_name and '\\' not in file_name:
                        first_level_contents.append(file_name)
                    else:
                        # 如果是子目录，提取第一层级的目录名
                        first_level_dir = file_name.split('\\')[0] if '\\' in file_name else file_name.split('/')[0]
                        if first_level_dir not in first_level_contents:
                            first_level_contents.append(first_level_dir)
            return first_level_contents
        else:
            print(f"错误: {result.stderr}")
            return None
    except Exception as e:
        print(f"调用 7z 命令行工具失败: {e}")
        return None


def extract_file_from_archive(zip_path, archive_path, file_name, output_dir):
    """从压缩包中提取指定文件到输出目录"""
    try:
        # 调用 7z 命令行工具提取文件
        result = subprocess.run(
            [zip_path, 'e', archive_path, file_name, f'-o{output_dir}'],  # 7z e 是提取文件的命令
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if result.returncode == 0:
            return True
        else:
            print(f"错误: {result.stderr}")
            return False
    except Exception as e:
        print(f"调用 7z 命令行工具失败: {e}")
        return False


def unzip_files(zip_path, source_file, output_dir):
    system_encoding = locale.getpreferredencoding()

    # 构建 7-Zip 命令
    command = [
        zip_path,
        "x",  # 解压命令
        source_file,  # 源文件
        f"-o{output_dir}",  # 输出目录
        "-y"  # 自动确认覆盖
    ]

    # 执行 7-Zip 命令
    try:
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("解压成功！")
        # print(result.stdout.decode(system_encoding, errors='replace'))
        return True
    except subprocess.CalledProcessError as e:
        print("解压失败！")
        print(f"错误信息: {e.stderr.decode(system_encoding, errors='replace')}")
        return False


def find_version_in_dir(first_level_contents):
    # 正则表达式匹配版本号（如 4.0.2.28 或 [4.0.2.28]）
    version_pattern = re.compile(r'^\[?(\d+(\.\d+)+)\]?$')

    for i in first_level_contents:
        match = version_pattern.match(i)
        if match:
            print(f"找到版本号文件夹: {i}")
            return match.group(1)  # 返回版本号

    return None


def update_filename_with_version(WeChat_path, version):
    # 获取文件所在的目录和文件的基本名称（不包括扩展名）
    directory = os.path.dirname(WeChat_path)
    base_name = os.path.basename(WeChat_path)
    file_name, file_extension = os.path.splitext(base_name)

    # 构建新的文件名
    new_file_name = f"{file_name}_{version}{file_extension}"
    new_WeChat_path = os.path.join(directory, new_file_name)

    path = Path(new_WeChat_path)
    if path.exists():
        print(f"文件 '{new_file_name}' 已存在。")
        move_to_recycle_bin(WeChat_path)

    else:
        # print(f"文件 '{new_file_name}' 不存在。")
        shutil.move(WeChat_path, new_WeChat_path)     # 重命名文件
        print('安装包文件已添加版本号')

    return f"{file_name}_{version}"


def move_to_recycle_bin(path):
    path = os.path.normpath(path)
    if os.path.exists(path):
        try:
            send2trash(path)
            print(f"已成功将 '{path}' 移动到回收站。")
        except Exception as e:
            print(f"移动 '{path}' 到回收站时出错: {e}")
    else:
        print(f"路径 '{path}' 不存在，无需移动。")


def find_version_and_save_json(contents, sha256_value):
    version = find_version_in_dir(contents)
    if version:
        file_name = update_filename_with_version(WeChat_path, version)
        save_to_json(file_name, sha256_value, json_path)
        return version
    return None


if __name__ == "__main__":
    page_url = "https://pc.weixin.qq.com/"
    WeChat_path = r"E:\WeChat\WeChatWin.exe"
    zip_path = r"D:\APP\7-Zip\7z.exe"
    output_dir = r"E:\WeChat\extracted"
    json_path = r"E:\WeChat\version.json"

    # 下载
    download_url = get_wechat_download_url(page_url)
    if download_url:
        print(f"最新版下载地址：\n{download_url}")
        result = download_file(download_url, WeChat_path)
        if result:
            sleep(1)
            sha256_value = calculate_sha256(WeChat_path)
            if sha256_value:
                result = compare_hash_values(json_path, sha256_value)
                if result:
                    first_level_contents = get_the_content_of_archive_files(zip_path, WeChat_path)
                    if first_level_contents:
                        version = find_version_and_save_json(first_level_contents, sha256_value)
                        if version:
                            print('任务完成')
                        else:
                            # 安装包中版本号文件夹位置调整，需要提取安装包中的文件进行查找
                            install_file = 'install.7z'
                            if install_file in first_level_contents:
                                print(f"找到 {install_file}，继续查找版本号...")
                                if extract_file_from_archive(zip_path, WeChat_path, install_file, output_dir):
                                    sleep(1)
                                    install_file_path = os.path.join(output_dir, install_file)
                                    if os.path.exists(install_file_path):
                                        install_contents = get_the_content_of_archive_files(zip_path, install_file_path)
                                        if install_contents:
                                            version = find_version_and_save_json(install_contents, sha256_value)
                                            if version:
                                                print('任务完成')
                                    else:
                                        print(f"安装包中未提取到 {install_file}")

                                # 将解压后的文件夹移动到回收站
                                move_to_recycle_bin(output_dir)
