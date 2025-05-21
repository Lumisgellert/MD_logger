import time
start = time.time()
for _ in range(100000):
    print("johjaflkdsjgfoöasdpgljpalsedäfhfdgshsfghfsgh")  # oder print("x") bei weniger Output
end = time.time()
print(f"Dauer: {end - start:.2f} Sekunden")
