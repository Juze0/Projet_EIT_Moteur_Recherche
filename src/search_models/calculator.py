from abc import ABC
from time import time

class Calculator(ABC):

    def __init__(self):
        pass


    def calculate(self, calculation_func, *args, **kwargs):
        print(f"Début du calcul...")
        start_time = time.time()
        calculated_data = calculation_func(*args, **kwargs)
        end_time = time.time()
        print(f"➥ Le calcul s'est terminée en {self.get_creation_duration_time(start_time, end_time)}!")
        return calculated_data
    

    def get_creation_duration_time(self, start_time, end_time):
        creation_time = end_time - start_time
        if creation_time < 60:
            return f"{creation_time:.4f} secondes"
        return f"{creation_time / 60:.2f} minutes"