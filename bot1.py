import os
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, CallbackContext, CommandHandler

# 환경 변수에서 TOKEN 가져오기
TOKEN = os.getenv("TOKEN")

# 금지어 리스트 (원하는 단어 추가 가능)
FORBIDDEN_WORDS = ["좆같은새끼", "좆같은새.끼", "좆같은새1끼", "시발새끼", "씨발새끼", "카피", "카.피", "카1피",
"씨발새.끼", "씨발새1끼", "시발새.끼", "시발새1끼", "씨.발새끼", "씨1발새끼", "시.발새끼", "시1발새끼", "사발새끼", "시발년", "씨발련",
"개새끼", "개1새끼", "개.새끼", "개새1끼", "개새.끼",
"자동매매", "자.동매매", "자.동.매매", "자.동.매.매", "자.동매.매", "자.동1매매", "자.동1매.매", "자.동1매1매", "자1동매매",
"자1동.매매", "자1동.매.매", "자1동1매.매", "자1동1매1매", "자동매1매", "자동매.매",
"니애미", "니애.미", "니.애미", "니.애.미", "니애1미", "니1애미", "니1애.미", "니1애1미", "니.애1미",
"니애비", "니애.비", "니.애비", "니.애.비", "니애1비", "니1애비", "니1애.비", "니1애1비", "니.애1비",
"니엄마", "니엄.마", "니.엄마", "니.엄.마", "니엄1마", "니1엄마", "니1엄.마", "니1엄1마", "니.엄1마",
"자동 매매", "죽여버린다", "죽.여버린다", "죽1여버린다", "꺼져", "꺼.져", "꺼1져", "좆까", "좆1까", "좆.까", "좆도", "청산", "청1산",
"청.산"]


async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("안녕하세요! 저는 금지어 감시 봇입니다.")

# 예외 처리할 관리자 ID 목록
EXEMPT_USERS = [2038663568, 6427359534]  # 운영진의 Telegram ID를 여기에 추가

async def filter_messages(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    user_id = update.message.from_user.id
    text = update.message.text.lower()

    # 운영진인지 먼저 확인 (운영진이면 그냥 통과)
    if user_id in EXEMPT_USERS:
        return  # 메시지 삭제 X, 아무 행동도 하지 않음

    # 금지어 감지 및 일반 사용자 처리
    if any(word in text for word in FORBIDDEN_WORDS):
        try:
            await context.bot.delete_message(chat_id=chat_id, message_id=update.message.message_id)

            # 영구 강퇴 (재입장 불가)
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


