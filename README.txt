图片分组压缩工具使用说明
====================================

本工具可将文件夹中的图片按指定数量分组压缩为ZIP文件。

使用方法：
1. 将本程序放在图片文件夹中，或指定图片文件夹路径
2. 打开命令提示符(cmd)
3. 运行程序并指定参数

基本命令：
  ImageGroupCompressor.exe "图片文件夹路径"

完整参数：
  ImageGroupCompressor.exe 文件夹路径 [选项]
  
选项:
  -s, --size   每组图片数量 (默认: 20)
  -o, --order  排序方式 (name/ctime/mtime/size/none) (默认: name)

示例：
1. 压缩当前文件夹图片（每组20张）：
   ImageGroupCompressor.exe .
   
2. 压缩D盘照片（每组10张，按修改时间排序）：
   ImageGroupCompressor.exe "D:\照片" -s 10 -o mtime

3. 压缩C盘图片（每组50张，按文件大小排序）：
   ImageGroupCompressor.exe "C:\图片文件夹" -s 50 -o size

注意事项：
- 确保文件夹路径正确
- 分组大小需大于0
- 程序会直接在图片文件夹中创建压缩包
- 支持格式：JPG, PNG, GIF, BMP, TIFF, WEBP
