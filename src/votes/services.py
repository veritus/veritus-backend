import case_gather.soupUtils as soupUtils
from case_gather.models import Case
from parliament.models import ParliamentMember
from .models import VoteRecord, Vote

def get_votes_by_parliament_session(parliament_session):
    '''
        We scrape the overall vote records for the parliament session
        and save them as a VoteRecord.
        Then we go to the details page to see what each individual
        parliament member voted and save them as a Vote
    '''
    link = "http://www.althingi.is/altext/xml/atkvaedagreidslur/?lthing="
    details_link = "http://www.althingi.is/altext/xml/atkvaedagreidslur/atkvaedagreidsla/?numer="
    votes_soup = soupUtils.getSoupFromLink(link + str(parliament_session.session_number))
    vote_records = collect_vote_records(votes_soup, parliament_session)
    for vote_record in vote_records:
        vote_record_althingi_id = vote_record['althingi_id']
        vote_record_exits = VoteRecord.objects.filter(
            althingi_id=vote_record_althingi_id
        ).exists()
        if not vote_record_exits:
            created_vote_record = VoteRecord.objects.create(
                case=vote_record['case'],
                althingi_id=vote_record_althingi_id,
                yes=vote_record['number_of_yes'],
                no=vote_record['number_of_no'],
                didNotVote=vote_record['number_of_did_not_vote'],
                althingi_result=vote_record['althingi_result'],
            )
            vote_details_soup = soupUtils.getSoupFromLink(
                details_link + str(vote_record['althingi_id'])
            )
            parliament_member_votes = get_parliament_member_votes(
                vote_details_soup
            )
            for parliament_member_vote in parliament_member_votes:
                parliament_member_name = get_parliament_member_name_from_vote(
                    parliament_member_vote
                )
                parliament_member = ParliamentMember.objects.filter(
                    name=parliament_member_name
                )
                # Create parliamentMember if he does not exist
                if not parliament_member.exists():
                    parliament_member = ParliamentMember.objects.create(
                        name=parliament_member_name
                    )
                else:
                    parliament_member = parliament_member.get()

                vote_result = get_parliament_member_result_from_vote(parliament_member_vote)
                Vote.objects.create(
                    parliament_member=parliament_member,
                    althingi_result=vote_result,
                    vote_record=created_vote_record
                )

def collect_vote_records(soup, parliament_session):
    vote_records = []
    for vote_record in get_all_votes(soup):
        case_number = get_case_number(vote_record)
        case = Case.objects.get(
            number=case_number,
            parliament_session=parliament_session,
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
    kind_tag = vote_overview_soup.find(kind)
    if kind_tag is not None:
        return kind_tag.find("fjöldi").string
    return None

def get_althingi_result(vote_overview_soup):
    did_not_vote_tag = vote_overview_soup.find('greiðirekkiatkvæði')
    if did_not_vote_tag is not None:
        return did_not_vote_tag.string
    return None

def get_parliament_member_votes(vote_details_soup):
    votes_tag = vote_details_soup.find('atkvæðaskrá')
    if votes_tag is not None:
        return votes_tag.find_all('þingmaður')
    return []

def get_parliament_member_name_from_vote(vote_soup):
    return vote_soup.find('nafn').string

def get_parliament_member_result_from_vote(vote_soup):
    return vote_soup.find('atkvæði').string
