import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Online_Course.settings')
django.setup()

from core.models import Instructor
from django.core.files import File

def update_instructor_images():
    try:
        # Update Saran's image
        saran = Instructor.objects.get(name='Saran')
        with open('static/images/cd_ins_1.jpg', 'rb') as img_file:
            saran.image.save('cd_ins_1.jpg', File(img_file), save=True)
        print("Updated Saran's image successfully")

        # Update Deepan's image
        deepan = Instructor.objects.get(name='Deepan')
        with open('static/images/cd_ins_2.jpg', 'rb') as img_file:
            deepan.image.save('cd_ins_2.jpg', File(img_file), save=True)
        print("Updated Deepan's image successfully")

    except Exception as e:
        print(f"Error updating images: {str(e)}")

if __name__ == '__main__':
    update_instructor_images()