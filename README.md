# 收集 Windows 版微信 4.0 以后的历史版本
- 每个工作日手动执行一次版本收集操作 😄，若发现新版本，会通过 Releases 功能进行发布。
- 下载地址：https://pc.weixin.qq.com

# 运行
### 下载微信客户端 v2.py

- 电脑需要安装 7-Zip
- 修改以下代码中的路径：
  - `WeChat_path`：微信客户端保存路径
  - `zip_path`：7-Zip 程序路径
  - `output_dir`：可能用到的临时解压目录路径
  - `json_path`：历史版本信息记录文件路径

```
WeChat_path = r"E:\WeChat\WeChatWin.exe"
zip_path = r"D:\APP\7-Zip\7z.exe"
output_dir = r"E:\WeChat\extracted"
json_path = r"E:\WeChat\version.json"
```

### 发布微信安装包.py
  - `token_path`：存放经过 Base64 编码的 GitHub 访问令牌的文件

```
token_path = rf"{directory}\token.txt"
```

# 备注
客户端更新迭代过程中，安装包文件调整过版本号文件夹的位置。


![image](https://github.com/user-attachments/assets/e2e08ee6-0f87-444c-9b33-9763d2f17ae5)

在 4.0 系列版本中，大概从 v4.0.3.19 版本起，产品脱离测试阶段，转为正式版。


> [!TIP]
> 手动收集可能存在遗漏，若需相对全面的历史版本安装包，可前往[自动收集](https://github.com/cscnk52/wechat-windows-versions)查看，该仓库每小时收集一次。 
