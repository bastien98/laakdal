import os
import zipfile
import datetime
import boto3
from botocore.exceptions import NoCredentialsError
from dotenv import load_dotenv
load_dotenv()

# S3 configuration
S3_BUCKET = 'test-kobe-laakdal'
AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
AWS_SECRET_KEY = os.getenv('AWS_SECRET_KEY')


def zip_folder(folder_path, output_path):
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, folder_path)
                zipf.write(file_path, arcname)


def upload_to_s3(local_file, s3_file):
    s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)
    try:
        s3.upload_file(local_file, S3_BUCKET, s3_file)
        return True
    except NoCredentialsError:
        print("Credentials not available")
        return False


def main():
    date_str = datetime.date.today().strftime("%Y-%m-%d")
    local_folder_path = f"./photos/{date_str}"
    zip_file_path = f"./tmp/{date_str}_photos.zip"

    # Zip the folder
    zip_folder(local_folder_path, zip_file_path)

    # Upload to S3
    s3_file_name = f"photos/{date_str}/{date_str}_photos.zip"
    if upload_to_s3(zip_file_path, s3_file_name):
        print("Upload Successful")
    else:
        print("Upload Failed")

    # Clean up the local zip file
    os.remove(zip_file_path)


if __name__ == "__main__":
    main()
