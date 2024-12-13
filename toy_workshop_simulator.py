import random
import datetime
import json
import time

class ToyWorkshopSimulator:
    def __init__(self):
        self.toy_types = {
            'robot': {'base_rate': 100, 'complexity': 0.8},
            'doll': {'base_rate': 150, 'complexity': 0.6},
            'car': {'base_rate': 200, 'complexity': 0.5},
            'puzzle': {'base_rate': 120, 'complexity': 0.7},
            'board_game': {'base_rate': 80, 'complexity': 0.9}
        }
        
        self.production_lines = {
            'line1': {'efficiency': 0.95, 'error_rate': 0.02},
            'line2': {'efficiency': 0.90, 'error_rate': 0.03},
            'line3': {'efficiency': 0.85, 'error_rate': 0.04}
        }
        
        self.elves = [f"elf_{i}" for i in range(1, 21)]  # 20 elves
        
    def calculate_production_rate(self, toy_type, line_efficiency):
        base_rate = self.toy_types[toy_type]['base_rate']
        complexity = self.toy_types[toy_type]['complexity']
        return int(base_rate * line_efficiency * (1 + random.uniform(-0.1, 0.1)))
    
    def generate_toy_data(self):
        # Select random toy type and production line
        toy_type = random.choice(list(self.toy_types.keys()))
        prod_line = random.choice(list(self.production_lines.keys()))
        
        # Get line characteristics
        line_data = self.production_lines[prod_line]
        
        # Calculate production metrics
        production_rate = self.calculate_production_rate(toy_type, line_data['efficiency'])
        
        # Generate random events
        is_error = random.random() < line_data['error_rate']
        errors_detected = random.randint(1, 5) if is_error else 0
        
        # Quality score calculation (affected by errors)
        base_quality = random.normalvariate(95, 3)
        quality_score = max(min(int(base_quality - (errors_detected * 5)), 100), 0)
        
        return {
            "@timestamp": datetime.datetime.now().isoformat(),
            "toy_type": toy_type,
            "production_line": prod_line,
            "production_rate": production_rate,
            "quality_score": quality_score,
            "elf_id": random.choice(self.elves),
            "errors_detected": errors_detected,
            "temperature": round(random.uniform(20.0, 25.0), 1),
            "humidity": round(random.uniform(45.0, 55.0), 1),
            "shift": self.get_current_shift(),
            "machine_status": "error" if errors_detected > 3 else "normal",
            "toys_completed": int(production_rate / 4),  # toys completed in this batch
            "version": "8.16.1"
        }
    
    def get_current_shift(self):
        hour = datetime.datetime.now().hour
        if 6 <= hour < 14:
            return "morning"
        elif 14 <= hour < 22:
            return "evening"
        else:
            return "night"

def main():
    simulator = ToyWorkshopSimulator()
    
    try:
        while True:
            data = simulator.generate_toy_data()
            print(json.dumps(data))
            time.sleep(1)  # Generate data every second
            
    except KeyboardInterrupt:
        print("\nStopping toy production simulation...")

if __name__ == "__main__":
    main()