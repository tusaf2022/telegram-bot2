import os
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, CallbackContext, CommandHandler

# Railway 환경 변수에서 TOKEN 불러오기
TOKEN = os.getenv("TOKEN")  # 환경 변수에서 "TOKEN"이라는 키의 값을 가져옴

# 금지어 리스트 (원하는 단어 추가 가능)
FORBIDDEN_WORDS = ["손실", "손.실", "손실1"]

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("안녕하세요! 저는 금지어 감시 봇입니다.")

async def filter_messages(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    user_id = update.message.from_user.id
    text = update.message.text.lower()  # 메시지를 소문자로 변환

    if any(word in text for word in FORBIDDEN_WORDS):
        try:
            await context.bot.delete_message(chat_id=chat_id, message_id=update.message.message_id)
            await context.bot.ban_chat_member(chat_id, user_id)
            await context.bot.send_message(chat_id, f"⚠️ {update.message.from_user.first_name}님이 금지된 단어를 사용하여 강퇴되었습니다.")
        except Exception as e:
            print(f"오류 발생: {e}")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, filter_messages))
    print("봇이 실행 중입니다...")
    app.run_polling()

if __name__ == "__main__":
    main()

