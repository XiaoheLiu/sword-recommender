import pandas as pd
from re import sub
from decimal import Decimal
from reviews.models import Sword


def parse_price(price):
    return Decimal(sub(r'[^\d.]', '', price))


def save_sword_from_row(sword_row):
    sword = Sword()
    sword.id = sword_row.name
    sword.name = sword_row.model
    sword.link = sword_row.link
    sword.manufacturer = sword_row.manufacturer
    sword.price = parse_price(sword_row.price)
    sword.sword_type = sword_row.sword_type
    sword.weight = sword_row.weight
    sword.overall_length = sword_row.overall_length
    sword.tip_type = sword_row.tip_type
    sword.save()


def run():
    df = pd.read_csv("./reviews/data/all_swords.csv")
    df = df.fillna('missing')
    df.apply(save_sword_from_row, axis=1)
    print('Saved all sword data into database.')
