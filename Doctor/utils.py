from django.contrib.auth.tokens import PasswordResetTokenGenerator
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template

from xhtml2pdf import pisa

class TokenGenerator(PasswordResetTokenGenerator):
    pass

generate_token = TokenGenerator()



def render_to_pdf(template_src, context):
    template = get_template(template_src)
    html  = template.render(context)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("cp1252")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None