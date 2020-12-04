import jdatetime


def convert_to_sec(datenow, dateorder):
    split_datenow = datenow.strftime('%H%M')
    split_dateorder = dateorder[:-2]
    res = int(split_dateorder) - int(split_datenow)
    a = 0
    for _ in range(0, res):
        a += 40
    datenow_sec = datenow.strftime('%H%M%S')
    final = int(dateorder) - int(datenow_sec) - a
    return final


def generate_time(dateorder):
    datenow = jdatetime.datetime.now().strftime('%H%M%S')
    date_order = dateorder.replace(':', '')
    final = int(date_order) - int(datenow)
    if final <= 0:
        if final < 0:
            plus_final = str(final).replace('-', '')
            f_plus_final = int(plus_final) + 30
            date = int(date_order) + f_plus_final
            return str(date)
        final += 30
        date = int(date_order) + final
        return str(date)
