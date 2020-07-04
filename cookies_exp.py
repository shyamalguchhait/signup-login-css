from datetime import datetime, timedelta

expires0=datetime.now()
expires0=expires0+timedelta(days=90)

def expires():
    return expires0
