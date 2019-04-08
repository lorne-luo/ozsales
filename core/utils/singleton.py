class SingletonDecorator:
    def __init__(self, klass):
        self.klass = klass
        self.instances = {}

    def __call__(self, *args, **kwargs):
        kw = ['%s=%s' % (k, kwargs[k]) for k in sorted(kwargs.keys())]
        ag = [str(i) for i in args]
        key = ','.join(ag + kw)
        key = '%s.%s:%s' % (self.klass.__module__, self.klass.__name__, key)

        if key not in self.instances:
            self.instances[key] = self.klass(*args, **kwargs)
        return self.instances[key]
