import os
import face_recognition
from django.shortcuts import render
from django.conf import settings

def upload_and_match(request):
    if request.method == 'POST' and request.FILES.get('image'):
        uploaded_file = request.FILES['image']
        upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
        os.makedirs(upload_dir, exist_ok=True)

        file_path = os.path.join(upload_dir, uploaded_file.name)
        with open(file_path, 'wb+') as dest:
            for chunk in uploaded_file.chunks():
                dest.write(chunk)

        uploaded_img = face_recognition.load_image_file(file_path)
        encodings = face_recognition.face_encodings(uploaded_img)
        if not encodings:
            return render(request, 'result.html', {'error': 'No face detected.'})

        uploaded_encoding = encodings[0]

        match_dir = os.path.join(settings.MEDIA_ROOT, 'wedding_photos')
        matching_images = []

        for img_name in os.listdir(match_dir):
            img_path = os.path.join(match_dir, img_name)
            try:
                known_img = face_recognition.load_image_file(img_path)
                known_encs = face_recognition.face_encodings(known_img)
                for enc in known_encs:
                    result = face_recognition.compare_faces([uploaded_encoding], enc, tolerance=0.6)
                    if result[0]:
                        matching_images.append('media/wedding_photos/' + img_name)
                        break
            except Exception as e:
                print(f"Error with {img_name}: {e}")

        return render(request, 'result.html', {'matches': matching_images})

    return render(request, 'upload.html')
