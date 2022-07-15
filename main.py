import os
import numpy as np
import csv


path = "measurements/"
path = os.path.realpath(path)
lons = os.listdir(path)


def get_relevant(file_name):
    file_path = path + '\\' + file_name
    fh = open(file_path, 'r')
    fh = fh.readlines()
    speed_temp = []
    for line in fh:
        line = line.split(',')
        speed = float(line[0])
        temp = float(line[1])
        if abs(temp) < 10:
            continue
        speed_temp.append([speed, temp])
    return speed_temp


def find_right_max_first_q(list_of_speeds):
    sorted_speeds = sorted(list_of_speeds, key=lambda x: -x[0])
    i = 0
    for speed, temperature in sorted_speeds[1:]:
        i += 1
        if temperature > sorted_speeds[i+1][1] and temperature > sorted_speeds[i-1][1] and temperature > 25:
            first_max_right = [speed, temperature]
            break
    epsilon_env = sorted_speeds[:i + 1]
    epsilon_env = epsilon_env[: :-1]
    for speed, temp in epsilon_env:
        if temp <= (first_max_right[1] - 5)/2:
            HWHM = speed - first_max_right[0]
            sigma = HWHM/((2* np.log(2))**0.5)
            grand_finle = [first_max_right[0], first_max_right[1], HWHM, sigma]

            break

    return grand_finle #list with [local_max_speed, temperture_of_that_speed, HWHM, sigma_of_HWHM]


def find_left_max_forth_q(list_of_speeds):
    sorted_speeds = sorted(list_of_speeds, key=lambda x: x[0])
    i = 0
    for speed, temperature in sorted_speeds[1:]:
        i += 1
        if temperature > sorted_speeds[i + 1][1] and temperature > sorted_speeds[i - 1][1] and temperature > 30:
            first_max_left = sorted_speeds[i]
            break
    epsilon_env2 = sorted_speeds[:i + 1]
    epsilon_env2 = epsilon_env2[::-1]
    for speed, temp in epsilon_env2:
        if temp <= (first_max_left[1]) / 2:
            HWHM = abs(first_max_left[0] - speed)
            sigma = HWHM / ((2 * np.log(2)) ** 0.5)
            grand_finle = [first_max_left[0], first_max_left[1], HWHM, sigma]
            break
    return grand_finle #list with [local_max_speed, temperture_of_that_speed, HWHM, sigma_of_HWHM]



lons_and_temp_pos = []
lons_and_temp_neg = []
count_p = 0
count_n = 0
for lon in lons:
    speeds_and_temps = get_relevant(lon)
    longitute = int(lon.replace("_0.csv", ''))
    if lon[0] == '-':
        lons_and_temp_neg.append([longitute])
        last_list = find_left_max_forth_q(speeds_and_temps)
        for item in last_list:
            lons_and_temp_neg[count_n].append(item)
        count_n += 1
    else:
        lons_and_temp_pos.append([longitute])
        last_list = find_right_max_first_q(speeds_and_temps)
        for item in last_list:
            lons_and_temp_pos[count_p].append(item)
        count_p += 1




lons_and_temp_pos = sorted(lons_and_temp_pos,key= lambda x: x[0])
lons_and_temp_neg = sorted(lons_and_temp_neg,key= lambda x: -x[0])
#lists with [lon, local_max_speed, temperture_of_that_speed, HWHM, sigma_of_HWHM]
print(lons_and_temp_pos, '\n', lons_and_temp_neg)

with open('analysed_data.csv', 'w', newline='') as file:
    fieldnames = ['longitute', 'max local speed', 'temperature at that speed', 'HWHM', 'Sigma']
    writer = csv.DictWriter(file, fieldnames=fieldnames)

    writer.writeheader()
    for item in lons_and_temp_pos:
        writer.writerow({fieldnames[0]: item[0], fieldnames[1]: item[1], fieldnames[2]: item[2], fieldnames[3]: item[3], fieldnames[4]: item[4]})
    for item in lons_and_temp_neg:
        writer.writerow(
            {fieldnames[0]: item[0], fieldnames[1]: item[1], fieldnames[2]: item[2], fieldnames[3]: item[3],
             fieldnames[4]: item[4]})


