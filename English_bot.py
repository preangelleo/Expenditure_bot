from GPT_functions import *


def st_find_ranks_for_word(key_word):
    engine = get_remote_db_connection()
    df = pd.DataFrame(engine.connect().execute(text(f"SELECT * FROM db_daily_words WHERE word = '{key_word}'")).fetchall())
    if df.empty: return 
    word_dict = df.iloc[0].to_dict()
    return word_dict
'''
{'id': 2524, 'word': 'happy', 'rank': 559, 'counts': 0, 'total_counts': 0, 'us-phonetic': '[ˈhæpi]', 'origin': 'The word "happy" comes from the Middle English word "hap" which means luck or chance. In Chinese, the word for happy is 高兴 (gāo xìng) which literally translates to "highly excited" or "pleased".', 'synonyms': 'cheerful(8003) | joyful(10551) | exuberant(14116) | blissful(17552) | jubilant(20243)', 'antonyms': None, 'tag': None, 'chinese': 'adj. 快乐的；幸福的、使人高兴的；满意的；乐意的；幸运的；合适的。comb. <非正式> 滥用……的', 'chat_gpt_explanation': '\nHappy is a feeling of joy, contentment, pleasure, or good fortune. It is a positive emotion that can be experienced in response to a variety of situations, including success, relationships, and activities.', 'note': '\n1. Joyful: feeling or expressing great pleasure and happiness.\n2. Cheerful: having a good disposition; being full of hope and courage.\n3. Jubilant: feeling or expressing great joy and triumph.\n4. Exuberant: joyously unrestrained; overflowing with enthusiasm.\n5. Blissful: supremely happy and contented.\n\nThe difference among these synonyms is the degree of happiness they express. Joyful and cheerful indicate mild pleasure, while jubilant and exuberant show more intense joy, and blissful is the highest level of happiness.', 'memo': None, 'toefl': 1, 'gre': 0, 'gmat': 0, 'sat': 0, 'scenario': None, 'mastered': 0, 'level': 1, 'sentence': None, 'last_check_time': None, 'youdao_synced': 0, 'manually_updated': 0, 'derivative': None, 'relevant': None, 'phrase': None, 'sealed': 1}
'''

'''class GptEnglishExplanation(Base):
    __tablename__ = 'gpt_english_explanation'

    id = Column(Integer, primary_key=True, autoincrement=True)
    word = Column(String(30))
    explanation = Column(Text)
    gpt_model = Column(String(30))
    update_time = Column(DateTime)
    '''


def find_words_for_bot_user(word:str, from_id=TG_BOT_OWNER_ID):
    word = word.lower()
    engine = get_remote_db_connection()

    df = pd.DataFrame(engine.connect().execute(text(f"SELECT * FROM db_daily_words WHERE word = '{word}'")).fetchall())
    if df.empty: return 

    word_dict = df.iloc[0].to_dict()
    word = word_dict.get('word', '')
    word_category = [key.upper() for key, value in word_dict.items() if value != 0 and key in ['toefl', 'gre', 'gmat', 'sat']]
    word_category_str = ' / '.join(word_category)
    word_trans = {
        '单词': word,
        '排名': word_dict.get('rank', ''),
        '发音': word_dict.get('us-phonetic', ''),
        '词库': word_category_str,
        '词意': word_dict.get('chinese', ''),
    }
    
    send_msg('\n'.join(f"{k}:\t {v}" for k, v in word_trans.items() if v), from_id)
    
    df = pd.DataFrame(engine.connect().execute(text(f"SELECT explanation FROM gpt_english_explanation WHERE word = '{word}'")).fetchall())
    if not df.empty: send_msg(df.iloc[0].to_dict().get('explanation', 'None'), from_id)
    else: 
        try: explanation = chat_gpt_english(word)
        except: return

        if explanation:
            new_record = {
                'word': word,
                'explanation': explanation,
                'gpt_model': DEFAULT_MODEL,
                'update_time': datetime.now()
            }
            df = pd.DataFrame([new_record])
            df.to_sql('gpt_english_explanation', engine, if_exists='append', index=False)
            print(f'New record added to gpt_english_explanation table: {word}')
            send_msg(explanation, from_id)
    
    return True


if __name__ == "__main__":
    print('English_bot.py is running ...')

    word = 'Laureate'
    word = 'creation'
    # df = pd.DataFrame(engine.connect().execute(text(f"SELECT explanation FROM gpt_english_explanation")).fetchall())
    # print(df)

    find_words_for_bot_user(word, from_id=TG_BOT_OWNER_ID)
