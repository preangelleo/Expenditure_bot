from Binance_api import *
from Prompt_template import *
from GPT_functions import *

# aiogram 3.2.0
# https://docs.aiogram.dev/en/latest/index.html

import asyncio
import logging
import sys
import os
from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold

# Bot token can be obtained via https://t.me/BotFather
TOKEN = os.getenv('TELEGRAM_TOKEN')
bot = Bot(token=TOKEN)
TG_BOT_OWNER_ID = int(os.getenv('TG_BOT_OWNER_ID'))

# All handlers should be attached to the Router (or Dispatcher)
dp = Dispatcher()

# Define a handler for telegram messages
async def handel_telegram_message(message: types.Message):

    # If sender's chat_id is not TG_BOT_OWNER_ID, then ignore the message
    from_id = message.from_user.id
    text_prompt = message.text 
    image_url = None

    # Print out the message in json format with indent
    '''
    Input a text message and I got this message object:
    <class 'aiogram.types.message.Message'>
    message_id=5565 date=datetime.datetime(2023, 12, 7, 16, 43, 28, tzinfo=TzInfo(UTC)) chat=Chat(id=2118900665, type='private', title=None, username='laogege6', first_name='Old_Bro_Leo', last_name=None, is_forum=None, photo=None, active_usernames=None, emoji_status_custom_emoji_id=None, emoji_status_expiration_date=None, bio=None, has_private_forwards=None, has_restricted_voice_and_video_messages=None, join_to_send_messages=None, join_by_request=None, description=None, invite_link=None, pinned_message=None, permissions=None, slow_mode_delay=None, message_auto_delete_time=None, has_aggressive_anti_spam_enabled=None, has_hidden_members=None, has_protected_content=None, sticker_set_name=None, can_set_sticker_set=None, linked_chat_id=None, location=None) message_thread_id=None from_user=User(id=2118900665, is_bot=False, first_name='Old_Bro_Leo', last_name=None, username='laogege6', language_code='zh-hans', is_premium=True, added_to_attachment_menu=None, can_join_groups=None, can_read_all_group_messages=None, supports_inline_queries=None) sender_chat=None forward_from=None forward_from_chat=None forward_from_message_id=None forward_signature=None forward_sender_name=None forward_date=None is_topic_message=None is_automatic_forward=None reply_to_message=None via_bot=None edit_date=None has_protected_content=None media_group_id=None author_signature=None text='are you still there' entities=None animation=None audio=None document=None photo=None sticker=None story=None video=None video_note=None voice=None caption=None caption_entities=None has_media_spoiler=None contact=None dice=None game=None poll=None venue=None location=None new_chat_members=None left_chat_member=None new_chat_title=None new_chat_photo=None delete_chat_photo=None group_chat_created=None supergroup_chat_created=None channel_chat_created=None message_auto_delete_timer_changed=None migrate_to_chat_id=None migrate_from_chat_id=None pinned_message=None invoice=None successful_payment=None user_shared=None chat_shared=None connected_website=None write_access_allowed=None passport_data=None proximity_alert_triggered=None forum_topic_created=None forum_topic_edited=None forum_topic_closed=None forum_topic_reopened=None general_forum_topic_hidden=None general_forum_topic_unhidden=None video_chat_scheduled=None video_chat_started=None video_chat_ended=None video_chat_participants_invited=None web_app_data=None reply_markup=None'''
    
    # check if the message is a photo
    if message.photo:
        # if from_id != TG_BOT_OWNER_ID: return

        '''file_id='AgACAgUAAxkBAAIVx2Vx-uODMrGVAAEL5Q9U1d9w2ECsLAAC5rgxG5oKkFc2W-bswf4s-gEAAwIAA3gAAzME' file_unique_id='AQAD5rgxG5oKkFd9' width=800 height=620 file_size=117042'''
        '''File path: photos/file_53.jpg'''
        '''File url: https://api.telegram.org/file/bot6134874649:AAG6QrYOOD5tvU-3q1sKOBcyfW9LRnx7ZDQ/photos/file_53.jpg'''

        file_id = message.photo[-1].file_id  # get the file_id of the largest size photo
        file_info = await bot.get_file(file_id)  # get File object
        file_path = file_info.file_path  # get file_path from File object
        image_url = f"https://api.telegram.org/file/bot{TOKEN}/{file_path}"  # construct file url
        text_prompt = f"{message.caption}\n{text_prompt}"


    await run_conversation_with_functions(chat_id=from_id, model=DEFAULT_MODEL, image_url=image_url, prompt = text_prompt)

    