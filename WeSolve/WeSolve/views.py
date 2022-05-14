from django.http import HttpResponse
from django.views import View

class ReturnPDF(View): 
    def get(self, request, path, *args, **kwargs):
        path_items = path.split('/')
        pdf_path = f'questions/uploads/{path_items[0]}/{path_items[1]}'
        with open(pdf_path, 'rb') as pdf:
                response = HttpResponse(pdf.read(), content_type='application/pdf')
                response['Content-Disposition'] = f'inline;filename={pdf_path}'
                return response