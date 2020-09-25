import json
from audioop import reverse

from braces.views import SuperuserRequiredMixin
from datetime import datetime, timedelta
from dateutil import tz
from django.utils import timezone
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect

from shlex import split
from subprocess import Popen, PIPE

from apps.forex.binance import get_btcusdt_price
from .redis import forex_redis, price_redis, get_btcusdt_resistance, set_btcusdt_resistance, set_btcusdt_support, \
    get_btcusdt_support


class BTCUSDTView(SuperuserRequiredMixin, TemplateView):
    template_name = 'forex/btcusdt.html'
    resistance_key = 'BTCUSDT_RESISTANCE'
    support_key = 'BTCUSDT_SUPPORT'

    def get_context_data(self, **kwargs):
        context = super(BTCUSDTView, self).get_context_data(**kwargs)
        resistance = get_btcusdt_resistance()
        support = get_btcusdt_support()

        next_refresh = timezone.now() + timedelta(seconds=60)
        next_refresh = next_refresh.replace(second=3)
        countdown = (next_refresh - timezone.now()).seconds
        context.update({'resistance': resistance,
                        'current_price': get_btcusdt_price(),
                        'support': support,
                        'countdown': countdown})
        return context

    def post(self, request, *args, **kwargs):
        resistance = request.POST.get('resistance', '')
        if resistance:
            set_btcusdt_resistance(resistance)

        support = request.POST.get('support', '')
        if support:
            set_btcusdt_support(support)

        return HttpResponseRedirect('/forex')


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
        trades = forex_redis.get('TRADES')
        trades = json.loads(trades) if trades else {}

        last_tick_time = price_redis.get('LAST_TICK_TIME')
        if last_tick_time:
            last_tick_time = datetime.strptime(last_tick_time, '%Y-%m-%d %H:%M:%S:%f').replace(tzinfo=tz.tzutc())
            last_tick_time = timezone.localtime(last_tick_time)
        context.update({'last_tick_time': last_tick_time})
        errors, error_time = self._get_last_error()
        context.update({'errors': errors})
        context.update({'trades': trades})
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
        url = reverse('forex:main')
        return HttpResponseRedirect(url)

    def _get_last_error(self):
        try:
            log_path = '/opt/qsforex/log/qsforex.log'
            grep_cmd = 'grep ERROR %s' % log_path
            tail_cmd = 'tail -n -7'

            p1 = Popen(split(grep_cmd), stdout=PIPE)
            p2 = Popen(split(tail_cmd), stdin=p1.stdout, stdout=PIPE)
            output, error = p2.communicate()
            error = output.decode()

            errors = [x for x in error.split('\n') if x]

            dt_str = errors[-1].split('|')[0]
            _time = datetime.strptime(dt_str, '%Y-%m-%d %H:%M:%S,%f')

            return errors, _time
        except:
            return [], None

    def _get_trade_count(self):
        OPENING_TRADE_COUNT_KEY = 'OPENING_TRADE_COUNT'
        return forex_redis.get(OPENING_TRADE_COUNT_KEY) or 0
