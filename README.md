# 收集 Windows 版微信 4.0 以后的历史版本
- 每个工作日手动执行一次版本收集操作 😄，若发现新版本，将使用 Releases 发布。
- 下载地址：https://pc.weixin.qq.com

# 运行
### 微信安装包下载 v2.py

- 前置要求：电脑需预先安装 7-Zip 软件
- 路径修改：请按实际调整以下路径
  - `WeChat_path`：保存微信安装包的路径
  - `zip_path`：7-Zip 程序路径
  - `output_dir`：解压操作所需的临时目录路径
  - `json_path`：记录历史版本信息的文件路径

```
WeChat_path = r"E:\WeChat\WeChatWin.exe"
zip_path = r"D:\APP\7-Zip\7z.exe"
output_dir = r"E:\WeChat\extracted"
json_path = r"E:\WeChat\version.json"
```

### 微信安装包发布.py
  - `token_path`：存放经过 Base64 编码的 GitHub 访问令牌的文件

```
token_path = rf"{directory}\token.txt"
```

# 备注
- 客户端更新迭代过程中，安装包文件调整过版本号文件夹的位置：


  ![image](https://github.com/user-attachments/assets/e2e08ee6-0f87-444c-9b33-9763d2f17ae5)

- 在 4.0 系列版本中，大概从 v4.0.3.19 版本起，产品脱离测试阶段，转为正式版。

- 微信官方于 2025-10-21 调整最新版安装包下载地址，地址中新增版本号标识。

---

> [!TIP]
> 手动收集可能存在遗漏，若需相对全面的历史版本安装包，可前往[自动收集](https://github.com/cscnk52/wechat-windows-versions)查看，该仓库每小时收集一次。 
