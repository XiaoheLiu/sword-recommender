from reviews.models import Sword


def run():
    Sword.objects.all().delete()
    print("Deleted all swords from database.")
