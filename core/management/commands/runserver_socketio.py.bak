# -*- coding: utf-8 -*-
#
# Django runserver management command for use with gevent-socketio
# library.
# https://gist.github.com/rhblind/0399f1058222e67a9bde
# Usage:
#   $ python manage.py runserver_socketio

from __future__ import unicode_literals

import re
import os
import sys
import errno
import socket
from datetime import datetime
from optparse import make_option

from django.conf import settings
from django.contrib.staticfiles.handlers import StaticFilesHandler
from django.core.management.base import BaseCommand, CommandError
from django.core.management.commands.runserver import naiveip_re, DEFAULT_PORT
from django.core.servers.basehttp import get_internal_wsgi_application
from django.utils import six, autoreload

from socketio.server import SocketIOServer


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option("--ipv6", "-6", action="store_true", dest="use_ipv6", default=False,
                    help="Tells Django to use a IPv6 address."),
        make_option("--noreload", action="store_false", dest="use_reloader", default=True,
                    help="Tells Django to NOT use the auto-reloader."),
        make_option("--resource", "-r", dest="resource", default="socket.io",
                    help="The URL which has to be identified as a socket.io request. "
                         "Defaults to the /socket.io/ URL."),
        make_option("--transports", "-t", dest="transports", default="websocket,xhr-multipart,xhr-polling",
                    help="Pass a list of transport protocols to listen to. Currently supported transports: "
                         "websocket, flashsocket, htmlfile, xhr-multipart, xhr-polling and jsonp-polling. "
                         "Defaults to xhr-multipart, xhr-polling and websocket."),
        make_option("--static", "-s", action="store_false", dest="use_static_handler", default=True,
                    help="Enable hosting of static files in development mode. Defaults to True."),
        make_option("--insecure", action="store_true", dest="insecure_serving", default=False,
                    help="Serve insecure. Set to True if you want to serve static content while "
                         "DEBUG=False. Defaults to False.")
    )
    help = "Starts a lightweight gevent-socketio enabled Web server for development."
    args = "[optional port number, or ipaddr:port]"

    requires_model_validation = False

    @staticmethod
    def get_handler(*args, **options):
        """
        Returns the default WSGI handler for the runner.
        """
        handler = get_internal_wsgi_application()
        use_static_handler = options.get("use_static_handler")
        insecure_serving = options.get("insecure_serving")
        if settings.DEBUG and use_static_handler or (use_static_handler and insecure_serving):
            handler = StaticFilesHandler(handler)

        return handler

    def handle(self, addrport='', *args, **options):
        if not settings.DEBUG and not settings.ALLOWED_HOSTS:
            raise CommandError("You must set settings.ALLOWED_HOSTS if DEBUG is False.")

        self.use_ipv6 = options.get("use_ipv6")
        if self.use_ipv6 and not socket.has_ipv6:
            raise CommandError("Your Python does not support IPv6.")
        if args:
            raise CommandError("Usage is runserver %s" % self.args)
        self._raw_ipv6 = False
        if not addrport:
            self.addr = ""
            self.port = DEFAULT_PORT
        else:
            m = re.match(naiveip_re, addrport)
            if m is None:
                raise CommandError('"%s" is not a valid port number '
                                   'or address:port pair.' % addrport)
            self.addr, _ipv4, _ipv6, _fqdn, self.port = m.groups()
            if not self.port.isdigit():
                raise CommandError("%r is not a valid port number." % self.port)
            if self.addr:
                if _ipv6:
                    self.addr = self.addr[1:-1]
                    self.use_ipv6 = True
                    self._raw_ipv6 = True
                elif self.use_ipv6 and not _fqdn:
                    raise CommandError('"%s" is not a valid IPv6 address.' % self.addr)
        if not self.addr:
            self.addr = "::1" if self.use_ipv6 else "127.0.0.1"
            self._raw_ipv6 = bool(self.use_ipv6)
        self.run(*args, **options)

    def run(self, *args, **options):
        """
        Runs the server, using the autoreloader if needed
        """
        use_reloader = options.get('use_reloader')

        if use_reloader:
            autoreload.main(self.inner_run, args, options)
        else:
            self.inner_run(*args, **options)

    def inner_run(self, *args, **options):
        """
        Bootstrap code
        """
        from django.conf import settings
        from django.utils import translation

        shutdown_message = options.get("shutdown_message", "")
        quit_command = "CTRL-BREAK" if sys.platform == "win32" else "CONTROL-C"

        self.stdout.write("Validating models...\n\n")
        self.validate(display_num_errors=True)
        now = datetime.now().strftime("%B %d, %Y - %X")
        if six.PY2:
            now = now.decode("utf-8")

        supported_transports = (
            "websocket", "flashsocket", "htmlfile",
            "xhr-multipart", "xhr-polling", "jsonp-polling")
        transports = [x.strip() for x in options.get("transports").split(",")
                      if x in supported_transports]
        if not transports:
            raise CommandError("Supported transport protocols are: {0}.".format(", ".join(supported_transports)))

        self.stdout.write(
            "{now}\n"
            "Django version {version}, using settings {settings}\n"
            "Starting SocketIO development server at http://{addr}:{port} and "
            "on 10843 (flash policy server)\n"
            "Listening on the following transports: {transports}\n"
            "Quit the server with {quit_command}".format(
                now=now, version=self.get_version(), settings=settings.SETTINGS_MODULE,
                addr="[%s]" % self.addr if self._raw_ipv6 else self.addr, port=self.port,
                transports=", ".join(transports), quit_command=quit_command
            )
        )

        translation.activate(settings.LANGUAGE_CODE)

        try:
            handler = self.get_handler(*args, **options)
            httpd = SocketIOServer((self.addr, int(self.port)), handler,
                                   resource=options.get("resource"), transports=transports)
            httpd.serve_forever()
        except socket.error as e:
            # Use helpful error messages instead of ugly tracebacks.
            ERRORS = {
                errno.EACCES: "You don't have permission to access that port.",
                errno.EADDRINUSE: "That port is already in use.",
                errno.EADDRNOTAVAIL: "That IP address can't be assigned-to.",
            }
            try:
                error_text = ERRORS[e.errno]
            except KeyError:
                error_text = str(e)
            self.stderr.write("Error: %s" % error_text)
            # Need to use an OS exit because sys.exit doesn't work in a thread
            os._exit(1)
        except KeyboardInterrupt:
            if shutdown_message:
                self.stdout.write(shutdown_message)
            sys.exit(0)
