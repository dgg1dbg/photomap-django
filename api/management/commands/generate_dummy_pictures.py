from django.core.management.base import BaseCommand
from ...post.model import Post
from ...picture.model import Picture
import random
from django.contrib.gis.geos import Point


class Command(BaseCommand):
    help = 'Generate dummy Picture entries'

    def add_arguments(self, parser):
        parser.add_argument('--count', type=int, default=1000, help='Number of dummy pictures to generate')
        parser.add_argument('--remove', type=bool, default=False, help='Remove all dummy pictures')

    def handle(self, *args, **options):
        count = options['count']
        posts = list(Post.objects.all())

        if options['remove']:
            Picture.objects.filter(file_id__startswith='dummy_file_id_').delete()
            self.stdout.write(self.style.SUCCESS('All dummy Picture objects removed successfully.'))
            return
        
        if not posts:
            self.stdout.write(self.style.ERROR('No Post objects found. Create some first.'))
            return
        pictures = []
        for i in range(count):
            post = random.choice(posts)
            longitude = random.uniform(124, 129)
            latitude = random.uniform(33, 38)
            location = Point(longitude, latitude)
            picture = Picture(
                file_id=f"dummy_file_id_{i}",
                location=location,
                description="Dummy description",
                post=post,
            )
            pictures.append(picture)

        Picture.objects.bulk_create(pictures)
        self.stdout.write(self.style.SUCCESS(f'{count} dummy Picture objects created successfully.'))
