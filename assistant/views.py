import os
import json
import traceback
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage

from assistant.rag.loader import load_and_chunk
from assistant.rag.embedding import embed_and_store, load_vectorstore
import os
import json
import traceback
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from assistant.rag.embedding import load_vectorstore
import google.generativeai as genai
from assistant.rag.embedding import load_vectorstore

import os
import shutil


def health_check(request):
    return JsonResponse({"status": "ok"})

@csrf_exempt
def upload_pdf(request):
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']
        file_path = default_storage.save(file.name, file)

        try:
            # Step 1: Safely delete vector store BEFORE loading
            persist_path = "vector_store"
            if os.path.exists(persist_path):
                import shutil
                shutil.rmtree(persist_path)

            # Step 2: Process and embed
            chunks = load_and_chunk(file_path)
            embed_and_store(chunks)

            return JsonResponse({'message': 'PDF embedded successfully'})
        except Exception as e:
            import traceback
            return JsonResponse({'error': str(e), 'trace': traceback.format_exc()}, status=500)

    return JsonResponse({'error': 'No file uploaded'}, status=400)


@csrf_exempt
def ask_question(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            question = data.get('question')
            if not question:
                return JsonResponse({'error': 'Missing question'}, status=400)

            #  Set API key
            genai.configure(api_key=os.environ.get("GEMINI_KEY"))

            # Get context from vector store
            db = load_vectorstore()
            docs = db.similarity_search(question, k=3)
            context = "\n\n".join([d.page_content for d in docs])

            #  Build Gemini prompt
            prompt = f"""Use the context below to answer the question. Be specific and detailed.

Context:
{context}

Question: {question}
"""

            model = genai.GenerativeModel("gemini-2.0-flash")
            response = model.generate_content(prompt)

            return JsonResponse({'answer': response.text})

        except Exception as e:
            return JsonResponse({
                'error': str(e),
                'trace': traceback.format_exc()
            }, status=500)

    return JsonResponse({'error': 'POST request required'}, status=400)