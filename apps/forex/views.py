# coding=utf-8
from datetime import datetime

from braces.views import SuperuserRequiredMixin
from django.views.generic import TemplateView

from .redis import forex_redis, price_redis
from . import forms


class ForexIndexView(SuperuserRequiredMixin, TemplateView):
    template_name = 'forex/index.html'
    instruments = ['EURUSD', 'GBPUSD', 'USDJPY', 'USDCHF', 'AUDUSD', 'NZDUSD', 'USDCNH', 'XAUUSD']
    suffix = ['CR1', 'CR2', 'CR3', 'CS1', 'CS2', 'CS3']

    def get_context_data(self, **kwargs):
        context = super(ForexIndexView, self).get_context_data(**kwargs)

        rs = {}
        for instrument in self.instruments:
            for s in self.suffix:
                key = '%s_%s' % (instrument, s)

                if instrument not in rs:
                    rs[instrument] = {}

                rs[instrument].update({s: forex_redis.get(key)})

        context.update({'resistance_support': rs})

        heartbeat = forex_redis.get('HEARTBEAT')
        if heartbeat:
            heartbeat = datetime.strptime(heartbeat, '%Y-%m-%d %H:%M:%S:%f')
        context.update({'heartbeat': heartbeat})

        last_tick_time = price_redis.get('LAST_TICK_TIME')
        if last_tick_time:
            last_tick_time = datetime.strptime(last_tick_time, '%Y-%m-%d %H:%M:%S:%f')
        context.update({'last_tick_time': last_tick_time})
        return context

    def post(self, request, *args, **kwargs):
        for instrument in self.instruments:
            for s in self.suffix:
                key = '%s_%s' % (instrument, s)
                if key in request.POST:
                    price = request.POST.get(key)
                    if price:
                        forex_redis.set(key, price)

        return super(ForexIndexView, self).get(request, *args, **kwargs)
