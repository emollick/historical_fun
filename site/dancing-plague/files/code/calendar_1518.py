"""Julian-calendar weekday check for the dated council decisions of 1518.
Run: python3 calendar_1518.py
"""
def julian_to_jdn(y, m, d):
    a = (14 - m) // 12
    y2 = y + 4800 - a
    m2 = m + 12 * a - 3
    return d + (153 * m2 + 2) // 5 + 365 * y2 + y2 // 4 - 32083

NAMES = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

def weekday(y, m, d):
    return NAMES[julian_to_jdn(y, m, d) % 7]

CHECKS = {
    'Easter 1518': (4, 4),
    'St Margaret, Strasbourg use (Grotefend: 15 July)': (7, 15),
    'Imlin: 8 days before Magdalene = 14 July': (7, 14),
    'St Mary Magdalene 22 July ("5a Mariae Magdalenae" = Thursday)': (7, 22),
    '"Fritag post Marie Magdalene" = 23 July': (7, 23),
    'Letter to the bishop, 25 July': (7, 25),
    'Mandate signed by Brant, 2 Aug': (8, 2),
    'St Lawrence 10 Aug': (8, 10),
    '"4a post Laurentii" = Wednesday 11 Aug': (8, 11),
    'St Adelphus of Metz 29 Aug (Strasbourg use)': (8, 29),
    '"Dienstag post Adolphi" = 31 Aug': (8, 31),
    'Michaelmas 29 Sept (end of the dance ban)': (9, 29),
}
if __name__ == '__main__':
    for label, (m, d) in CHECKS.items():
        print(f'{label:62s} 1518-{m:02d}-{d:02d} = {weekday(1518, m, d)}')
