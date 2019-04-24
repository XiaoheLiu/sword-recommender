from reviews.models import Review, Sword
from random import randint
import pandas as pd


def save_review_from_row(sword_row):
    if sword_row.note != 'missing':
        review = Review()
        review.comment = sword_row.note
        review.author_id = randint(1, 4)
        review.sword_id = sword_row.name
        review.rating = randint(1, 5)
        review.save()


def run():
    df = pd.read_csv("./reviews/data/all_swords.csv")
    df['note'] = df['note'].fillna('missing')
    df.apply(save_review_from_row, axis=1)
    print('Saved reviews into database.')
