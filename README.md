# 收集 Windows 版微信历史版本
- 每个工作日手动运行一次 😄，发现新版本后通过 Releases 发布。
- 仅包含 4.0 以后的版本
- 下载地址：https://pc.weixin.qq.com

# 运行
- 电脑需要安装 7-Zip
- 修改以下代码中的路径：
  - `WeChat_path`：微信客户端下载路径
  - `zip_path`：7-Zip 程序路径
  - `output_dir`：可能用到的临时解压目录
  - `json_path`：历史版本信息记录文件路径

```
WeChat_path = r"E:\WeChat\WeChatWin.exe"
zip_path = r"D:\APP\7-Zip\7z.exe"
output_dir = r"E:\WeChat\extracted"
json_path = r"E:\WeChat\version.json"
```

# 备注
客户端更新迭代过程中，安装包文件调整过版本号文件夹的位置。


![image](https://github.com/user-attachments/assets/e2e08ee6-0f87-444c-9b33-9763d2f17ae5)
