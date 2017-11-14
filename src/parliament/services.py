import os
from .models import ParliamentSession

def parliament_session_ids_by_parliament(parliament):
    return ParliamentSession.objects.filter(parliament=parliament).values_list('id', flat=True)

def get_parliament_sessions_to_look_at():
    PARLIAMENT_SESSIONS_TO_LOOK_AT = int(os.environ["PARLIAMENT_SESSIONS_TO_LOOK_AT"])
    return ParliamentSession.objects.all().order_by('-id')[
        :PARLIAMENT_SESSIONS_TO_LOOK_AT
    ]
