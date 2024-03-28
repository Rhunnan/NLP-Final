from pygoogletranslation import Translator
import re
import pandas as pd
import requests
import nltk
from bs4 import BeautifulSoup
pd.set_option('display.max_colwidth', 500)
pd.set_option('display.width', 1000)



# Fetch the page content
banatNewsUrls = [
    "https://www.philstar.com/banat/showbiz/2024/03/24/2342878/kapamilya-stars-nangharos-sa-billboard-philippines",
    "https://www.philstar.com/banat/palaro/2024/03/28/2343931/flyboys-2008-reapers-2013-nanghawod-sa-last-dance",
    "https://www.philstar.com/banat/palaro/2024/03/28/2343929/barili-wa-gihapoy-pilde-sa-cabaron-cup-volleyball",
    "https://www.philstar.com/banat/palaro/2024/03/28/2343928/davis-mi-agak-sa-lakers-vs-bucks-sud-sa-2ot",
    "https://www.philstar.com/banat/palaro/2024/03/28/2343928/davis-mi-agak-sa-lakers-vs-bucks-sud-sa-2ot",
    "https://www.philstar.com/banat/balita/2024/03/27/2343629/napatay-sa-amahan",
    "https://www.philstar.com/banat/balita/2024/03/27/2343626/duha-ka-hvi-nga-pusher-sikop-sa-managlahing-buy-bust-operation",
    "https://www.philstar.com/banat/balita/2024/03/28/2343901/ccdrrmo-miduso-og-dugang-budget-aron-pagtabang-sa-mga-mag-uuma",
    "https://www.philstar.com/banat/palaro/2024/03/28/2343928/davis-mi-agak-sa-lakers-vs-bucks-sud-sa-2ot",
    "https://www.philstar.com/banat/opinyon/2024/03/28/2343922/editoryal-tama-na-lord"

]
#initializing the translator 
translator = Translator()
#translator na function try pako mangita pako other way na mas accurate ang translate for accurate sentiment mag check2 pakog aohter libraries or API
def translate_to_english(text):
    translation = translator.translate(text, src='ceb', dest='en')
    return translation


bisaya_text_corpus = []
english_text_from_bisaya_corpus = []
for i in range(len(banatNewsUrls)):
    response = requests.get(banatNewsUrls[i])
    html_content = response.text
    
# Parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

#Extracting all paragraphs within a specific div
    bisaya_texts = soup.select('div.article__writeup p')
    bisaya_text_corpus.extend(bisaya_texts)

#making a list sa bisaya nga mga txt nya convert to string kay mga tag type ni tungod kay returned gekan sa web scrape
index = 0
for bisayaText in bisaya_text_corpus:
    bisaya_text_corpus[index] = str(bisaya_text_corpus[index])
    index+=1
#diri na part is ang pag translate nako sa bisaya into a english language then himuon string ron maka gamit kos mga available libraries na nag tailor sa english na language
#since wala pamay mga libraries na ge make para sa bisaya na language. ako naman ge suwayan but dli ma lemmatize or kuha ang root word sa words kay dli
#suppoerted ang bisaya langauge sa stop words sa nltk og sa lemmatizer sa nltk
index = 0
for bisayaText in bisaya_text_corpus:
    translated = translate_to_english(bisaya_text_corpus[index])
    cleaned_translation = translated.text.replace("Translated(src=tl, dest=en, text=<p> <p>", "")
    english_text_from_bisaya_corpus.append(cleaned_translation)
    index+=1
    
# Extract and print ang english translted na text
# for text in english_text_from_bisaya_corpus :
#     print(text)

#buhat kog dictionary para sa dataFrame pero pwede raman sad i lahus ra 
data = {
    "Bisaya Review": bisaya_text_corpus,
    "Translated To English na Bisaya Review": english_text_from_bisaya_corpus
}
# df = pd.DataFrame([bisaya_text_corpus, english_text_from_bisaya_corpus], columns = ['Bisaya Reviews', 'Translated Reviews To English'])
df = pd.DataFrame(data)

print(df)

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')


#resseting the pd set ups to default
pd.set_option('display.max_colwidth', None)
pd.set_option('display.width', 600)

# my function to preprocess data that i web scrapre
def preprocess_text(text):
    word_tokens = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    filtered_text = [word for word in word_tokens if not re.match(r"^[a-zA-Z]\.$", word) and not re.match(r"^[a-zA-Z]$", word) and not re.match(r"[/<>_-]", word)]
    filtered_text = [word for word in filtered_text if word not in stop_words]
    lemmatizer = WordNetLemmatizer()
    lemmatized_text = [lemmatizer.lemmatize(word) for word in filtered_text]
    return lemmatized_text

# preprocessing_text
list_of_preprocessed_text = []
index = 0
for text in english_text_from_bisaya_corpus:
    preprocessed_text = preprocess_text(english_text_from_bisaya_corpus[index])
    list_of_preprocessed_text.append(preprocessed_text)
    index+=1

#making a duplicate of the preprocessed bisaya text but made it as a string so that i could represent it in a dataframe
list_of_preprocessed_text_for_df = list_of_preprocessed_text
index = 0
for Text in list_of_preprocessed_text:
    list_of_preprocessed_text_for_df[index] = str(list_of_preprocessed_text[index])
    index+=1
dfPreprocessedText = pd.DataFrame(list_of_preprocessed_text_for_df, columns = ["Pre-Processed-Text"])
index = 0
# print("List of every Tokenized or preprocessed index translated english text")
# for Text in list_of_preprocessed_text:
#     print(list_of_preprocessed_text[index])
#     index+=1
print(dfPreprocessedText)