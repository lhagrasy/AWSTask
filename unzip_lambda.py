import json
import boto3
from io import BytesIO
import zipfile



def lambda_handler(event,context):
    s3_resource = boto3.resource('s3')
    source_bucket = 's3task'
    target_bucket = 's3task'
    my_bucket = s3_resource.Bucket(source_bucket)


    for file in my_bucket.objects.all():
        if(str(file.key).endswith('.zip')):
            zip_obj = s3_resource.Object(bucket_name=source_bucket, key=file.key)
            buffer = BytesIO(zip_obj.get()["body"].read())


            z = zipfile.ZipFile(buffer)
            for filename in z.namelist():
                file_info = z.getinfo(filename)
                try:
                    response = s3_resource.meta.client_upload_fileobj(
                            z.open(filename),
                            Bucket=target_bucket,
                            key=f'{filename}'

                            )
                except Exception as e:
                    print(e)
        else:
            print(file.key+ ' is not a zip file')

