from promises.models import Promise, PromiseBill, SuggestedPromiseBill
from bill_gather.models import Bill, Parliament, ParliamentSession
from tags.models import Tag, BillTags, PromiseTags

def find_connected_bills_and_promises():
    current_parliament = Parliament.objects.all().order_by('-id')[0]
    parliament_sessions = ParliamentSession.objects.filter(parliament=current_parliament)
    current_promises = Promise.objects.filter(parliament=current_parliament)

    for parliament_session in parliament_sessions:
        session_bills = Bill.objects.filter(session=parliament_session)

