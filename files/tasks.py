import datetime
import os
from dataclasses import dataclass
from typing import List

import pandas as pd
from config import celery_app
from files.models import Report
from shop.models import Customer


@dataclass
class ReportDTO:
    file_url: str
    params: str


def save_report_object(dto: ReportDTO) -> Report:
    """ Сохраняет объект отчета
    """
    report = Report.objects.create(
        file_url=dto.file_url,
        params=dto.params,
        create_at=datetime.date.today()
    )
    return report


def save_to_xlsx_list(
        data: List[dict],
        sheet_name: str,
        filename: str,
        saved_params: str,
):
    """ Сохраняет список словарей в xlsx файл
    """
    path_dir = f"{os.getcwd()}/mareety_bot_backend/media/reports"
    if not os.path.exists(path_dir):
        os.makedirs(path_dir)
    path_file = f"{path_dir}/{filename}"

    path_url = f"/media/reports/{filename}"
    count_saved_items = 100

    new_data = []
    # columns = list(data[0].keys())
    writer = pd.ExcelWriter(path_file, engine="openpyxl")
    df = pd.DataFrame(data=new_data)
    df.to_excel(writer, sheet_name=sheet_name, index=False, header=True)

    c = 0
    for item in data:
        new_data.append(item)
        if len(new_data) == count_saved_items:
            df = pd.DataFrame(data=new_data)
            df.to_excel(
                writer,
                sheet_name=sheet_name,
                index=False,
                startrow=c,
                header=False
            )

            c += count_saved_items
            new_data = []
    df = pd.DataFrame(data=new_data)
    df.to_excel(writer, sheet_name=sheet_name, index=False, startrow=c)
    writer.close()

    domain = "https://185.124.64.148"

    full_path_url = domain + path_url

    report = save_report_object(
        ReportDTO(
            file_url=full_path_url,
            params=saved_params
        )
    )
    print(report)


@celery_app.task(
    bind=True,
    name=f"files.build_users_to_file_task",
    default_retry_delay=60 * 60 * 30,
    max_retries=5,
    soft_time_limit=60 * 60 * 35,
    time_limit=60 * 60 * 35,
)
def build_users_to_file_task(self):
    customers = Customer.objects.all()
    objects = []
    for c in customers:
        obj = c.__dict__
        obj.pop("_state")
        obj.pop("tg_user_id")
        objects.append(obj)
    save_to_xlsx_list(
        objects, "Users", f"mareety_users.xlsx", ""
    )
