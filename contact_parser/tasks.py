import pytz

from celery import shared_task
from datetime import datetime, timedelta
from django.db.models import Q
from openpyxl import load_workbook

from .models import ExcelDocument, Contact


@shared_task
def parse_excel_file_task(file_id):
    file = ExcelDocument.objects.get(id=file_id).uploaded_file
    work_sheet_rows = load_workbook(file).active.rows
    next(work_sheet_rows)
    for row in work_sheet_rows:
        name, email, phone_number = (cell.value for cell in row)
        if not phone_number:
            continue

        qs = Contact.objects.filter(Q(phone_number=phone_number) | Q(email=email.lower()))
        if qs.exists():
            last_uploaded_date = max(qs.values_list('created_at', flat=True))
            if datetime.now(pytz.utc) - last_uploaded_date < timedelta(minutes=3):
                continue

        Contact.objects.create(
            name=name,
            phone_number=phone_number,
            email=email.lower(),
            document_id=file_id,
        )
