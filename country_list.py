countries = open("countries.txt", "r")
country_list = [" "]
for line in countries.readlines():
    clean_line = line.strip()
    country_list.append(clean_line)

# print(country_list)

# choices_list = []
# for country in country_list:
#     t = tuple(country)
#     choices_list.append(t)