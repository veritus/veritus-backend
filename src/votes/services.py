import logging
import case_gather.soupUtils as soupUtils
from case_gather.models import Case
from parliament.models import ParliamentMember
from .models import VoteRecord, Vote
import main.sentryLogger as SentryLogger

CRONLOGGER = logging.getLogger('cronJobs')

def get_votes_by_parliament_session(parliament_session_number):
    '''
        We scrape the overall vote records for the parliament session
        and save them as a VoteRecord.
        Then we go to the details page to see what each individual
        parliament member voted and save them as a Vote
    '''
    CRONLOGGER.info(parliament_session_number)
    link = "http://www.althingi.is/altext/xml/atkvaedagreidslur/?lthing="
    details_link = "http://www.althingi.is/altext/xml/atkvaedagreidslur/atkvaedagreidsla/?numer="
    votes_soup = soupUtils.getSoupFromLink(link + str(parliament_session_number))
    vote_records = collect_vote_records(votes_soup)
    for vote_record in vote_records:
        VoteRecord.objects.create(
            case = vote_record.case,
            althingi_id = vote_record.althingi_id,
            yes = vote_record.number_of_yes,
            no = vote_record.number_of_no,
            didNotVote = vote_record.number_of_did_not_vote,
            althingi_result = vote_record.althingi_result,
        )
        vote_details_soup = soupUtils.getSoupFromLink(details_link + str(vote_record.althingi_id))
        parliament_member_votes = get_parliament_member_votes(vote_details_soup)
        for parliament_member_vote in parliament_member_votes:
            try: 
                parliament_member = ParliamentMember.objects.get(
                    name = parliament_member_vote['nafn']
                )
                Vote.objects.create(
                    parliament_member=parliament_member,
                    althingi_result=parliament_member_vote['atkvæði']
                )
            except DoesNotExist:
                SentryLogger.logToSentry('ParliamentMember not found: ' + parliament_member_vote['nafn'])
                raise


def collect_vote_records(soup):
    vote_records = []
    for vote_record in get_all_votes(soup):
        case_number = get_case_number(vote_record)
        case = Case.objects.get(
            number=case_number,
            parliament_session=parliament_session_number,
        )
        vote_overview = get_vote_overview(vote_record)
        
        vote = {
            'case': case,
            'althingi_id': get_althingi_id(vote_record),
            'number_of_yes': get_number_of_votes("já", vote_overview),
            'number_of_no': get_number_of_votes("nei", vote_overview),
            'number_of_did_not_vote': get_number_of_votes("greiðirekkiatkvæði", vote_overview),
            'althingi_result': get_althingi_result(vote_overview),
        }
        vote_records.append(vote)
        
    return vote_records
        

def get_all_votes(soup):
    """
        Takes in a soup and returns all <atkvæðagreiðsla><atkvæðagreiðsla> tags
    """
    return soup.find_all('atkvæðagreiðsla')

def get_case_number(vote_record_soup):
    return vote_record_soup['málsnúmer']

def get_althingi_id(vote_record_soup):
    return vote_record_soup['atkvæðagreiðslunúmer']

def get_vote_overview(vote_record_soup):
    return vote_record_soup.find('samantekt')

def get_number_of_votes(kind, vote_overview_soup):
    return vote_overview_soup.find(kind).find("fjöldi").string

def get_althingi_result(vote_overview_soup):
    return vote_overview_soup.find('greiðirekkiatkvæði').string

def get_parliament_member_votes(vote_details_soup):
    return vote_details_soup.find('atkvæðaskrá').find_all('þingmaður')
