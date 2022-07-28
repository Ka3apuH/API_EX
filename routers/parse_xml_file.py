import csv
import io

from fastapi import APIRouter, status, UploadFile, File

from typing import Optional, List
from loguru import logger
from starlette.responses import StreamingResponse

from XML_parser.parser_1 import ret_list_of_abiturient
from schemas.abiturient import abiturient

router = APIRouter(prefix="/api", tags=['xml_parse'])


@router.post("/xml", status_code=status.HTTP_201_CREATED)
@logger.bind(request_id='create_csv').catch()
async def create_csv(files: List[Optional[UploadFile]] = File(...)):
    abity: List[abiturient] = []

    for f in files:
        abity.extend(ret_list_of_abiturient(xml_file_content=await f.read()))

    fieldnames = list(abiturient.schema()["properties"].keys())

    fp = io.StringIO("")

    writer = csv.DictWriter(fp, fieldnames=fieldnames, quotechar='"', quoting=csv.QUOTE_ALL)
    writer.writeheader()
    for person in abity:
        writer.writerow(person.dict())

    return StreamingResponse(io.BytesIO(bytes(fp.getvalue(), encoding='utf-8')), media_type="text/csv")
