import re
import string
from emot.emo_unicode import UNICODE_EMO, EMOTICONS
import re


"""https://viblo.asia/p/hieu-ve-regular-expression-xu-ly-ngon-ngu-tu-nhien-don-gian-hon-voi-python-WAyK8L7NKxX"""

REGEX = {
    "url": 'https?:\/\/[^\s]*',
    "datetime": '\d{1,2}\s?[:/-]\s?\d{1,2}\s?[:/-]\s?\d{4}' \
                '|\d{1,2}\s?[:/-]\s?\d{4}' \
                '|\d{1,2}\s?[:/-]\s?\d{1,2}' \
                '|\d{4}',
    "email": '[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+.[a-zA-Z0-9-.]+',
    "real_number": '\d+[\.,]\d+',
    "fraction": '\d+\/\d+',
}


MONEYTAG = [u'k', u'đ', u'ngàn', u'nghìn', u'usd', 
            u'tr', u'củ', u'triệu', u'yên', u'tỷ', 
            u'tỉ', u'$', u'đô']


def preprocess_money(text):
  for money in MONEYTAG:
    text = re.sub(u'(^|\s)\d*([,.]?\d+)+\s*' + money, 'monney', text)
  text = re.sub('((^|\s)(\d+\s*\$)|((^|\s)\$\d+\s*))', 'monney', text)
  return text


def preprocess_syllable_repeat(text):
    return re.sub(r'(\D)\1+', r'\1', text)


def preprocess_regex(text, regex_type):
    return re.sub(REGEX[regex_type], regex_type, text)


""""""


def apply_dictionary(text, dictionary):
    splited_text = text.split()
    for i in range(len(splited_text)):
        if splited_text[i] in dictionary:
            splited_text[i] = dictionary[splited_text[i]]
    return " ".join(splited_text)


def replace_str(string, i, j, new_str):
    return string[:i] + new_str + string[j:]


def preprocess_punctuation(text, removal=False):
    for i in range(len(text)):
        if text[i] in string.punctuation:
            if removal:
                text[i] = " "
                continue
            new_c = text[i]
            if i != 0 and text[i-1] != " ":
                new_c = " " + new_c
            if i != len(text)-1 and text[i+1] != " ":
                new_c += " "
            if new_c != text[i]:
                text = replace_str(text, i, i+1, new_c)
    return text


"""https://towardsdatascience.com/text-preprocessing-for-data-scientist-3d2419c8199d"""


def preprocess_emojis(text, removal=False):
  for emot in UNICODE_EMO:
    if removal:
        text = text.replace(emot, " ")
        continue
    text = text.replace(emot, "_".join(UNICODE_EMO[emot].replace(",","").replace(":","").split()))
  return text


def preprocess_emoticons(text, removal=False):
  for emot in EMOTICONS:
    if removal:
        text = text.replace(emot, " ")
        continue
    text = re.sub(u'('+emot+')', "_".join(EMOTICONS[emot].replace(",","").split()), text)
  return text

TIME_TAG = {u'h':' giờ', u'p': ' phút', u's': 'giây'}
def preprocess_time(text):
  for k,v in TIME_TAG.items():
    time = re.compile(r'\d+([\.,]\d+){0,1}'+k)
    if time.search(text) is not None:
      text = re.sub(u'\d+([\.,]\d+){0,1}' + k, time.search(text).group().rstrip('h')+v, text)
  
  return text



""""""


syllables = {'òa': 'oà', 'óa': 'oá', 'ỏa': 'oả', 'õa': 'oã', 'ọa': 'oạ', 'òe': 'oè', 'óe': 'oé', 'ỏe': 'oẻ',
             'õe': 'oẽ', 'ọe': 'oẹ', 'ùy': 'uỳ', 'úy': 'uý', 'ủy': 'uỷ', 'ũy': 'uỹ', 'ụy': 'uỵ', 'uả': 'ủa',
             'ả': 'ả', 'ố': 'ố', 'u´': 'ố', 'ỗ': 'ỗ', 'ồ': 'ồ', 'ổ': 'ổ', 'ấ': 'ấ', 'ẫ': 'ẫ', 'ẩ': 'ẩ',
             'ầ': 'ầ', 'ỏ': 'ỏ', 'ề': 'ề', 'ễ': 'ễ', 'ắ': 'ắ', 'ủ': 'ủ', 'ế': 'ế', 'ở': 'ở', 'ỉ': 'ỉ',
             'ẻ': 'ẻ', 'àk': u' à ', 'aˋ': 'à', 'iˋ': 'ì', 'ă´': 'ắ', 'ử': 'ử', 'e˜': 'ẽ', 'y˜': 'ỹ', 'a´': 'á'}

sentiment_words = {# Chuẩn hóa 1 số sentiment words/English words
                    ':))': '  positive ', '🙂': ' positive ', '😊': ' positive ', 'ô kêi': ' ok ', 'okie': ' ok ', ' o kê ': ' ok ',
                    'okey': ' ok ', 'ôkê': ' ok ', 'oki': ' ok ', ' oke ': ' ok ', ' okay': ' ok ', 'okê': ' ok ',
                    ' tks ': u' cám ơn ', 'thks': u' cám ơn ', 'thanks': u' cám ơn ', 'ths': u' cám ơn ', 'thank': u' cám ơn ',
                    '⭐': 'star ', '*': 'star ', '🌟': 'star ', '🎉': u' positive ',
                    'kg ': u' không ', 'not': u' không ', u' kg ': u' không ', '"k ': u' không ', ' kh ': u' không ',
                    'kô': u' không ', 'hok': u' không ', ' kp ': u' không phải ', u' kô ': u' không ', '"ko ': u' không ',
                    u' ko ': u' không ', u' k ': u' không ', 'khong': u' không ', u' hok ': u' không ',
                    'he he': ' positive ', 'hehe': ' positive ', 'hihi': ' positive ', 'haha': ' positive ', 'hjhj': ' positive ',
                    ' lol ': ' nagative ', ' cc ': ' nagative ', 'cute': u' dễ thương ', 'huhu': ' nagative ', ' vs ': u' với ',
                    'wa': ' quá ', 'wá': u' quá', 'j': u' gì ', 'dì': u' gì ', '“': ' ',
                    ' sz ': u' cỡ ', 'size': u' cỡ ', u' đx ': u' được ', 'dk': u' được ', 'dc': u' được ', 'đk': u' được ',
                    'đc': u' được ', 'authentic': u' chuẩn chính hãng ', u' aut ': u' chuẩn chính hãng ',
                    u' auth ': u' chuẩn chính hãng ', 'thick': u' positive ', 'store': u' cửa hàng ',
                    'shop': u' cửa hàng ', 'spen': 'spen', 'sp': u' sản phẩm ', 'gud': u' tốt ', 'god': u' tốt ', 'wel done': ' tốt ',
                    'good': u' tốt ', 'gút': u' tốt ',
                    'sấu': u' xấu ', 'gut': u' tốt ', u' tot ': u' tốt ', u' nice ': u' tốt ', 'perfect': 'rất tốt',
                    'bt': u' bình thường ','dùg': u'dùng','tìh': u'tình','tjh': u'tình',
                    'time': u' thời gian ', 'qá': u' quá ', u' ship ': u' giao hàng ', u' m ': u' mình ', u' mik ': u' mình ',
                    'ể': 'ể', 'product': 'sản phẩm', 'quality': 'chất lượng', 'chat': ' chất ', 'excelent': 'hoàn hảo',
                    'bad': 'tệ', 'fresh': ' tươi ', 'sad': ' tệ ',
                    'date': u' hạn sử dụng ', 'hsd': u' hạn sử dụng ', 'quickly': u' nhanh ', 'quick': u' nhanh ',
                    'fast': u' nhanh ', 'delivery': u' giao hàng ', u' síp ': u' giao hàng ',
                    'beautiful': u' đẹp tuyệt vời ', u' r ': u' rồi ', u' shopE ': u' cửa hàng ',
                    u' order ': u' đặt hàng ',
                    'chất lg': u' chất lượng ', u' sd ': u' sử dụng ', u' dt ': u' điện thoại ', u' nt ': u' nhắn tin ',
                    u' tl ': u' trả lời ', u' sài ': u' xài ', u'bjo': u' bao giờ ',
                    'thik': u' thích ', u' sop ': u' cửa hàng ', ' fb ': ' facebook ', ' face ': ' facebook ', ' very ': u' rất ',
                    u'quả ng ': u' quảng  ',
                    'dep': u' đẹp ', u' xau ': u' xấu ', 'delicious': u' ngon ', u'hàg': u' hàng ', u'qủa': u' quả ',
                    'iu': u' yêu ', 'fake': u' giả mạo ', 'trl': 'trả lời', '><': u' positive ',
                    ' por ': u' tệ ', ' poor ': u' tệ ', 'ib': u' nhắn tin ', 'rep': u' trả lời ', u'fback': ' feedback ',
                    'fedback': ' feedback ',
                    # dưới 3* quy về 1*, trên 3* quy về 5*
                    '6 sao': ' 5star ', '6 star': ' 5star ', '5star': ' 5star ', '5 sao': ' 5star ', '5sao': ' 5star ',
                    'starstarstarstarstar': ' 5star ', '1 sao': ' 1star ', '1sao': ' 1star ', '2 sao': ' 1star ', '2sao': ' 1star ',
                    '2 starstar': ' 1star ', '1star': ' 1star ', '0 sao': ' 1star ', '0star': ' 1star ',
                    ').': ') .'}


def preprocess(data):
    # to lower:
    data = map(lambda x: x.lower(), data)
    # applies dicts:
    for k, v in syllables.items():
      data = map(lambda x: x.replace(k, v), list(data))
    for k, v in sentiment_words.items():
      data = map(lambda x: x.replace(k, v), list(data))

    # processes time
    data = map(lambda x: preprocess_time(x), list(data))
    # processes emojis:
    # data = map(lambda x: preprocess_emoticons(x), list(data))
    data = map(lambda x: preprocess_emojis(x), list(data))
    # processes money:
    data = map(lambda x: preprocess_money(x), list(data))

    # processes syllable repeat:
    data = map(lambda x: preprocess_syllable_repeat(x), list(data))
    # processes all other types of regex
    for regex in REGEX:
        data = map(lambda x: preprocess_regex(x, regex), list(data))
    # removes abundant characters:
    data = map(lambda x: x.replace(u'"', u' '), list(data))
    data = map(lambda x: x.replace(u'️', u''), list(data))
    data = map(lambda x: x.replace('🏻', ''), list(data))
    data = map(lambda x: preprocess_punctuation(x), list(data))
    # data = map(lambda x: ViTokenizer.tokenize(x), list(data))
    return list(data)
