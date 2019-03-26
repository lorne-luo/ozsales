# coding=utf-8
from datetime import datetime
from subprocess import Popen, PIPE
from shlex import split
from braces.views import SuperuserRequiredMixin
from django.views.generic import TemplateView

from .redis import forex_redis, price_redis
from . import forms


class ForexIndexView(SuperuserRequiredMixin, TemplateView):
    template_name = 'forex/index.html'
    instruments = ['EURUSD', 'GBPUSD', 'USDJPY', 'USDCHF', 'AUDUSD', 'NZDUSD', 'USDCNH', 'XAUUSD']
    suffix = ['R', 'S']

    def get_context_data(self, **kwargs):
        context = super(ForexIndexView, self).get_context_data(**kwargs)

        rs = {}
        for instrument in self.instruments:
            for s in self.suffix:
                key = '%s_%s' % (instrument, s)

                if instrument not in rs:
                    rs[instrument] = {}

                rs[instrument].update({s: price_redis.get(key)})

        context.update({'resistance_support': rs})

        heartbeat = forex_redis.get('HEARTBEAT')
        if heartbeat:
            heartbeat = datetime.strptime(heartbeat, '%Y-%m-%d %H:%M:%S:%f')
        context.update({'heartbeat': heartbeat})

        # grep ERROR /opt/qsforex/log/qsforex.log |tail -n -1

        last_tick_time = price_redis.get('LAST_TICK_TIME')
        if last_tick_time:
            last_tick_time = datetime.strptime(last_tick_time, '%Y-%m-%d %H:%M:%S:%f')
        context.update({'last_tick_time': last_tick_time})
        error, error_time = self._get_last_error()
        context.update({'last_error': error})
        context.update({'last_error_time': error_time})
        context.update({'trade_count': self._get_trade_count()})
        return context

    def post(self, request, *args, **kwargs):
        for instrument in self.instruments:
            for s in self.suffix:
                key = '%s_%s' % (instrument, s)
                if key in request.POST:
                    price = request.POST.get(key)
                    if price:
                        price_redis.set(key, price)

        return super(ForexIndexView, self).get(request, *args, **kwargs)

    def _get_last_error(self):
        try:
            log_path = '/opt/qsforex/log/qsforex.log'
            grep_cmd = 'grep ERROR %s' % log_path
            tail_cmd = 'tail -n -1'

            p1 = Popen(split(grep_cmd), stdout=PIPE)
            p2 = Popen(split(tail_cmd), stdin=p1.stdout, stdout=PIPE)
            output, error = p2.communicate()
            error = output.decode()

            dt_str = error.split('|')[0]
            _time = datetime.strptime(dt_str, '%Y-%m-%d %H:%M:%S,%f')

            return error, _time
        except:
            return 'Cant get error', None

    def _get_trade_count(self):
        OPENING_TRADE_COUNT_KEY = 'OPENING_TRADE_COUNT'
        return forex_redis.get(OPENING_TRADE_COUNT_KEY)
