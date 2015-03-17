from .methods import clean_duplicate_players, clean_duplicate_alliances, clean_duplicate_castles
import celery


@celery.task
def clean_duplicates(*args, **kwargs):
    print "Clean castles..."
    clean_duplicate_castles()

    print "Clean players..."
    clean_duplicate_players()

    print "Clean alliances..."
    clean_duplicate_alliances()