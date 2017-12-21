# coding=utf-8


class HansSelect2ViewMixin(object):
    # translate into chinese
    def get_create_option(self, context, q):
        create_option = super(HansSelect2ViewMixin, self).get_create_option(context, q)
        if create_option:
            create_option[0]['text'] = u'点击新建 "%s"' % q
        return create_option
