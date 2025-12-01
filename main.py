from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters
import subprocess
import os
import tempfile

# ضع التوكن الخاص بالبوت هنا
TOKEN = "8485168816:AAG5wN7PuQwlv8l-XwqullQ_LNheirKGqbQ"

# المسار الكامل لـ yt-dlp
YTDLP_PATH = r"C:\\Users\\mohammad\\AppData\\Roaming\\Python\\Python39\\Scripts\\yt-dlp.exe"


async def start(update, context):
    await update.message.reply_text(
        "👋 أهلاً! أرسل رابط فيديو من أي منصة مدعومة وسأقوم بتحميله لك بأفضل جودة متاحة."
    )


async def handle_msg(update, context):
    url = update.message.text

    if not url.startswith("http"):
        await update.message.reply_text("⚠️ يجب إرسال رابط فيديو صحيح.")
        return

    msg = await update.message.reply_text("⏳ جاري التحميل...")

    with tempfile.TemporaryDirectory() as tdir:
        output = os.path.join(tdir, "video.mp4")

        try:
            # تحميل أفضل جودة متاحة (فيديو + صوت معًا إن أمكن)
            subprocess.run([
                YTDLP_PATH,
                "-f", "best",          # أفضل صيغة متاحة
                "--no-playlist",       # أسرع: يتجاهل قوائم التشغيل
                "-o", output,
                url
            ], check=True)

            # إرسال الفيديو للمستخدم
            with open(output, "rb") as video_file:
                await update.message.reply_video(video=video_file)

            await msg.edit_text("✅ تم التحميل بنجاح!")

        except Exception as e:
            print(f"Error: {e}")
            await msg.edit_text("❌ لم أتمكن من تحميل الفيديو. تأكد من صحة الرابط.")


def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_msg))

    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()