# 安装
# pip install -U huggingface_hub

from huggingface_hub import snapshot_download

# 如需代理：
import os
# os.environ["HTTP_PROXY"] = "http://127.0.0.1:7890"
# os.environ["HTTPS_PROXY"] = "http://127.0.0.1:7890"

# 如需镜像（任选其一可用镜像域名）
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"

# 拉取仓库（包含 LFS 大文件，会自动断点续传）
snapshot_download(repo_id="FireRedTeam/FireRedTTS2", local_dir="/Users/lizea/PycharmProjects/model/", local_dir_use_symlinks=False)