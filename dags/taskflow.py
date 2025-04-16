from airflow.decorators import dag,task
from datetime import datetime, timedelta
import random

@dag(
    start_date = datetime(2023,1,1),
    schedule = '@daily',
    catchup = False,
    tags = ['generate_random']
)

def generate_random():

    @task
    def generate_random_number():
        number = random.randint(1,100)   
        print("Generate number is " + str(number))
        return number
    
    @task
    def check_odd_even(number):
        result = ""
        if number%2 == 0:
            result = "even"
        else:
            result = "odd"
        print("Result is " + result)
    
    check_odd_even(generate_random_number())

generate_random()