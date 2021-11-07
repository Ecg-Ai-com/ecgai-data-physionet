import logging

import azure.functions as func
from ecgai_logging.log_decorator import log

from src import PtbXl


@log
async def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP get_record trigger processed a request.')

    record_id = req.params.get('record_id')
    # sample_rate = req.params.get('sample_rate')
    if not record_id:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            record_id = int(req_body.get('record_id'))

    if record_id:
        record_proxy = PtbXl()
        recordDTO = await record_proxy.get_record(record_id=record_id, sample_rate=100)
        return func.HttpResponse(recordDTO.json())
    else:
        return func.HttpResponse(
            "Get record function. Pass a record_id in the query string or in the request "
            "body for a personalized response.",
            status_code=200
        )
