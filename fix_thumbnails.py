import os
import django
import requests

# Set up the Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "yesterdays.settings")
django.setup()

from images.models import Image
from images.tasks import process_image

def main():
    # Get all images that have a thumbnail URL set
    images = Image.objects.exclude(thumbnail__isnull=True).exclude(thumbnail="")
    broken_count = 0

    print(f"Scanning {images.count()} images for broken thumbnails...")

    for img in images:
        try:
            # A HEAD request just grabs the headers (very fast), not the image data
            response = requests.head(img.thumbnail, timeout=5)
            
            # If Cloudflare/R2 returns a 404, we know the database and R2 are out of sync
            if response.status_code == 404:
                print(f"Image {img.id} has a broken thumbnail ({img.thumbnail}). Queuing fix...")
                process_image.delay(img.id, force=True)
                broken_count += 1
                
        except requests.RequestException as e:
            print(f"Error checking image {img.id}: {e}")

    print(f"\nDone! Queued {broken_count} images for reprocessing.")

if __name__ == "__main__":
    main()