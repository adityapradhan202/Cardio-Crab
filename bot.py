from telegram import Update
from telegram.ext import ConversationHandler
from telegram.ext import ContextTypes, CallbackContext
from telegram.ext import CommandHandler
from telegram.ext import ApplicationBuilder

import dotenv
import os

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

You'll need some data from the medical reports before checking your heart health. And to check the list of data that you need use -> /parameters_description
To check your heart health use -> /check_heart_health

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

async def parameters_description(update:Update, context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(parameters_description_text)

async def get_bot_invite_link(update:Update, context:ContextTypes.DEFAULT_TYPE):
    inv_link = 't.me/Cardio_Crab_Bot'
    await update.message.reply_text(f"Invitation link of the bot - {inv_link}")
    await update.message.reply_text('Share this link among people so that they can know there heart health too 👍')


if __name__ == "__main__":
    app = ApplicationBuilder().token(bot_token).build()
    print("-> The bot is up! Check telegram bot to use the bot!")

    start_cmd_handler = CommandHandler('start', start)
    help_cmd_handler = CommandHandler('help', help)
    devinfo_cmd_handler = CommandHandler('devinfo', devinfo)
    para_descript_handler = CommandHandler('parameters_description', parameters_description)

    app.add_handler(start_cmd_handler)
    app.add_handler(help_cmd_handler)
    app.add_handler(devinfo_cmd_handler)
    app.add_handler(para_descript_handler)

    app.run_polling()




