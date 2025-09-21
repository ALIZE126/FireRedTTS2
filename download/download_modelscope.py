# 安装 ModelScope
# pip install modelscope

from modelscope.hub.snapshot_download import snapshot_download
import os

# 如需代理：
# os.environ["HTTP_PROXY"] = "http://127.0.0.1:7890"
# os.environ["HTTPS_PROXY"] = "http://127.0.0.1:7890"

# 如果想切换到 ModelScope 的镜像，可以在这里设置：
# os.environ["MODELSCOPE_HUB"] = "https://modelscope.cn"  # 这是默认值，也可以改成你自己的镜像

# 下载模型仓库到指定目录
snapshot_download(
    model_id="FireRedTeam/FireRedTTS2",           # 模型 ID
    cache_dir="/Users/lizea/PycharmProjects/model",  # 保存目录（与 HF local_dir 类似）
    revision=None,                               # 可指定版本，如 "v1.0.0"
    allow_file_pattern=None                      # 可指定下载哪些文件，None 表示全部下载
)