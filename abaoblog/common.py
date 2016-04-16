__author__ = 'haoyi'


def smart_truncate(text, length=100, suffix='...'):
    if len(text) <= length:
        return text
    else:
        return ' '.join(text[:length + 1].split(' ')[0:-1]) + ' ' + suffix
