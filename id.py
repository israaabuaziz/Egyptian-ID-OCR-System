def get_birth_date(century, day, month, year_born):
    century_mapping = {
        "3": f"{day}-{month}-20{year_born}",
        "2": f"{day}-{month}-19{year_born}"
    }
    return century_mapping.get(century, "Unknown century")


def get_gender(gender_digit):
    return "Female" if int(gender_digit) % 2 == 0 and int(gender_digit) != 6 else "Male"


def extract_id_info(national_id):  # sourcery skip: extract-method
    number_mapping = {
        '01': "القاهرة",
        '02': "اسكندرية",
        '03': "بورسعيد",
        '04': "السويس",
        '11': "دمياط",
        '12': "الدقاهلية",
        '13': "الشرقية",
        '14': "القليوبية",
        '15': "كفر الشيخ",
        '16': "الغربية",
        '17': 'المنوفية',
        '18': "البحيرة",
        '19': "اسماعلية",
        '21': "الجيزة",
        '22': "بني سويف",
        '23': "الفيوم",
        '24': "المنيا",
        '25': "اسيوط",
        '26': "سوهاج",
        '27': "قنا",
        '28': "أسوان",
        '29': "الاقصر",
        '31': "البحر الاحمر",
        '32': "وادى الجديد",
        '33': "مرسي مطروح",
        '34': "شمال سيناء",
        '35': "جنوب سيناء",
        '88': "outside the country"
    }

    try:
        century = national_id[0]
        year_born = national_id[1:3]
        month = national_id[3:5]
        day = national_id[5:7]
        temp_born = national_id[7:9]
        place_of_birth = number_mapping.get(temp_born, "Unknown")
        gender = national_id[12]
        verify_id = national_id[13]

        birth_date = get_birth_date(century, day, month, year_born)
        gender_str = get_gender(gender)
        print(f"birth date: {birth_date}")
        print(f"place of birth: {place_of_birth}")
        print(f"gender: {gender_str}")
        
        return {
            "birth_date": birth_date,
            "place_of_birth": place_of_birth,
            "gender": gender_str,
        }

    except (IndexError, ValueError):
        print('*************************************')
        print('Invalid or incomplete national ID.')
        print("Insert new image please and try again!!")
        print("Notice: the clarity and resolution should be clear and perfectly skewed and the image not too far and not too close.")
        print('*************************************')
        return None
