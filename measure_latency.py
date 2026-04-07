import requests
import time
import statistics

BASE_URL = "http://34.41.209.28:5000"

def measure(endpoint, n=50):
    latencies = []

    for i in range(n):
        payload = {
            "VIN": f"TESTVIN{i}_{endpoint.replace('/', '')}",
            "Make": "TESLA",
            "Model": "MODEL 3",
            "Model Year": 2024,
            "City": "Seattle"
        }

        start = time.perf_counter()
        response = requests.post(f"{BASE_URL}{endpoint}", json=payload, timeout=30)
        end = time.perf_counter()

        if response.status_code != 200:
            print(f"Request failed for {endpoint}: {response.text}")

        latencies.append((end - start) * 1000)

    return statistics.mean(latencies)

fast_avg = measure("/insert-fast")
safe_avg = measure("/insert-safe")

print(f"/insert-fast average latency: {fast_avg:.2f} ms")
print(f"/insert-safe average latency: {safe_avg:.2f} ms")
