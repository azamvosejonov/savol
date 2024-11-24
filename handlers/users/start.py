from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import random
from loader import dp,bot,user_db
from aiogram.types import CallbackQuery
from aiogram.dispatcher.filters import Text









# Savollar va javoblar
quiz_data = [
    {"question": "Yer Quyosh atrofini necha kunda aylanib chiqadi?", "options": ["365", "300", "400"], "answer": "365"},
    {"question": "Eng katta okean qaysi?", "options": ["Tinch okeani", "Atlantika", "Hind okeani"],
     "answer": "Tinch okeani"},
    {"question": "Eng uzun daryo qaysi?", "options": ["Amazonka", "Nil", "Missisipi"], "answer": "Nil"},
    {"question": "Ayolning eng uzun so‘zi qaysi?", "options": ["chiroyli", "yig‘lama", "a'lo"], "answer": "a'lo"},
    {"question": "Odam tanasida qancha suyak bor?", "options": ["206", "210", "220"], "answer": "206"},
    {"question": "Eng yuqori nuqta qayerda?", "options": ["Everest", "K2", "Elbrus"], "answer": "Everest"},
    {"question": "Inson miya vazni qancha?", "options": ["1.4 kg", "1.5 kg", "1 kg"], "answer": "1.4 kg"},
    {"question": "Hamma vaqtning eng qadimgi fuqaroligiga ega davlat?", "options": ["Misr", "Iroq", "Xitoy"],
     "answer": "Misr"},
    {"question": "Qaysi o‘rmon eng katta?", "options": ["Amazonka", "Sibir", "Tropik"], "answer": "Amazonka"},
    {"question": "Qaysi davrda dinozavrlar yashagan?", "options": ["Jurassik", "Permian", "Devon"],
     "answer": "Jurassik"},
    {"question": "Eng yirik hayvon qaysi?", "options": ["Fil", "Ko‘k kit", "Zebra"], "answer": "Ko‘k kit"},
    {"question": "Qaysi hayvon parvoz qilolmaydi?", "options": ["Pingvin", "Ikkilamchi", "To‘rva"],
     "answer": "Pingvin"},
    {"question": "Haqiqiy qahva qayerda o‘sadi?", "options": ["Afrika", "Osiyo", "Amerika"], "answer": "Afrika"},
    {"question": "Dunyodagi eng tez uchuvchi qush qaysi?", "options": ["Qush", "Falcon", "Kunduz"], "answer": "Falcon"},
    {"question": "Havolarda eng tez uchuvchi kim?", "options": ["Falcon", "Aviator", "Qush"], "answer": "Falcon"},
    {"question": "Dengizda eng katta hayvon qaysi?", "options": ["Ko‘k kit", "Qora qartal", "Sarmaoy"],
     "answer": "Ko‘k kit"},
    {"question": "Eng katta orol qaysi?", "options": ["Grinlandiya", "Avstraliya", "Java"], "answer": "Grinlandiya"},
    {"question": "Qaysi matematik amalda siz ko‘paytirish amalga oshirasiz?",
     "options": ["Qaytarish", "Kop", "O‘zgartirish"], "answer": "Kop"},
    {"question": "Maysalar qaysi o‘simlik turiga kiradi?", "options": ["Sotib olish", "Bahor", "Havol"],
     "answer": "Sotib olish"},
    {"question": "Dunyodagi eng tez ishlaydigan kompyuter qaysi?", "options": ["Clustertown", "Acer", "Olga"],
     "answer": "Clustertown"},
    {"question": "Tegishli qo'shiq qaysi?", "options": ["Crack", "Win", "MisT"], "answer": "Crack"},
    {"question": "Helsinki qayerda?", "options": ["Finlandiya", "Norvegiya", "Svenska"], "answer": "Finlandiya"},
    {"question": "Kremniy deb nima?", "options": ["Olimpiya tog'i", "Kimiya tuzilma", "Atom"], "answer": "Atom"},
    {"question": "Xitoyning poytaxti qaysi?", "options": ["Pekin", "Guangzhou", "Nanjing"], "answer": "Pekin"},
    {"question": "Osiyo eng katta qit'a hisoblanadi?", "options": ["Ha", "Yo‘q", "Birinchi"], "answer": "Ha"},
    {"question": "Dunyodagi eng qimmat mashina qanday nomlangan?", "options": ["Bugatti Chiron", "Tesla", "Mitsubishi"],
     "answer": "Bugatti Chiron"},
    {"question": "Zaminning ikki foizi qayerda?", "options": ["Suv", "Yer", "Suv"], "answer": "Suv"},
    {"question": "Ko‘z sohasida qaysi ajratilgan miya?", "options": ["Sarfo", "Fin", "Masal"], "answer": "Sarfo"},
    {"question": "Egizaklar haqida qanday mantiq?", "options": ["Shaxsiy", "Hayot", "Ilk"], "answer": "Hayot"},
    {"question": "Surxondaryo qanday?", "options": ["Bo‘yi uzun", "Sho‘rt", "Tovar"], "answer": "Bo‘yi uzun"},
    {"question": "Ixtilomni qayta ishlashda?", "options": ["Dizayn", "Depozit", "Oyna"], "answer": "Dizayn"}

]

# Foydalanuvchi reytinglari
user_scores = {}
current_questions = {}

# /start komandasi uchun handler
@dp.message_handler(CommandStart())
async def send_welcome(message: types.Message):
    user_id = message.from_user.id
    user_scores[user_id] = 0  # Foydalanuvchini ro'yxatga qo'shamiz
    await message.reply(
        "Salom! Mini-Quizga xush kelibsiz. Savollarga javob bering va ball to‘plang.\n"
        "Boshlash uchun /quiz buyrug‘ini bering."
    )



@dp.message_handler(commands=['stats'])
async def start_quiz(message: types.Message):
    count = user_db.count_users()
    await message.answer(f"Bazada <b>{count}</b> ta foydalanuvchi bor")

@dp.message_handler(commands=['quiz'])
async def start_quiz(message: types.Message):
    # Tasodifiy savol tanlaymiz
    question_data = random.choice(quiz_data)
    question = question_data["question"]
    options = question_data["options"]
    correct_answer = question_data["answer"]

    # Foydalanuvchi uchun savolni saqlaymiz
    current_questions[message.from_user.id] = correct_answer

    # Javob variantlari uchun klaviatura yaratamiz
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(*options)

    # Savolni foydalanuvchiga yuboramiz
    await message.reply(f"Savol: {question}", reply_markup=markup)

# Javobni qayta ishlash
@dp.message_handler(lambda message: message.from_user.id in current_questions)
async def handle_answer(message: types.Message):
    user_id = message.from_user.id

    # Agar foydalanuvchi reytingda mavjud bo'lmasa, uni qo'shamiz
    if user_id not in user_scores:
        user_scores[user_id] = 0

    correct_answer = current_questions[user_id]

    # Javobni tekshiramiz
    if message.text == correct_answer:
        user_scores[user_id] += 1
        response = "To'g'ri javob! 🎉"
    else:
        response = f"Notog'ri javob. 😢 To'g'ri javob: {correct_answer}"

    # Natijani ko'rsatamiz
    response += f"\nBalingiz: {user_scores[user_id]}"
    await message.reply(response, reply_markup=types.ReplyKeyboardRemove())

    # Savolni o'chirib tashlaymiz
    del current_questions[user_id]

    # Yangi savolni taklif qilamiz
    await message.reply("Yana bir savol uchun /quiz ni yozing!")

# /score komandasi uchun handler
@dp.message_handler(commands=['score'])
async def show_score(message: types.Message):
    score = user_scores.get(message.from_user.id, 0)
    await message.reply(f"Sizning umumiy ballaringiz: {score}")


# Botni ishga tushirish
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

