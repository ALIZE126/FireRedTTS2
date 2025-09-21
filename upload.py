import os
import alibabacloud_oss_v2 as oss

# ====== 配置你的 bucket 信息 ======
region = "cn-beijing"                   # Bucket 区域
bucket = "fire-red-model"               # Bucket 名称
endpoint = "https://oss-cn-beijing.aliyuncs.com"  # Endpoint
local_folder = "/Users/lizea/PycharmProjects/model/FireRedTeam/FireRedTTS2"  # 本地文件夹路径
oss_prefix = "FireRedTTS2"  # OSS 上的前缀目录（可自行调整）


# ====== 构建客户端 ======
credentials_provider = oss.credentials.EnvironmentVariableCredentialsProvider()
cfg = oss.config.load_default()
cfg.credentials_provider = credentials_provider
cfg.region = region
cfg.endpoint = endpoint
client = oss.Client(cfg)

# ====== 上传函数（对单个文件做分片上传） ======
def multipart_upload(client, bucket, local_file_path, oss_key, part_size=5*1024*1024):
    """单文件分片上传"""
    print(f"开始上传: {local_file_path} → oss://{bucket}/{oss_key}")

    init = client.initiate_multipart_upload(
        oss.InitiateMultipartUploadRequest(bucket=bucket, key=oss_key)
    )
    size = os.path.getsize(local_file_path)
    parts_meta = []
    pn = 1

    with open(local_file_path, "rb") as f:
        for start in range(0, size, part_size):
            n = min(part_size, size - start)
            reader = oss.io_utils.SectionReader(oss.io_utils.ReadAtReader(f), start, n)
            up = client.upload_part(oss.UploadPartRequest(
                bucket=bucket, key=oss_key, upload_id=init.upload_id, part_number=pn, body=reader
            ))
            print(f"  part {pn} ok, etag={up.etag}")
            parts_meta.append(oss.UploadPart(part_number=pn, etag=up.etag))
            pn += 1

    parts_meta.sort(key=lambda p: p.part_number)
    done = client.complete_multipart_upload(
        oss.CompleteMultipartUploadRequest(
            bucket=bucket, key=oss_key, upload_id=init.upload_id,
            complete_multipart_upload=oss.CompleteMultipartUpload(parts=parts_meta)
        )
    )
    print(f"✅ 完成: {oss_key} (etag={done.etag})\n")

# ====== 遍历文件夹并上传 ======
for root, dirs, files in os.walk(local_folder):
    for filename in files:
        local_file = os.path.join(root, filename)

        # 计算相对路径（保持文件夹层级结构）
        rel_path = os.path.relpath(local_file, local_folder)
        # 拼 OSS key（oss_prefix/相对路径）
        oss_key = f"{oss_prefix}/{rel_path.replace(os.sep, '/')}"  # OSS 使用正斜杠

        multipart_upload(client, bucket, local_file, oss_key)