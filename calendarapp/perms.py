

class AdaptorEditInline(object):

    @classmethod
    def can_edit(cls, adaptor_field):
        user = adaptor_field.request.user
        obj = adaptor_field.obj

        can_edit = False
        if not user.is_authenticated:
            pass
        elif user.is_active:
            can_edit = True
            pass
        else:
            can_edit = user.has_perm('edit')
        return can_edit
