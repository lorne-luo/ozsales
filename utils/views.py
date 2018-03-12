from io import BytesIO
from django.template.loader import get_template
from django.http import HttpResponse
from django.views.generic import TemplateView
from xhtml2pdf import pisa


class PDFDownloadView(TemplateView):
    """convert template view into pdf and serve as downloading"""
    template_name = None

    def render_to_pdf(self, template_src, context_dict=None, direct_download=None):
        if context_dict is None:
            context_dict = {}

        template = get_template(template_src)
        html = template.render(context_dict)
        result = BytesIO()

        pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
        if not pdf.err:
            if direct_download:
                return result.getvalue()
            return HttpResponse(result.getvalue(), content_type='application/pdf')
        return None

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        pdf = self.render_to_pdf(self.template_name, context)
        return HttpResponse(pdf, content_type='application/pdf')
