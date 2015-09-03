__author__ = 'jcteng'


class BasePage(object):

    class Meta:
        abstract = True

class Page(BasePage):

    parent = None
    in_menus = None
    content_model = None
    login_required = False

    def __str__(self):
        return self.titles

    @classmethod
    def get_content_models(cls):

        def is_content_model(m):
            return m is not Page and issubclass(m, Page) and not m._meta.proxy
        return list(filter(is_content_model, apps.get_models()))

    def get_content_model(self):
        return getattr(self, self.content_model, None)

    def set_parent(self, new_parent):
        pass

    def set_parent(self, new_parent):
        pass