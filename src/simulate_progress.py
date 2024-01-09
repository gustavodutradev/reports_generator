import time
from tqdm import tqdm

class SimulateProgress:
    def __init__(self, stop_progress=False):
        self.stop_progress = stop_progress

    def start(self):
        self.stop_progress = False
        self.simulate_progress()

    def simulate_progress(self):
        for _ in tqdm(range(100)):
            time.sleep(0.25)
            if self.stop_progress:
                break

