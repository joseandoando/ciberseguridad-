import json

import azure.functions as func

from ai_service import AIService
from rag_service import RAGService

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)
ai_service = AIService()
rag_service = RAGService()


@app.route(route="ask", methods=["POST"])
async def ask(req: func.HttpRequest) -> func.HttpResponse:
    try:
        payload = req.get_json()
    except ValueError:
        return func.HttpResponse(
            json.dumps({"error": "Invalid JSON"}),
            status_code=400,
            mimetype="application/json",
        )

    question = str(payload.get("question", "")).strip()
    if not question:
        return func.HttpResponse(
            json.dumps({"error": "Field 'question' is required"}),
            status_code=400,
            mimetype="application/json",
        )

    context = rag_service.retrieve(question)
    answer = await ai_service.answer(question, context)

    return func.HttpResponse(
        json.dumps({"question": question, "answer": answer}),
        status_code=200,
        mimetype="application/json",
    )
