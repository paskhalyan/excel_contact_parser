from django.shortcuts import render

from django.views import generic

from .forms import ExcelFileForm
from .models import ExcelDocument
from .tasks import parse_excel_file_task


def thank_you_view(request):
    return render(request, 'contact_parser/thank_you.html')


class ContactParserView(generic.edit.FormView):
    form_class = ExcelFileForm
    template_name = 'contact_parser/upload.html'
    success_url = '/thank-you/'

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        file = request.FILES.get('excel_file')

        if form.is_valid():
            valid_file = ExcelDocument(uploaded_file=file)
            valid_file.save()

            parse_excel_file_task.delay(valid_file.id)

            return self.form_valid(form)

        return self.form_invalid(form)
