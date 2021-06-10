def filter_by_owner(model, user):
    return model.objects.filter(owner=user)[0]
