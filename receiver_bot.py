from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import os

# ✅ توكن بوت الاستقبال
BOT_RECEIVER_TOKEN = "1724071074:AAHY4HlO6P6c2zrgJVtOwj30Iz0xgwhFoGU"

# ✅ معرف المسؤول الوحيد المسموح له بالدخول
ADMIN_ID = 1487998139  # استبدل بمعرفك الشخصي في تيليجرام

# ✅ الرمز السري للدخول
SECRET_CODE = "4455"

# ✅ قائمة المستخدمين المصرح لهم
authorized_users = set()

# ✅ استجابة للأمر /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    if user_id in authorized_users:
        await update.message.reply_text("✅ لديك صلاحية الوصول للبيانات!")
    else:
        await update.message.reply_text("🔒 مرحبًا! الرجاء إدخال الرمز السري لمتابعة.")

# ✅ التحقق من الرمز السري
async def check_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    code = update.message.text.strip()

    if code == SECRET_CODE:
        authorized_users.add(user_id)
        await update.message.reply_text("✅ تم التحقق! يمكنك الآن رؤية البيانات.")
    else:
        await update.message.reply_text("❌ رمز خاطئ! حاول مرة أخرى.")

# ✅ استقبال البيانات من البوت الرئيسي
async def receive_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    if user_id not in authorized_users:
        await update.message.reply_text("⛔️ لا يمكنك الوصول إلى البيانات بدون التحقق!")
        return

    message = update.message.text

    # 📝 حفظ البيانات في ملف
    with open("received_users.txt", "a", encoding="utf-8") as file:
        file.write(f"{message}\n")

    await update.message.reply_text("✅ تم حفظ البيانات!")

# ✅ تشغيل البوت
def main():
    app = Application.builder().token(BOT_RECEIVER_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_code))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, receive_data))

    print("✅ بوت الاستقبال يعمل...")
    app.run_polling()

if __name__ == "__main__":
    main()
