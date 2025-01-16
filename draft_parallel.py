import concurrent.futures
import os 

# Fonction de travail
def task(i):
    return f"Task {i} completed"

if __name__ == '__main__':
    # Récupérer le nombre de cœurs logiques disponibles
    cpu_count = os.cpu_count()

    with concurrent.futures.ProcessPoolExecutor(max_workers=cpu_count) as executor:
        # Lancer plusieurs tâches en parallèle
        results = list(executor.map(task, range(cpu_count)))

    print(results)
