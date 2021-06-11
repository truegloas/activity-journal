from datetime import date


def filter_by_owner(model, user):
    return model.objects.filter(owner=user)[0]


def extract_date_from_str(date_str):
    return date(*list(list(map(lambda x: int(x), date_str.split('-')))))


def date_formatter(year, month, day):
    return f"{year:04}", f"{month:02}", f"{day:02}"
