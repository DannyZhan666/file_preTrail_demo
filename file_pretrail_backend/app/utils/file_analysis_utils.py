import json
import os
import pickle
import random
import re

import fitz
import numpy as np
import pandas as pd
import pdfplumber
from dotenv import load_dotenv
from transformers import AutoModelForSequenceClassification, AutoTokenizer, TextClassificationPipeline

load_dotenv()

ALL_PATTERN = os.environ["ALL_PATTERN"]
TEXT_PATTERN = os.environ["TEXT_PATTERN"]
TEXT_FREQ_THRESHOLD = os.environ["TEXT_FREQ_THRESHOLD"]
NUMERIC_RE_PATTERN = os.environ["NUMERIC_RE_PATTERN"]
NUMERIC_SELECT_PATTERN = os.environ["NUMERIC_SELECT_PATTERN"]
NUMERIC_LENGTHTHRESHOLD = os.environ["NUMERIC_LENGTHTHRESHOLD"]
STOP_WORDS_FN = os.environ["STOP_WORDS_FN"]
SELECT_WORD_FILE = os.environ["SELECT_WORD_FILE"]
MODEL_PATH = os.environ["MODEL_PATH"]
SELECT_COLS = os.environ["SELECT_COLS"].split('|')


### sec 0 : 分段，分句，读取合同
def get_special_condition_starting_page_index_new(file_name):
    with pdfplumber.open(file_name) as pdf:
        ## 有时候第一页不是正式合同，所以需要定位第一页 -- 假设special condition都是跟在正式合同后面
        ## 这里不包含special condition全部出现在前面的情况
        start_idx = 0
        while start_idx < 500:
            cur_text = pdf.pages[start_idx]
            if "BREACH OF COPYRIGHT MAY RESULT IN LEGAL ACTION" in cur_text.extract_text():
                break
            else:
                start_idx += 1
        for i in range(start_idx, 200):
            try:
                text = pdf.pages[i]
                if "BREACH OF COPYRIGHT MAY RESULT IN LEGAL ACTION" not in text.extract_text():
                    return i
                # demo.append(str(re.findall(r'(\d+\.\s.*\n?)+', clean_text.extract_text())).replace('[]', ' '))
            except:
                return np.nan


def get_intact_paragraph(all_text, page_numbers):
    source_text = all_text.split('SPLIT_ANCHOR_RE')[::-1]
    source_text = [at for at in source_text if pd.notnull(at) and len(re.sub('[^a-zA-Z]+', '', at)) > 0]

    new_text = []  # 用于存储合并后的段落
    current_page = page_numbers + 1  # 用于记录当前段落的页码

    # 遍历拆分后的文本并合并
    while len(source_text) > 1:
        cur_sentence = source_text.pop()
        cur_sentence_clean = re.sub('[^a-zA-Z]+', '', cur_sentence)

        # 如果当前段落是以大写字母开头，说明它是新段落，直接加入
        if cur_sentence_clean[0].isupper():
            # 查找所有的 [PAGE_*] 角标
            page_tags = re.findall(r'\[PAGE_(\d+)\]', cur_sentence)
            if page_tags:
                new_text.append((cur_sentence, current_page))
                current_page += len(page_tags)
            else:
                new_text.append((cur_sentence, current_page))

        else:
            # 否则合并与上一段落
            previous_para, previous_page = new_text.pop()
            new_text.append(((previous_para + ' ' + cur_sentence), previous_page))

    # 处理文本合并后存储
    return new_text


def get_all_text(filename, doc, start_page_index, end_page_est=10):
    end_page_index = start_page_index + end_page_est
    all_text_ls = []
    page_numbers = []  # 用来记录每个段落的页码
    next_page = start_page_index  # 用来标记当前页
    for cur_pg_num in range(start_page_index, end_page_index):
        try:
            # 获取当前页文本并替换换行符
            cur_paragraphs = doc.load_page(cur_pg_num).get_text().replace("\n", " ")
            # 为当前页添加角标
            cur_paragraphs = cur_paragraphs + f"[PAGE_{next_page}] "
            all_text_ls.append(cur_paragraphs)
            page_numbers.append(next_page)  # 记录页码
            next_page += 1  # 增加页码
        except:
            pass
    # print(len(all_text_ls))
    # print(all_text_ls)
    all_text = " ".join(all_text_ls)
    # print(all_text)
    # 正则表达式匹配段落编号
    re_patn = "(?<![^\s>｜^\(])([0-9]+)(\. |\) )"  ## 基于上面的改进
    all_para_nums = re.findall(re_patn, all_text)
    all_para_nums = [''.join(list(i)) for i in all_para_nums]
    ### temporaty solution, sometimes will replace 18.3. by the 3. if 3. exists
    # 解决偶尔替换编号问题
    all_para_nums_start_with_space = [" " + a for a in all_para_nums]
    all_para_nums_start_with_bracket = ["(" + b for b in all_para_nums]
    # 用 SPLIT_ANCHOR_RE 替换段落编号
    for para_num in (all_para_nums_start_with_space + all_para_nums_start_with_bracket):
        all_text = all_text.replace(para_num, "SPLIT_ANCHOR_RE")

    ### combine all text :有时候段落中也会有一些类似段落符的字，
    ### 这时候需要把他们合并，比如clause need fourteen（14） days，这里这个（14）还是会被检索到，然后变成分隔符

    # 调用 get_intact_paragraph 函数进行段落合并
    all_text_combine = get_intact_paragraph(all_text, start_page_index)
    print(all_text_combine)
    try:
        cur_df = pd.DataFrame(all_text_combine, columns=['paragraph', 'page_num'])
    except Exception as e:
        print("DataFrame构造失败：", e)
    # cur_df = pd.DataFrame(np.array(all_text.split('SPLIT_ANCHOR_RE')),columns = ['paragraph'])
    cur_df['file_name'] = filename
    return cur_df


### sec 1 : 这一部分专门来处理文本或者数字的关键字
def load_stopwords(fname):
    with open(fname, 'rb') as f:
        stopwords = pickle.load(f)
    return stopwords


def get_kw_freq(content, re_pt):
    kw_ls = [i.strip() for k in content for i in re.sub(re_pt, ' ', k).lower().split(" ") if len(i.strip()) > 1]
    kw_dict = {}
    for kw in kw_ls:
        if kw in kw_dict.keys():
            kw_dict[kw] += 1
        else:
            kw_dict[kw] = 1
    kw_dict_df = pd.DataFrame.from_dict(sorted(kw_dict.items(), key=lambda x: x[-1], reverse=True))
    kw_dict_df.columns = ['kw', 'count']
    return kw_dict_df


def get_selected_keywords(content):
    ### LOAD STOPWORDS
    all_stopwords = load_stopwords(STOP_WORDS_FN)
    ### 1. 只弄文字
    pure_text_kw_df = get_kw_freq(content, TEXT_PATTERN)
    ### 2. 只弄数字
    numeric_kw_df = get_kw_freq(content, NUMERIC_RE_PATTERN)
    ###文字
    kept_words = list(pure_text_kw_df[(~pure_text_kw_df['kw'].isin(all_stopwords))
                                      & (pure_text_kw_df['count'] > TEXT_FREQ_THRESHOLD)]['kw'].values)

    ###数字
    kept_kw_num = list(numeric_kw_df[(numeric_kw_df['kw'].str.contains(NUMERIC_SELECT_PATTERN))
                                     | (numeric_kw_df['kw'].map(len) <= NUMERIC_LENGTHTHRESHOLD)]['kw'].values)

    return kept_words + kept_kw_num


### sec 2 : 这一部分是清理文本数据
def load_kept_word(fn=SELECT_WORD_FILE):
    with open(fn, 'rb') as f:
        all_kept_kw = pickle.load(f)
    return all_kept_kw


def select_kept_word(sentence, selected_keywords):
    cur_sent = [i.lower().strip() for i in re.sub(ALL_PATTERN, ' ', sentence).lower().split(" ")]
    cur_sent = [i for i in cur_sent if len(i) > 1 and i in selected_keywords]
    return ' '.join(cur_sent)


### sec 3: 加载模型
def load_model(model_path=MODEL_PATH):
    fine_tune_sentiment_model = AutoModelForSequenceClassification.from_pretrained(model_path)
    fine_tune_tokenizer = AutoTokenizer.from_pretrained(model_path)
    fine_tune_pipeline = TextClassificationPipeline(model=fine_tune_sentiment_model,
                                                    tokenizer=fine_tune_tokenizer, return_all_scores=True)
    return fine_tune_pipeline


def get_pred_result(rlt):
    return '|'.join([i['label'] for i in rlt[0] if i['score'] > 0.5])


def predict_pdf_chunk(local_pdf_file):
    with fitz.open(local_pdf_file, filetype="pdf") as doc:
        start_page = get_special_condition_starting_page_index_new(local_pdf_file)
        cur_pdf = get_all_text(local_pdf_file, doc, start_page)
        all_kept_kw = load_kept_word()
        cur_pdf['paragraph'] = cur_pdf['paragraph'].apply(
            lambda x: ' '.join([i.lower().strip() for i in re.sub(ALL_PATTERN, ' ', x).lower().split(" ")]))
        cur_pdf['paragraph_clean'] = cur_pdf['paragraph'].apply(lambda x: select_kept_word(x, all_kept_kw))
        model = load_model()
        cur_pdf['model_predict_details'] = cur_pdf['paragraph_clean'].apply(lambda x: model.predict(x))
        cur_pdf['model_predict_labels'] = cur_pdf['model_predict_details'].apply(lambda x: get_pred_result(x))
        return cur_pdf[SELECT_COLS]


def predict_chunk(cur_path):
    choices = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
    cur_results = []
    with pdfplumber.open(cur_path) as pdf:
        length_pdf = len(pdf.pages)
        for l in range(length_pdf):
            cur_rt = get_random_time()
            cur_pred = []
            for _ in range(cur_rt):
                cur_pred.append(random.choice(choices))
            cur_rlt = ['chunk_%d' % l, '|'.join(cur_pred)]
            cur_results.append(cur_rlt)
    return cur_results


def get_random_time():
    return random.randint(1, 5)


def get_response(prompt, client, MODEL_NAME):
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": "You are a highly experienced and professional Conveyancer of Australia, who specializing in reviewing property contract"
            },
            {
                "role": "user",
                "content": prompt
            }],
        temperature=0
    )

    return response.choices[0].message.content


def load_review_items(file_name):
    with open(os.path.join(file_name)) as f:
        return json.load(f)


def chunk_text(text: list, chunk_size: int = 30, overlap_size: int = 5) -> list[str]:
    """
    将长文本按指定长度分割为多个chunk，支持重叠部分。

    参数:
        text (str): 原始文本
        chunk_size (int): 每个chunk最大长度
        overlap_size (int): 相邻chunk重叠字符数

    返回:
        list[str]: 分割后的chunk列表
    """
    if chunk_size <= overlap_size:
        raise ValueError("chunk_size 必须大于 overlap_size")

    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = min(start + chunk_size, text_length)
        chunks.append(text[start:end])
        start += chunk_size - overlap_size
    return chunks


def clean_paragraphs(paragraphs, chunk_size=30, overlap_window=5):
    cur_cleaned_text_chunks = []
    for paragraph in paragraphs:
        cur_text = [i.lower().strip() for i in paragraph.split()]
        cur_text = [i for i in cur_text if len(i) > 0]
        # cur_text_chunk = chunk_text(cur_text)
        cur_cleaned_text_chunks.append(cur_text)
    return cur_cleaned_text_chunks


def get_all_text_new(doc, start_page_index, end_page_est=15):
    end_page_index = start_page_index + end_page_est
    all_chunk_sentences = []
    for cur_pg_num in range(start_page_index, end_page_index):
        try:
            cur_paragraphs = doc.load_page(cur_pg_num).get_text().split("\n")
            all_chunk_sentences += clean_paragraphs(cur_paragraphs)
        except:
            pass
    return all_chunk_sentences
