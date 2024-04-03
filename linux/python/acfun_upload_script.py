import subprocess
import glob
import os
import re
from acfun_upload import AcFun
acfun = AcFun()
acfun.login(username = "  ", password = "  ")
def extract_first_frame(input_video, output_image):
    # FFmpeg命令来提取第一帧
    ffmpeg_command = [
        'ffmpeg',
        '-i', input_video,       # 输入视频文件
        '-vframes', '1',         # 仅提取一帧
        '-f', 'image2',          # 输出格式为图片
        '-y',
        '-update',
        output_image            # 输出图片文件
    ]
    # 使用subprocess运行FFmpeg命令
    subprocess.run(ffmpeg_command)
f_path = input("输入文件路径:（如不输入默认为:/mnt/smbshare/1.mp4)")
if not f_path:
    f_path = '/mnt/smbshare/1.mp4'
f_name_temp = os.path.basename(f_path)
f_name_temp1 = re.sub("AC娘本体-","", f_name_temp)
f_new_name = re.sub(r'(\d{4})-(\d{2})-(\d{2})-(\d{2})-(\d{2})-(\d{2})-(.*)\.mp4', r'[AC娘录播]\7 \1\2\3直播录播', f_name_temp1)
f_title = input("请输入视频标题:（如不输入默认为录播投稿格式)")
if not f_title:
    f_title = f_new_name
f_channel_id = input("选择投稿分区:(默认为207，即虚拟偶像分区):")
if not f_channel_id:
    f_channel_id = "207"
extract_first_frame(f_path, 'output_frame.jpg')
f_cover = input("选择封面路径:如不输入默认截取视频的第一帧)")
if not f_cover:
    f_cover = './output_frame.jpg'
f_desc=input("输入视频介绍:(如不输入默认为视频标题)")
if not f_desc:
    f_desc = f_title
f_tags=input("输入视频标签:(默认为 AC娘录播)")
if not f_tags:
    f_tags = "AC娘录播"
f_creation_type=input("是否原创:(原创为 3, 默认为转载，即 1)")
if not f_creation_type:
    f_creation_type = "1"
f_originalLinkUrl=input("如果为转载，请输入原视频地址:(默认为 https://live.acfun.cn/live/23682490)")
if not f_originalLinkUrl:
    f_originalLinkUrl = "https://live.acfun.cn/live/23682490"
print("请检查配置是否正确:\n")
print('视频名称为', f_title, '\n视频地址为', f_path, '\n投稿分区为', f_channel_id, '\n视频介绍信息为', f_desc, '\n标签信息为', f_tags, '\n该视频为转载，原地址为', f_originalLinkUrl)
input("按任意键继续...")
acfun.create_douga(file_path=f_path, title=f_title, channel_id=f_channel_id, cover=f_cover, desc=f_desc, tags=f_tags, creation_type=f_creation_type, originalLinkUrl=f_originalLinkUrl)
