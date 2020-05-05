import os

class Config:
    CHANNEL_ACCESS_TOKEN = os.environ['CHANNEL_ACCESS_TOKEN']
    CHANNEL_SECRET = os.environ['CHANNEL_ACCESS_TOKEN']

    # CHANNEL_ACCESS_TOKEN = 'KNBx2StVKwtSjMOoAiwuqz2vkaMpLnpEOem8vyTvNZyYa2iW6qvtmTM63+/HyWSrf4/WcsSPjdDU7c26Sc4SINN1BG9xHo1NXJzskNLUksP581BcwuOa4ygXPvetGCyT2x8PdqhUA9Z2propI9qTvwdB04t89/1O/w1cDnyilFU='
    # CHANNEL_SECRET = '07c15d0ddedc668c91a1cd9fdbf9051e'

    BASE_ID = '@072oimpj'

    LINE_PAY_ID = os.environ['LINE_PAY_ID']
    LINE_PAY_SECRET = os.environ['LINE_PAY_SECRET']

    # LINE_PAY_ID = '1654151870'
    # LINE_PAY_SECRET = 'cdf067f352c0a9c097abea21e0279cb2'

    LIFF_URL = 'https://liff.line.me/1654173476-1re659nb'

    STORE_IMAGE_URL = 'https://i.imgur.com/igoTNFV.png'
