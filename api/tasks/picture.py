import redis
import io
from celery import shared_task
import boto3
from PIL import Image
from django.conf import settings

r = redis.StrictRedis(host='redis', port=6379, db=2)


TARGET_WIDTHS = {
    'small': 150,
    'medium': 3000,
    'large': 6000
}

def resize_keep_aspect(image, target_width):
    if image.width <= target_width:
        return image.copy()
    w_percent = target_width / float(image.width)
    target_height = int(image.height * w_percent)
    return image.resize((target_width, target_height), Image.LANCZOS)

@shared_task
def compress_and_upload_image(image_key, size):
    image_data = r.get(image_key)
    if image_data is None:
        return
    image = Image.open(io.BytesIO(image_data))

    resized = resize_keep_aspect(image, TARGET_WIDTHS[size])

    buffer = io.BytesIO()
    resized.save(buffer, format='JPEG')
    buffer.seek(0)

    s3_client = boto3.client('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                             aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
    s3_client.upload_fileobj(buffer, 
                             settings.AWS_BUCKET_NAME, 
                             f'compressed/{image_key}_{size}.jpg',
                             ExtraArgs={'ContentType': 'image/jpeg'}
                             )

    done_key = f'done:{image_key}'
    count = r.incr(done_key)
    if count == 3:
        r.delete(done_key)
        r.delete(image_key)


@shared_task
def delete_picture(picture_id):
    s3_client = boto3.client('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                             aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
    for size in TARGET_WIDTHS.keys():
        s3_client.delete_object(Bucket=settings.AWS_BUCKET_NAME, Key=f'compressed/{picture_id}_{size}.jpg')