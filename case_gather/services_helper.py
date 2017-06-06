import logging
from case_gather.models import Subject, SuperSubject

def get_all_subjects_in_db():
    logger = logging.getLogger('cronJobServices')

    try:
        subjects_in_db = Subject.objects.all()
        logger.info(subjects_in_db)
    except Exception as e:
        logger.error('Failed to create objects, error raised:' + '-' +
                     e.message, traceback.format_exc())

    return subjects_in_db

def collect_subjects(subjects_in_db):

    subject_numbers = []
    for subject in subjects_in_db:
        subject_numbers.append(subject.number)

    return subject_numbers

def get_all_parents_in_db():
    logger = logging.getLogger('cronJobServices')

    try:
        parents_in_db = SuperSubject.objects.all()
        logger.info(parents_in_db)
    except Exception as e:
        logger.error('Failed to create objects, error raised:' + '-' +
                     e.message, traceback.format_exc())

    return parents_in_db

def collect_parents(parents_in_db):

    parent_numbers = []
    for parent in parents_in_db:
        parent_numbers.append(parent.number)

    return parent_numbers