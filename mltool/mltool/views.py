from django.views.generic import TemplateView
from django.http import HttpResponse
import os
import re
import json


class ReceiptViewer(TemplateView):

    template_name = 'mltool/receipt_viewer.html'
    name = '/Users/peyman/projects/logo-net/data/walmart'

    def image_list(self):
        return sorted(
            filter(lambda item: re.match('.*[.]jp[e]?g', item), os.listdir(os.path.join(self.name, 'images')))
        )

    def get_context_data(self, **kwargs):
        all_receipts = self.image_list()
        current = kwargs.get('pk') or all_receipts[0]
        try:
            next_receipt = all_receipts[all_receipts.index(current) + 1]
        except Exception:
            next_receipt = None
        return {
            'name': 'Peyman',
            'next': next_receipt,
            'current': current,
            'image_url': '/static/images/{}'.format(current)
        }

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        name = data.pop('name')
        result = {
            'coordinates': data,
            'label': 'walmart',
        }
        with open(os.path.join(self.name, 'coordinates', name + '.json'), 'w') as writer:
            writer.write(json.dumps(result))
        return HttpResponse('ok')
