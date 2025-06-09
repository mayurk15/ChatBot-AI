from django.http import StreamingHttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import requests
import json
import time

HUGGINGFACE_API_TOKEN = "ADD THE TOKEN HERE"
API_URL = "https://router.huggingface.co/sambanova/v1/chat/completions"
MODEL_NAME = "Meta-Llama-3.1-8B-Instruct"  # Your working model

@csrf_exempt
def chat_view(request):
    if request.method == 'POST':
        prompt = request.POST.get('prompt', '')

        headers = {
            "Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": MODEL_NAME,
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }

        def stream_response():
            response = requests.post(
                API_URL,
                headers=headers,
                json=payload,
                timeout=60
            )

            if response.status_code != 200:
                yield f"⚠️ Error: {response.status_code} - {response.text}\n"
                return

            try:
                data = response.json()
                # The generated content is here:
                generated_text = data["choices"][0]["message"]["content"]
            except Exception as e:
                yield f"⚠️ Error parsing response: {str(e)}\n"
                return

            # Simulate streaming response line by line
            for line in generated_text.split('\n'):
                yield line + '\n'
                time.sleep(0.05)

        return StreamingHttpResponse(stream_response(), content_type='text/plain')

    return render(request, 'chat.html')


def login(request):
    return render(request, 'login.html')


def home(request):
    return render(request, 'new.html')
