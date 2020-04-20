# input_data = {
#                 "region": {
#                 "name": "Africa",
#                 "avgAge": 19.7,
#                 "avgDailyIncomeInUSD": 5,
#                 "avgDailyIncomePopulation": 0.71
#                 },
#                 "periodType": "days",
#                 "timeToElapse": 58,
#                 "reportedCases": 674,
#                 "population": 66622705,
#                 "totalHospitalBeds": 1380614
#             }


# def covid19ImpactEstimator(input_data):

#     # impact = # solution for impact
#     # severeImpact = # solution for severe impact



#     response = {
#                 "data": input_data, # the input data you got
#                 "impact": {"impact": impact}, # your best case estimation
#                 "severeImpact": {"severeImpact":severeImpact} # your severe case estimation
#                 }

#     return response
            
# print(covid19ImpactEstimator(input_data))


# x - y + z = 30

import random


x = random.randint(-100, 100)
y = random.randint(-100, 100)
z = random.randint(-100, 100)

while not (y - x + z) == 30 or x%2 == 0 or y%2 == 0 or z%2 == 0:

    x = random.randint(0, 50)
    y = random.randint(0, 50)
    z = random.randint(0, 50)

else:
    print(x,y,z)