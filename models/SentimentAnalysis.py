# Import Google Cloud client的library
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types


def sentimentAnalysis(text):
    # 把client實體化
    client = language.LanguageServiceClient()

    # 準備要分析的句子
    # text = u'Absolutely one of the worst movies I\'ve ever had to sit through. Despicable characters, a drawn out storyline, and annoying dialogue made the enjoyable act of movie watching a chore.'
    document = types.Document(
        content=text,
        type=enums.Document.Type.PLAIN_TEXT)

    # 用api分析句子的情緒
    sentiment = client.analyze_sentiment(document=document).document_sentiment

    print('Text: {}'.format(text))
    print('Sentiment: {}, {}'.format(sentiment.score, sentiment.magnitude))

    result = {"score":sentiment.score, "magnitude":sentiment.magnitude}

    return result