import os
import argparse
import alibabacloud_oss_v2 as oss

# 创建命令行参数解析器，用于分片上传示例。
parser = argparse.ArgumentParser(description="multipart upload sample")

# 添加命令行参数 --region，表示存储空间所在的区域，必需参数
parser.add_argument('--region', help='The region in which the bucket is located.', required=True)

# 添加命令行参数 --bucket，表示存储空间的名称，必需参数
parser.add_argument('--bucket', help='The name of the bucket.', required=True)

# 添加命令行参数 --endpoint，表示其他服务可用来访问OSS的域名，非必需参数
parser.add_argument('--endpoint', help='The domain names that other services can use to access OSS')

# 添加命令行参数 --key，表示对象的名称，必需参数
parser.add_argument('--key', help='The name of the object.', required=True)

# 添加命令行参数 --file_path，表示要上传的文件路径，必需参数
parser.add_argument('--file_path', help='The path of Upload file.', required=True)


def main():
    # 解析命令行参数
    args = parser.parse_args()

    # 从环境变量中加载凭证信息，用于身份验证
    credentials_provider = oss.credentials.EnvironmentVariableCredentialsProvider()

    # 使用SDK的默认配置，并设置凭证提供者
    cfg = oss.config.load_default()
    cfg.credentials_provider = credentials_provider

    # 设置配置中的区域信息
    cfg.region = args.region

    # 如果提供了endpoint参数，则设置配置中的endpoint
    if args.endpoint is not None:
        cfg.endpoint = args.endpoint

    # 使用配置好的信息创建OSS客户端
    client = oss.Client(cfg)

    # 初始化分片上传请求，获取upload_id用于后续分片上传
    result = client.initiate_multipart_upload(oss.InitiateMultipartUploadRequest(
        bucket=args.bucket,
        key=args.key,
    ))

    # 定义每个分片的大小为5MB
    part_size = 5 * 1024 * 1024

    # 获取要上传文件的总大小
    data_size = os.path.getsize(args.file_path)

    # 初始化分片编号，从1开始
    part_number = 1

    # 存储每个分片上传的结果
    upload_parts = []

    # 打开文件以二进制模式读取
    with open(args.file_path, 'rb') as f:
        # 遍历文件，按照part_size分片上传
        for start in range(0, data_size, part_size):
            n = part_size
            if start + n > data_size:  # 处理最后一个分片可能小于part_size的情况
                n = data_size - start

            # 创建SectionReader来读取文件的特定部分
            reader = oss.io_utils.SectionReader(oss.io_utils.ReadAtReader(f), start, n)

            # 上传分片
            up_result = client.upload_part(oss.UploadPartRequest(
                bucket=args.bucket,
                key=args.key,
                upload_id=result.upload_id,
                part_number=part_number,
                body=reader
            ))

            # 打印每个分片上传的结果信息
            print(f'status code: {up_result.status_code},'
                  f' request id: {up_result.request_id},'
                  f' part number: {part_number},'
                  f' content md5: {up_result.content_md5},'
                  f' etag: {up_result.etag},'
                  f' hash crc64: {up_result.hash_crc64},'
                  )

            # 将分片上传结果保存到列表中
            upload_parts.append(oss.UploadPart(part_number=part_number, etag=up_result.etag))

            # 增加分片编号
            part_number += 1

    # 对上传的分片按照分片编号排序
    parts = sorted(upload_parts, key=lambda p: p.part_number)

    # 发送完成分片上传请求，合并所有分片为一个完整的对象
    result = client.complete_multipart_upload(oss.CompleteMultipartUploadRequest(
        bucket=args.bucket,
        key=args.key,
        upload_id=result.upload_id,
        complete_multipart_upload=oss.CompleteMultipartUpload(
            parts=parts
        )
    ))

    # 下面的代码是另一种方式，通过服务器端列出并合并所有分片数据为一个完整的对象
    # 这种方法适用于当您不确定所有分片是否都已成功上传时
    # Merge fragmented data into a complete Object through the server-side List method
    # result = client.complete_multipart_upload(oss.CompleteMultipartUploadRequest(
    #     bucket=args.bucket,
    #     key=args.key,
    #     upload_id=result.upload_id,
    #     complete_all='yes'
    # ))

    # 输出完成分片上传的结果信息
    print(f'status code: {result.status_code},'
          f' request id: {result.request_id},'
          f' bucket: {result.bucket},'
          f' key: {result.key},'
          f' location: {result.location},'
          f' etag: {result.etag},'
          f' encoding type: {result.encoding_type},'
          f' hash crc64: {result.hash_crc64},'
          f' version id: {result.version_id},'
    )

if __name__ == "__main__":
    main()  # 脚本入口，当文件被直接运行时调用main函数