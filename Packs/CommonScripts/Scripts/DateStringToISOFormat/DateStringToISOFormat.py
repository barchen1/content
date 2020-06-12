import demistomock as demisto
from dateutil.parser import parse


def parse_datestring_to_iso(date_value: str, day_first: bool, year_first: bool, fuzzy: bool) -> str:
    return parse(date_value, dayfirst=day_first, yearfirst=year_first, fuzzy=fuzzy).isoformat()


def main():
    args = demisto.args()
    date_value = args.get('value')
    day_first = args.get('dayfirst', 'True').lower() == 'true'
    year_first = args.get('yearfirst', 'False').lower() == 'true'
    fuzzy = args.get('fuzzy', 'True').lower() == 'true'
    iso_string = parse_datestring_to_iso(date_value, day_first, year_first, fuzzy)
    demisto.results(iso_string)


# python2 uses __builtin__ python3 uses builtins
if __name__ in ('__builtin__', 'builtins', '__main__'):
    main()
