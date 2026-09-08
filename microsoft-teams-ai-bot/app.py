import json
import os

from aiohttp import web
from botbuilder.core import ActivityHandler, BotFrameworkAdapter, BotFrameworkAdapterSettings, TurnContext
from botbuilder.schema import Activity, ActivityTypes
from dotenv import load_dotenv

from ai_service import AIService
from rag_service import RAGService

load_dotenv()

APP_ID = os.getenv("MICROSOFT_APP_ID", "")
APP_PASSWORD = os.getenv("MICROSOFT_APP_PASSWORD", "")
PORT = int(os.getenv("PORT", "3978"))

adapter = BotFrameworkAdapter(BotFrameworkAdapterSettings(APP_ID, APP_PASSWORD))
ai_service = AIService()
rag_service = RAGService()


class EnterpriseAIBot(ActivityHandler):
    async def on_message_activity(self, turn_context: TurnContext):
        question = (turn_context.activity.text or "").strip()
        context = rag_service.retrieve(question)
        answer = await ai_service.answer(question, context)
        await turn_context.send_activity(answer)

    async def on_members_added_activity(self, members_added, turn_context: TurnContext):
        for member in members_added:
            if member.id != turn_context.activity.recipient.id:
                await turn_context.send_activity(
                    "Hi! I am the Microsoft Teams AI Support Bot. Ask me an operational or support question."
                )


bot = EnterpriseAIBot()


async def messages(req: web.Request) -> web.Response:
    if "application/json" not in req.headers.get("Content-Type", ""):
        return web.Response(status=415, text="Content-Type must be application/json")

    body = await req.json()
    activity = Activity().deserialize(body)
    auth_header = req.headers.get("Authorization", "")

    async def aux_func(turn_context: TurnContext):
        await bot.on_turn(turn_context)

    await adapter.process_activity(activity, auth_header, aux_func)
    return web.Response(status=201)


async def ask(req: web.Request) -> web.Response:
    try:
        payload = await req.json()
    except json.JSONDecodeError:
        return web.json_response({"error": "Invalid JSON"}, status=400)

    question = str(payload.get("question", "")).strip()
    if not question:
        return web.json_response({"error": "Field 'question' is required"}, status=400)

    context = rag_service.retrieve(question)
    answer = await ai_service.answer(question, context)
    return web.json_response({
        "question": question,
        "answer": answer,
        "rag_context_used": bool(context),
    })


async def health(_: web.Request) -> web.Response:
    return web.json_response({
        "status": "ok",
        "service": "microsoft-teams-ai-bot",
        "azure_openai_configured": bool(ai_service.client),
    })


@web.middleware
async def error_middleware(request: web.Request, handler):
    try:
        return await handler(request)
    except Exception as exc:
        return web.json_response(
            {"error": type(exc).__name__, "message": str(exc)},
            status=500,
        )


app = web.Application(middlewares=[error_middleware])
app.router.add_post("/api/messages", messages)
app.router.add_post("/api/ask", ask)
app.router.add_get("/health", health)


if __name__ == "__main__":
    web.run_app(app, host="0.0.0.0", port=PORT)
