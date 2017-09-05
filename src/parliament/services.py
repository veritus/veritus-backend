from .models import Parliament, ParliamentSession

def parliament_session_ids_by_parliament(parliament):
    return ParliamentSession.objects.filter(parliament=parliament).values_list('id', flat=True)
