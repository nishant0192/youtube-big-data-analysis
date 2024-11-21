from hdfs import InsecureClient

hdfs_client = InsecureClient("http://localhost:9870", user="root")

def upload_to_hdfs(file_path, hdfs_path):
    hdfs_client.upload(hdfs_path, file_path)

def download_from_hdfs(hdfs_path, local_path):
    hdfs_client.download(hdfs_path, local_path)
