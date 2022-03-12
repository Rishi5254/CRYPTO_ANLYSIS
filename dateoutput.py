def formatted_date(date):
    date = date.split("-")
    year = date[0]
    month = date[1]
    day = date[2]
    if len(month) == 1 and len(day) == 1:
        month = f"0{month}"
        day = f"0{day}"
    elif len(day) == 1:
        day = f"0{day}"
    elif len(month) == 1:
        month = f"0{month}"
    return f"{year}-{month}-{day}"


def date_sequence(date, res):
    date = f"{date}"
    date = date.split("-")
    if date[2][0] == "0":
        day = int(date[2][1])
    else:
        day = int(date[2])
    if date[1][0] == "0":
        month = int(date[1][1])
    else:
        month = int(date[1])
    year = int(date[0])

    if res == "p":
        if 1 < day <= 31:
            return formatted_date(f"{year}-{month}-{day - 1}")
        elif day == 1:
            return formatted_date(f"{year}-{month - 1}-31")
    elif res == "n":
        if 1 <= day < 31:
            return formatted_date(f"{year}-{month}-{day + 1}")
        elif day == 31:
            return formatted_date(f"{year}-{month + 1}-01")
    elif res == "pp":
        if 2 < day <= 31:
            return formatted_date(f"{year}-{month}-{day - 2}")
        elif day == 2:
            return formatted_date(f"{year}-{month - 1}-31")
        elif day == 1:
            return formatted_date(f"{year}-{month - 1}-30")



