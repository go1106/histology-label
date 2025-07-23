#from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import SlideImage
from .forms import SlideImageForm

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from .models import Annotation



def home(request):
    return render(request, 'core/home.html')




def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in after signup
            return redirect('gallery')  # or wherever you want to send them
    else:
        form = UserCreationForm()
    return render(request, 'core/signup.html', {'form': form})


@login_required
def upload_image(request):
    if request.method == 'POST':
        form = SlideImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.uploaded_by = request.user
            image.save()
            return redirect('gallery')
    else:
        form = SlideImageForm()
    return render(request, 'core/upload.html', {'form': form})



def gallery(request):
    slides = SlideImage.objects.all().order_by('-upload_date')  # newest first
    return render(request, 'core/gallery.html', {'slides': slides})

from django.shortcuts import get_object_or_404

def slide_detail(request, slide_id):
    slide = get_object_or_404(SlideImage, id=slide_id)
    return render(request, 'core/slide_detail.html', {'slide': slide})




def slide_detail(request, slide_id):
    slide = get_object_or_404(SlideImage, id=slide_id)
    annotations = Annotation.objects.filter(slide=slide)

    return render(request, 'core/slide_detail.html', {
        'slide': slide,
        'annotations': annotations
    })

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

@csrf_exempt
def save_annotation(request, slide_id):
    if request.method == 'POST':
        data = json.loads(request.body)

        label = data.get('label')
        x = data.get('x')
        y = data.get('y')
        width = data.get('width')
        height = data.get('height')

        slide = get_object_or_404(SlideImage, id=slide_id)

        Annotation.objects.create(
            slide=slide,
            label=label,
            x=x,
            y=y,
            width=width,
            height=height,
            created_by=request.user if request.user.is_authenticated else None
        )

        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

from django.views.decorators.http import require_POST

from django.shortcuts import get_object_or_404

@require_POST
def delete_annotation(request, annotation_id):
    annotation = get_object_or_404(Annotation, id=annotation_id)
    if request.user.is_authenticated and request.user == annotation.created_by:
        annotation.delete()
        return JsonResponse({'status': 'deleted'})
    return JsonResponse({'status': 'unauthorized'}, status=403)

import csv
from django.http import HttpResponse

def export_annotations_csv(request, slide_id):
    slide = get_object_or_404(SlideImage, id=slide_id)
    annotations = Annotation.objects.filter(slide=slide)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{slide.title}_annotations.csv"'

    writer = csv.writer(response)
    writer.writerow(['Label', 'X', 'Y', 'Width', 'Height', 'Created By', 'Created At'])

    for ann in annotations:
        writer.writerow([
            ann.label,
            ann.x,
            ann.y,
            ann.width,
            ann.height,
            ann.created_by.username if ann.created_by else 'Anonymous',
            ann.created_at.strftime('%Y-%m-%d %H:%M:%S')
        ])

    return response


from transformers import AutoFeatureExtractor, AutoModelForImageClassification
from PIL import Image
import torch
import io


from transformers import AutoImageProcessor, AutoModelForImageClassification
from PIL import Image
import torch

# 使用较新的 ViT 模型
extractor = AutoImageProcessor.from_pretrained("google/vit-base-patch16-224")
model = AutoModelForImageClassification.from_pretrained("google/vit-base-patch16-224")

#extractor = AutoFeatureExtractor.from_pretrained("microsoft/resnet-50")
#model = AutoModelForImageClassification.from_pretrained("microsoft/resnet-50")


@require_POST
@login_required
def analyze_slide(request, slide_id):
    try:
        print("🔍 1. Get slide")
        slide = get_object_or_404(SlideImage, id=slide_id)

        print("🔍 2. Load and resize image")
        image = Image.open(slide.image_file.path).convert("RGB").resize((224, 224))

        print("🔍 3. Run extractor")
        inputs = extractor(images=image, return_tensors="pt")
        inputs = {k: v.to("cpu").float() for k, v in inputs.items()}  # ✅ 放到 CPU 且 float32

        print("🔍 4. Send model to CPU")
        model.to("cpu")  # ✅ 明确模型在 CPU 上运行

        print("🔍 5. Model forward")
        with torch.no_grad():
            outputs = model(**inputs)

        print("🔍 6. Get prediction")
        predicted_class = outputs.logits.argmax(-1).item()
        label = model.config.id2label[predicted_class]

        print("✅ 7. Success, label:", label)
        return JsonResponse({"label": label})

    except Exception as e:
        print("❌ Exception during AI analysis:", e)
        return JsonResponse({"error": "AI analysis failed", "detail": str(e)}, status=500)
