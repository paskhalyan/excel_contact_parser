from django import forms
from django.core.exceptions import ValidationError
from openpyxl import load_workbook

# Can be 3 more specific errors instead of CORRUPTED_FILE_ERROR
CORRUPTED_FILE_ERROR = 'Uploaded file is corrupted or is in wrong format!'
WRONG_FILE_EXTENSION_ERROR = 'Error! Uploaded file should be with .xlsx extension!'


class ExcelFileForm(forms.Form):
    excel_file = forms.FileField(
        label='Select an excel file',
        widget=forms.ClearableFileInput(),
    )

    def clean_excel_file(self):
        file = self.cleaned_data.get('excel_file')
        if not file.name.endswith('.xlsx'):
            raise ValidationError(WRONG_FILE_EXTENSION_ERROR)

        try:
            work_sheet = load_workbook(file).active
        except:  # Every possible exception could be handled and raised with more specific error messages
            raise ValidationError(CORRUPTED_FILE_ERROR)

        first_row = next(work_sheet.rows)
        if len(first_row) is not 3:
            raise ValidationError(CORRUPTED_FILE_ERROR)

        name_cell, email_cell, phone_number_cell = first_row
        if (
            name_cell.value != 'Name' or
            email_cell.value != 'Email' or
            phone_number_cell.value != 'Phone Number'
        ):
            raise ValidationError(CORRUPTED_FILE_ERROR)

        return file
