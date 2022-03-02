import pandas as pd


def clean_data(df):

    pd.options.mode.chained_assignment = None


    df = df[df['review-text'].notna()]
    df['review-text'] = df['review-text'].str.replace("<br />", " ")
    df['review-text'] = df['review-text'].str.replace("\[?\[.+?\]?\]", " ")
    df['review-text'] = df['review-text'].str.replace("\/{3,}", " ")
    df['review-text'] = df['review-text'].str.replace("\&\#.+\&\#\d+?;", " ")
    df['review-text'] = df['review-text'].str.replace("\d+\&\#\d+?;", " ")
    df['review-text'] = df['review-text'].str.replace("\&\#\d+?;", " ")

    #smileys und so weiter
    df['review-text'] = df['review-text'].str.replace("\:\|", "")
    df['review-text'] = df['review-text'].str.replace("\:\)", "")
    df['review-text'] = df['review-text'].str.replace("\:\(", "")
    df['review-text'] = df['review-text'].str.replace("\:\/", "")

    #leerzeichen nach .
    df['review-text'] = df['review-text'].str.replace(".", ". ")

    #mehrere spaces durch eins ersetzen
    df['review-text'] = df['review-text'].str.replace("\s{2,}", " ")


    df['review-text'] = df['review-text'].str.lower()



    return(df)
