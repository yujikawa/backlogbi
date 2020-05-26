from janome.tokenizer import Tokenizer
from wordcloud import WordCloud
import numpy as np


def word_clound_output(text_array: np.ndarray) -> WordCloud:
    words = []
    t = Tokenizer()
    for text in text_array:
        tokens = t.tokenize(text)
        for token in tokens:
            if token.part_of_speech.split(',')[0] == '名詞':
                text = token.base_form
                text = text.lower()
                words.append(text)
    text = ' '.join(words)
    fpath = "fonts/RictyDiminished-Bold.ttf"
    wordcloud = WordCloud(background_color="white",
                          font_path=fpath, width=640, height=400).generate(text)
    return wordcloud
