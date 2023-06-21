import copy
import numpy as np
import string
import pymorphy2
import nltk
import tqdm


class LuhnSummarizer:
    def __init__(self):
        self.morph = pymorphy2.MorphAnalyzer()
        self.lemmatizer = nltk.stem.WordNetLemmatizer()

    def process_text(self, data):
        language = self.__find_text_language(data)
        result = self.__get_dict_from_text(data)
        sentences = self.__split_to_sentences(data, language)
        scores = dict()
        for i in range(len(sentences)):
            scores[i] = self.__find_sentence_score(sentences[i], result, language)
        best_sentences = {k: v for k, v in sorted(scores.items(), key=lambda item: item[1], reverse=True)}
        summary = ''
        for sentence in list(best_sentences.items())[:5]:
            summary += data.split('.')[sentence[0]] + '.'
        summary = summary.replace('\n', '')

        return summary

    def __split_to_words(self, text, mode='ru'):
        allowed_symbols = string.ascii_letters + '-'
        for letter in text:
            if mode == 'ru':
                allowed_symbols = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ' + '-'
            if letter not in allowed_symbols:
                text = text.replace(letter, ' ')

        return text.lower().split()

    def __split_to_sentences(self, text, mode='ru'):
        allowed_symbols = string.ascii_letters + '-' + '.'
        for sign in ';!?\n':
            text.replace(sign, '.')
        for letter in text:
            if mode == 'ru':
                allowed_symbols = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ' + '-' + '.'
            if letter not in allowed_symbols:
                text = text.replace(letter, ' ')

        return text.lower().split('.')

    def __find_text_language(self, text):
        en = 0
        ru = 0
        for letter in text:
            if letter in 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ':
                ru += 1
            if letter in string.ascii_letters:
                en += 1
        return 'ru' if ru > en else 'en'

    def __normalize_word(self, word):
        language = self.__find_text_language(word)
        if language == 'ru':
            morph = pymorphy2.MorphAnalyzer()
            word = morph.parse(word)[0].normal_form
        else:
            lemmatizer = nltk.stem.WordNetLemmatizer()
            word = lemmatizer.lemmatize(word)
        return word

    def __normalize_word_fast(self, word):
        mode = self.__find_text_language(word)
        if mode == 'ru':
            word = self.morph.parse(word)[0].normal_form
        else:
            word = self.lemmatizer.lemmatize(word)
        return word

    def __get_dict_from_text(self, text):
        language = self.__find_text_language(text)
        words = self.__split_to_words(text, language)
        words_dict = dict()
        words = list(tqdm.tqdm(map(self.__normalize_word_fast, words)))
        with open('../plugins/common_english_words.txt', 'r', encoding='utf-8') as w:
            english_words = w.read()
        with open('../plugins/common_russian_words.txt', 'r', encoding='utf-8') as w:
            russian_words = w.read()
        english_words = english_words.lower().split('\n')
        russian_words = russian_words.lower().split('\n')
        words = [item for item in words if item not in english_words + russian_words]
        for i in tqdm.tqdm(range(len(words))):
            if words_dict.get(words[i]) is None:
                words_dict[words[i]] = 1
            else:
                words_dict[words[i]] += 1
        words_dict = {k: v for k, v in sorted(words_dict.items(), key=lambda item: item[1])}
        words_dict_copy = copy.deepcopy(words_dict)
        for k, v in words_dict_copy.items():
            if v <= 3:
                words_dict.pop(k)

        return words_dict

    def __find_sentence_score(self, sentence, result, mode='ru'):
        sentence = self.__split_to_words(sentence, mode)
        sentence_bin = []
        for i in range(len(sentence)):
            if sentence[i] in result:
                sentence_bin.append(1)
            else:
                sentence_bin.append(0)
        part_len = 0
        significant_words = 0
        insignificant_words = 0
        parts_score = [0]
        for num in sentence_bin:
            if num == 1:
                if part_len == 0:
                    part_len += 1
                else:
                    part_len += 1
                    part_len += insignificant_words
                    insignificant_words = 0
                significant_words += 1
            else:
                if part_len > 0:
                    if insignificant_words == 4:
                        insignificant_words = 0
                        parts_score.append(significant_words ** 2 / part_len)
                        significant_words = 0
                        part_len = 0
                    else:
                        insignificant_words += 1

        return max(parts_score)
