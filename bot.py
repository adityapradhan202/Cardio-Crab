from telegram import Update
from telegram.ext import ConversationHandler
from telegram.ext import ContextTypes, CallbackContext
from telegram.ext import CommandHandler
from telegram.ext import ApplicationBuilder
from telegram.ext import MessageHandler
from telegram.ext import filters

import dotenv
import os

import joblib
heart_classifier = joblib.load('heart_classifier.joblib')

dotenv.load_dotenv()
bot_token = os.getenv('TOKEN')

async def start(update:Update, context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
"""🦀 Welcome to Cardio-Crab!

😥 Got your results but there's still time for the doctor consultation?
😉 Don't worry Cardio-Crab has got your brack!
        
Use the /help command to proceed!"""
    )

help_text = """
Here are the Cardio-Crabs commands!

You'll need some data from the medical reports before checking your heart health. And to check the list of data that you need use -> 
/description
To check your heart health use -> 
/check_heart

If you dont have any data or reports and just wanna test the bot for fun use this data -> 
https://github.com/adityapradhan202/Cardio-Crab/blob/main/heart_disease.csv
(This a dataset from kaggle!)

Disclaimer - The machine learning model integrated with this bot is only 84 percent accurate! In some cases the predictions might be wrong. We suggest you to consult an expert doctor, because it is the matter of your heart!

Developer's info - /devinfo
"""

parameters_description_text = """
These are the details that you will need to provide:-
1. Age

2. Sex - (Male or Female)

3. Chest pain type 
    - Value 0: typical angina
    - Value 1: atypical angina
    - Value 2: non-anginal pain
    - Value 3: asymptomatic

4. Resting blood pressure
    - blood pressure while resting (in mm Hg on admission to the hospital)

5. Cholestrol
    - A person's serum cholesterol in mg/dl

6. Fasting blood pressure
    - Blood sugar while fasting & [ > 120 mg/dl ] (1 = true; 0 = false)

7. Rest ECG
    - ECG (electrocardiographic) while resting
    - Value 0: normal
    - Value 1: having ST-T wave abnormality (T wave inversions and/or ST elevation or depression of > 0.05 mV)
    - Value 2: showing probable or definite left ventricular hypertrophy by Estes' criteria

8. Max heartrate
    - Maximum heart rate achieved

9. exang
    - exercise-induced angina (1 = yes; 0 = no)
    Exercise-induced angina (AP) is a common complaint of cardiac patients, particularly when exercising in the cold. It usually happens during activity (exertion) and goes away with rest or angina medication. For example, pain, when walking uphill or in cold weather, maybe angina. Stable angina pain is predictable and usually similar to previous episodes of chest pain.

10. oldpeak
    - ST depression induced by exercise relative to rest
    Exercise-induced ST segment depression is considered a reliable ECG finding for the diagnosis of obstructive coronary atherosclerosis. ST-segment depression is believed as a common electrocardiographic sign of myocardial ischemia during exercise testing. Ischemia is generally defined as oxygen deprivation due to reduced perfusion. ST segment depression less than 0.5 mm is accepted in all leads. ST segment depression 0.5 mm or more is considered pathological.

11. Slope
    - The slope of the peak exercise ST segment
    - Value 0: upsloping
    - Value 1: flat
    - Value 2: downsloping


12. Number of major vessels
    - No. of major vessels (0-3) colored by fluoroscopy

13. thal
    - thalassemia
    - 0: normal
    - 1: fixed defect
    - 2: reversible defect
    - People with thalassemia can get too much iron in their bodies, either from the disease or from frequent blood transfusions. Too much iron can result in damage to your heart, liver & endocrine system, which includes hormone-producing glands that regulate processes throughout your body.


Scroll up ☝️ and read the data that you will need in order to make the bot do predictions!
"""

async def help(update:Update, context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(help_text, disable_web_page_preview=True)

async def devinfo(update:Update, context:ContextTypes.DEFAULT_TYPE):
    link = 'https://github.com/adityapradhan202'
    await update.message.reply_text(f"Here's the developer's github profile - {link}")

async def description(update:Update, context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(parameters_description_text)

async def get_bot_invite_link(update:Update, context:ContextTypes.DEFAULT_TYPE):
    inv_link = 't.me/Cardio_Crab_Bot'
    await update.message.reply_text(f"Invitation link of the bot - {inv_link}")
    await update.message.reply_text('Share this link among people so that they can know there heart health too 👍')


#  Conversation part -
#  STAGES
AGE,SEX,CPT,RBP,CHOL,FBS,RECG,MAXHR,EXANG,OPEAK,SLOPE,NMV,THAL = range(13)

# starting point
async def check_heart(update:Update, context:CallbackContext):

    await update.message.reply_text('IMPORTANT - Use the /cancel the process to cancel or stop the bot at any moment!')
    await update.message.reply_text("How old are you?")

    return AGE

async def get_age_ask_sex(update:Update, context:CallbackContext):
    context.user_data['age'] = int(update.message.text)
    await update.message.reply_text("Enter 'M' if you are a male... enter 'F' if you are a female...")
    
    return SEX

async def get_sex_ask_cpt(update:Update, context:CallbackContext):
    if update.message.text == 'M' or update.message.text == 'm':
        context.user_data['sex'] = 1
    elif update.message.text == 'F' or update.message.text == 'f':
        context.user_data['sex'] = 0

    await update.message.reply_text("""
Enter the integer value for chest pain type -                                
🔴 Typical angina ➡️ 0
🔴 Atypical angina ➡️ 1
🔴 Non-anginal pain ➡️ 2
🔴 Asymptomatic ➡️ 3
""")
    
    return CPT

async def get_cpt_ask_rbp(update:Update, context:CallbackContext):
    context.user_data['cpt'] = int(update.message.text)
    await update.message.reply_text("Enter your resting blood presure (in mm Hg on admission to the hospital)")

    return RBP

async def get_rbp_ask_chol(update:Update, context:CallbackContext):
    context.user_data['rbp'] = int(update.message.text)
    await update.message.reply_text("Enter your cholestral (in mg/dl)")

    return CHOL

async def get_chol_ask_fbs(update:Update, context:CallbackContext):
    context.user_data['chol'] = int(update.message.text)
    await update.message.reply_text("Enter your fasting blood sugar (in mg/dl)")

    return FBS

async def get_fbs_ask_recg(update:Update, context:CallbackContext):
    if int(update.message.text) > 120:
        context.user_data['fbs'] = 1
    else:
        context.user_data['fbs'] = 0

    await update.message.reply_text('Enter the integer values related to your resting ECG type...')
    await update.message.reply_text(
"""
🔴 Normal ➡️ 0
🔴 Having ST-T wave abnormality (T wave inversions and/or ST elevation or depression of > 0.05 mV) ➡️ 1
🔴 Showing probable or definite left ventricular hypertrophy by Estes' criteria ➡️ 2

"""
    )
    return RECG

async def get_recg_ask_maxhr(update:Update, context:CallbackContext):
    context.user_data['recg'] = int(update.message.text)
    await update.message.reply_text("Enter maximum heart rate achieved...")

    return MAXHR

async def get_maxhr_ask_exang(update:Update, context:CallbackContext):
    context.user_data['maxhr'] = int(update.message.text)
    await update.message.reply_text('Enter ➡️ 1 if you have exercise-induced angina, otherwise enter ➡️ 0')

    return EXANG

async def get_exang_ask_opeak(update:Update, context:CallbackContext):
    
    context.user_data['exang'] = int(update.message.text)
    await update.message.reply_text('Enter old peak...')
    return OPEAK

async def get_opeak_ask_slope(update:Update, context:CallbackContext):
    # old peak is a float value  - unlike the other parameters
    context.user_data['opeak'] = float(update.message.text)
    await update.message.reply_text("""
Slope - the slope of the peak exercise ST segment
🔴 upsloping ➡️ 0
🔴 flat ➡️ 1
🔴 downsloping ➡️ 2

""")
    
    return SLOPE

async def get_slope_ask_nmv(update:Update, context:CallbackContext):
    context.user_data["slope"] = int(update.message.text)
    await update.message.reply_text('Enter no. of major vessels  within the range(0-3) colored by fluoroscopy')
    return NMV

async def get_nmv_ask_thal(update:Update, context:CallbackContext):
    context.user_data["nvm"] = int(update.message.text)
    await update.message.reply_text("""
Enter inter value for your thalassemia  type
🔴 normal ➡️ 0
🔴 fixed defect ➡️ 1
🔴 reversible defect ➡️ 2
""")

    return THAL

async def model_final_output(update:Update, context:CallbackContext):
    context.user_data['thal']  = int(update.message.text)

    input_data = dict(context.user_data).values()
    input_data = list(input_data)
    final_input = [
        input_data
    ]

    output = heart_classifier.predict(final_input)
    output_proba = heart_classifier.predict_proba(final_input)

    if output[0] == 1:
        await update.message.reply_text("You have higher chance of having heart disease!")
        await update.message.reply_text(f"Probability of you having a heart disease is {round(output_proba[0][1] * 100, 2)}%")
        await update.message.reply_text(f"Probability of you not having a heart disease is {round(output_proba[0][0] * 100, 2)}%")
    elif output[0] == 0:
        await update.message.reply_text("You have lower chance of having heart disease!")
        await update.message.reply_text(f"Probability of you having a heart disease is {round(output_proba[0][1] * 100, 2)}%")
        await update.message.reply_text(f"Probability of you not having a heart disease is {round(output_proba[0][0] * 100, 2)}%")
        await update.message.reply_text("These result might not be relevant, because the accuracy of this machine learning model is just 84 percent... We will strongly suggest you to take advice from experts🧑🏼‍⚕️")

    return ConversationHandler.END


async def cancel(update:Update, context:CallbackContext):
    await update.message.reply_text('Process cancelled!')
    return ConversationHandler.END


if __name__ == "__main__":
    app = ApplicationBuilder().token(bot_token).build()
    print("-> The bot is up! Check telegram bot to use the bot!")

    start_cmd_handler = CommandHandler('start', start)
    help_cmd_handler = CommandHandler('help', help)
    devinfo_cmd_handler = CommandHandler('devinfo', devinfo)
    para_descript_handler = CommandHandler('description', description)

    app.add_handler(start_cmd_handler)
    app.add_handler(help_cmd_handler)
    app.add_handler(devinfo_cmd_handler)
    app.add_handler(para_descript_handler)

    # conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("check_heart", check_heart)],
        states={
            AGE: [MessageHandler((filters.TEXT & ~filters.COMMAND), get_age_ask_sex)],
            SEX: [MessageHandler((filters.TEXT & ~filters.COMMAND), get_sex_ask_cpt)],
            CPT: [MessageHandler((filters.TEXT & ~filters.COMMAND), get_cpt_ask_rbp)],
            RBP: [MessageHandler((filters.TEXT & ~filters.COMMAND), get_rbp_ask_chol)],
            CHOL: [MessageHandler((filters.TEXT & ~filters.COMMAND), get_chol_ask_fbs)],
            FBS: [MessageHandler((filters.TEXT & ~filters.COMMAND), get_fbs_ask_recg)],
            RECG: [MessageHandler((filters.TEXT & ~filters.COMMAND), get_recg_ask_maxhr)],
            MAXHR: [MessageHandler((filters.TEXT & ~filters.COMMAND), get_maxhr_ask_exang)],
            EXANG: [MessageHandler((filters.TEXT & ~filters.COMMAND), get_exang_ask_opeak)],
            OPEAK: [MessageHandler((filters.TEXT & ~filters.COMMAND), get_opeak_ask_slope)],
            SLOPE: [MessageHandler((filters.TEXT & ~filters.COMMAND), get_slope_ask_nmv)],
            NMV: [MessageHandler((filters.TEXT & ~filters.COMMAND), get_nmv_ask_thal)],
            THAL: [MessageHandler((filters.TEXT & ~filters.COMMAND), model_final_output)]

        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )

    # adding the conversation handler to bot
    app.add_handler(conv_handler)

    app.run_polling()




