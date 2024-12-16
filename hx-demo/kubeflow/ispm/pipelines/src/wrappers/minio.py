from minio import Minio
from minio.error import S3Error
import os
import io
import glob

def pipelines_filesystem_conn(host, port, user, passwd):
    """
    Function for establishing the connection with the
    pipelines shared filesystem.
    """

    client = Minio(f"{host}:{port}", user, passwd, secure=False)

    return client

def minio_create_bucket(client, bucket_name):
    """
    Function that checks if a bucket with the
    user name exists, if not creates one.
    """

    try:
        if client.bucket_exists(bucket_name):
            print(f"{bucket_name} bucket already exists!")
        else:
            # Create bucket.
            client.make_bucket(bucket_name)
            print(f"creating bucket {bucket_name} ...")
    except S3Error as e:
        print(f"Error creating bucket: {e}")

def minio_create_directory(client, bucket_name, directory):
    """
    Creates a directory under a bucket.
    Args:
        directory: the directory to be created
    """

    # Create an empty BytesIO stream
    empty_data = io.BytesIO(b"")
    try:
        # Upload an empty file to create the directory
        client.put_object(bucket_name, os.path.join(directory, ".miniokeep"), empty_data, 0)
        print(f"Directory '{directory}' created under bucket '{bucket_name}'.")
    except S3Error as e:
        print(f"Error creating directory: {e}")

def minio_push_file(client, bucket_name, local_file_path, bucket_directory, file_name):
    """
    Function that pushes a file into a bucket inside a Minio instance
    Args:
        client (class minio.api.Minio): Client where the credentials 
        are defined for establishing the connection.
        bucket_name (str): Name of the bucket where the file is
        going to be pushed.
        local_file_path (str): Path where the file is located locally.
        bucket_directory (str): Directory where the file is going to be 
        pushed inside the bucket in Minio.
        file_name (str): Name that the file is going to have after pushing
        it to Minio
    """

    try:
        object_name = os.path.join(bucket_directory, file_name)
        # Replace Windows path separator with Unix-style for MinIO
        object_name = object_name.replace(os.sep, '/')
        client.fput_object(bucket_name, object_name, local_file_path)
        print(f"Uploaded {local_file_path} to {object_name} in MinIO")
    except S3Error as e:
        print(f"Error uploading to MinIO: {e}")

def minio_get_file(client, bucket_name, local_file_path, bucket_directory, file_name):
    """
    Function that gets a file from a bucket in Minio.
    Args:
        client (class minio.api.Minio): Client where the credentials 
        are defined for establishing the connection.
        bucket_name (str): Name of the bucket from the file is going
        to be retrieved.
        local_file_path (str): Path where the file is going to be
        downloaded.
        bucket_directory (str): Directory from the file is going to be 
        retrieved inside the bucket in Minio.
        file_name (str): Name of the file to be downloaded.
    """

    try:
        object_name = os.path.join(bucket_directory, file_name)
        # Replace Windows path separator with Unix-style for MinIO
        object_name = object_name.replace(os.sep, '/')
        client.fget_object(bucket_name, object_name, local_file_path)
        print(f"Downloaded {object_name} from minio to {local_file_path} in the container")
    except S3Error as e:
        print(f"Error uploading to MinIO: {e}")
        

    
def minio_get_folder(client, bucket_name, minio_path, local_path):
    # Ensure the local directory exists
    if not os.path.exists(local_path):
        os.makedirs(local_path)

    # List objects in the given path
    objects = client.list_objects(bucket_name, prefix=minio_path, recursive=True)

    for obj in objects:
        # Remove the leading minio_path from the object name to get the relative path
        relative_path = obj.object_name[len(minio_path):].lstrip('/')

        # Form the local file path preserving only the last part of the structure
        local_file_path = os.path.join(local_path, relative_path)

        # Create directories if needed
        if not os.path.exists(os.path.dirname(local_file_path)):
            os.makedirs(os.path.dirname(local_file_path))

        # Download the file
        client.fget_object(bucket_name, obj.object_name, local_file_path)
        print(f"Downloaded {obj.object_name} to {local_file_path}")
        

def upload_local_directory_to_minio(client, local_path, bucket_name, minio_path):
    assert os.path.isdir(local_path)

    for local_file in glob.glob(local_path + '/**'):
        local_file = local_file.replace(os.sep, "/")
        if not os.path.isfile(local_file):
            upload_local_directory_to_minio(
                local_file, bucket_name, minio_path + "/" + os.path.basename(local_file))
        else:
            remote_path = os.path.join(
                minio_path, local_file[1 + len(local_path):])
            remote_path = remote_path.replace(
                os.sep, "/")
            client.fput_object(bucket_name, remote_path, local_file)