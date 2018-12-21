import random
import string

from django.utils.text import slugify
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template

from xhtml2pdf import pisa
from django.conf import settings
from django.conf.urls.static import static
import os




# travailler avec pdf

def render_to_pdf(template_src, context_dict={}):
    def link_callback(uri, rel):
        # use short variable names
        sUrl = settings.STATIC_URL      # Typically /static/
        sRoot = settings.STATIC_ROOT    # Typically /home/userX/project_static/
        mUrl = settings.MEDIA_URL       # Typically /static/media/
        mRoot = settings.MEDIA_ROOT     # Typically /home/userX/project_static/media/

        # convert URIs to absolute system paths
        if uri.startswith(mUrl):
            path = os.path.join(mRoot, uri.replace(mUrl, ""))
        elif uri.startswith(sUrl):
            path = os.path.join(sRoot, uri.replace(sUrl, ""))

        # make sure that file exists
        if not os.path.isfile(path):
            raise Exception('media URI must start with %s or %s' % (sUrl, mUrl))
        return path
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("utf-8")), result,link_callback=link_callback)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None
