import requests

url = "http://127.0.0.1:8000/calculate_total?food_type=Non%20-%20Veg&plan_type=Basic&num_people=3&meal_type=1%20Meal%20Lunch&services=D"

response = requests.request("GET", url)

print(response.text)
