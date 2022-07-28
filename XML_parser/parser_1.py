import itertools
from concurrent.futures import ThreadPoolExecutor
from typing import List, Optional

from bs4 import BeautifulSoup, Tag
from loguru import logger

from schemas.abiturient import abiturient


def to_int_(i: str) -> str:
    if (i == 'true'):
        return '1'
    return '0'


def parse_entrants(
        result: List[abiturient],
        entrant: Tag) -> None:
    for item in entrant.find_all('row'):
        try:
            marks = ['', '', '', '']
            try:
                marks_ = item.get('marks', "").split(' ')
                marks[0] = marks_[0]
                marks[1] = marks_[1]
                marks[2] = marks_[2]
                marks[3] = marks_[3]
            except:
                pass

            result.append(abiturient(
                # id='',#item.find('id'),
                entrantId=item.get('entrantId', ""),
                entrantPersonalNumber=item.find('entrantPersonalNumber').get_text(),
                regNumber=item.get('regNumber', ""),
                familyName=item.get('fullFio', "").split()[0],
                fullFio=item.get('fullFio', ""),
                snils=item.get('snils', ""),
                email=item.get('email', ""),
                priority=item.get('priority', ""),
                achievements_list="; ".join(
                    [i.get_text() for i in item.find_all('markEntrantAchievements')]),
                achievementMark=item.get('achievementMark', ""),
                finalMark=item.get('finalMark', ""),
                marks=item.get('marks', ""),
                mark_1=marks[0],
                mark_2=marks[1],
                mark_3=marks[2],
                mark_4=marks[3],
                markEntranceExams="[\"" + "\",\"".join(
                    [i.get_text() for i in item.find_all('markEntranceExams')]) + "\"]",
                targetAdmissionKind=item.get('targetAdmissionKind', "144"),
                targetAdmissionExtOrgUnit=item.get('targetAdmissionExtOrgUnit', ""),
                needDormitory=to_int_(item.get('needDormitory', "")),
                averageEduInstitutionMark=item.get('averageEduInstitutionMark', ""),
                originalIn=to_int_(item.get('originalIn', "")),
                accepted=to_int_(item.get('accepted', "")),
                acceptedEntrant=to_int_(item.get('acceptedEntrant', "")),
                passedExam=to_int_(item.get('passedExam', "")),
                status=item.get('status', ""),
                refusedToBeEnrolled=to_int_(item.get('refusedToBeEnrolled', "")),
                benefitCategory=item.get('benefitCategory', ""),
                preferenceCategory=item.get('preferenceCategory', ""),
                competition=item.parent.parent.get('id', ''),  # row_iter.get('id'),
                service_status=item.get('service_status', ""),
                service_lastupdate=item.get('service_lastupdate', ""),
                position=item.get('position', ""),
                absolutePosition=item.get('absolutePosition', ""),
                formativeOrgUnitTitle=item.parent.parent.get('formativeOrgUnitTitle', '')
                # ,row_iter.get('formativeOrgUnitTitle')
            ))
        except:
            pass


def ret_list_of_abiturient(xml_file_content: bytes) -> List[Optional[abiturient]]:
    logger.bind(request_id='ret_list_of_abiturient').info("начало парсинга")
    tree_xml = BeautifulSoup(xml_file_content, 'lxml-xml')

    result: List[abiturient] = []
    try:
        for comp in tree_xml.find_all('competition'):
            entrants = list(itertools.chain(*[row.find_all('entrant') for row in comp.find_all('row')]))
            with ThreadPoolExecutor() as executer:
                executer.map(parse_entrants, [result for _ in entrants], entrants)
                executer.shutdown(wait=True)
    except:
        pass
    logger.bind(request_id='ret_list_of_abiturient').info("конец парсинга")
    return result
