# tinypng
tinypng是一个图片压缩工具，底层使用 [tinypng](https://www.tinypng.com) 的服务。直接把图片文件或者文件夹拖动到窗口即可压缩，不受图片个数限制。
tinypng目前只支持3.x版本的python。只支持windows系统。

# 使用
## 1.tinypng依赖requests,pyyaml,ndg-httpsclient,pyopenssl,pyasn1,pyinstaller,使用前请自己安装这些库。

    pip3 install requests
    pip3 install pyyaml
    pip3 install ndg-httpsclient
    pip3 install pyopenssl
    pip3 install pyasn1
    pip3 install pyinstaller

## 2.复制库tkdnd2.9.2到python安装目录下的tcl目录。如：C:/Python310/tcl

# 直接运行：
    双击start.bat

# 构建可执行文件：
    双击build.bat