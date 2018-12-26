import xlwt
from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template, render_to_string 
from working_with_pdf.utils import render_to_pdf
from django.contrib.auth import get_user_model
User = get_user_model()

def home(request):
  return render(request, "myapp/index.html")

def generate_pdf(request):
        try:
            users = User.objects.all()
            template = get_template('myapp/generate_pdf.html')
            context = {
                "users": users,
            }
            #mRoot = settings.MEDIA_ROOT
            html = template.render(context)
            
            pdf = render_to_pdf('myapp/generate_pdf.html', context)
            if pdf:
                response = HttpResponse(pdf, content_type='application/pdf')
                filename = "mypdf_%s.pdf" %("12341231")
                content = "inline; filename='%s'" %(filename)
                download = request.GET.get("download")
                if download:
                    content = "attachment; filename='%s'" %(filename)
                response['Content-Disposition'] = content
                return response
        except Exception as e:
            print("erreur ", e)
        return HttpResponse("Une erreur s'est produit")


def generate_xls(request):
    try:
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="export_box.xls"'
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Packages')
        # Sheet header, first row
        row_num = 0
        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        columns = ['ID','Nom', 'Prenom', 'Email', ]
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)
        # Sheet body, remaining rows
        font_style = xlwt.XFStyle()
        rows = users = User.objects.all().values_list('id','first_name', 'last_name', 'email')
        for row in rows:
            row_num += 1
            for col_num in range(len(row)):
                ws.write(row_num, col_num, row[col_num], font_style)
        wb.save(response)
        return response
    except Exception as e:
        print("Erreur", e)
        return HttpResponse("Une erreur s'est produite")
    