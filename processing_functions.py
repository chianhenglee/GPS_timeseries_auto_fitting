def check_leap_year(input_year):
	'''return True if input_year is leap year, false if not'''
	if input_year % 4 == 0:
		if input_year % 100 == 0 :
			if input_year % 400 == 0 :
				LeapYear = True
			else :
				LeapYear = False
		else :
			LeapYear = True
	else :
		LeapYear = False

	return LeapYear


def get_digit_date(doy_date):

	digit_date = []

	for cur_date in doy_date:

		cur_date_str = str(cur_date)

		y = cur_date_str[0:4]
		doy = cur_date_str[4:]

		if check_leap_year(int(y)):
			digit_date.append(int(y)+int(doy)/366)
		else:
			digit_date.append(int(y)+int(doy)/365)

	return digit_date

