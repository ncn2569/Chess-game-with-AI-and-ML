import src.genetic_algorithm as ga
from src import config
import time

# Các hằng số cho GA
POPULATION_SIZE = 20
NUM_GENERATIONS = 10
NUM_WEIGHTS = 6 # (pawn, knight, bishop, rook, queen, king_safety - ví dụ)
GA_SEARCH_DEPTH = 1 # Độ sâu tìm kiếm khi huấn luyện (phải thấp)
MUTATION_RATE = 0.1
MUTATION_STRENGTH = 10 # +/- 10 điểm trọng số

def run_training():
    """
    Chạy vòng lặp huấn luyện GA.
    TODO: Người dùng sẽ hoàn thiện logic này khi đã code xong 
    src/genetic_algorithm.py
    """
    print("Bắt đầu quá trình huấn luyện AI (headless)...")
    start_time = time.time()

    # (Người dùng tự hiện thực logic)
    # 1. Khởi tạo quần thể
    # population = ga.initialize_population(POPULATION_SIZE, NUM_WEIGHTS)
    
    # 2. Vòng lặp qua các thế hệ
    # for gen in range(NUM_GENERATIONS):
    #    print(f"--- Thế hệ {gen + 1}/{NUM_GENERATIONS} ---")
    #
    #    a. Tính fitness cho từng cá thể
    #    pop_with_fitness = []
    #    for chromosome in population:
    #        fitness = ga.calculate_fitness(chromosome, 
    #                                       config.STANDARD_WEIGHTS, 
    #                                       GA_SEARCH_DEPTH)
    #        pop_with_fitness.append((chromosome, fitness))
    #
    #    b. Sắp xếp và chọn lọc
    #    pop_with_fitness.sort(key=lambda x: x[1], reverse=True)
    #    print(f"Best fitness: {pop_with_fitness[0][1]}")
    #    print(f"Best weights: {pop_with_fitness[0][0]}")
    #
    #    parents = ga.selection(pop_with_fitness)
    #
    #    c. Lai ghép và đột biến
    #    new_population = [pop_with_fitness[0][0]] # Elitism
    #    while len(new_population) < POPULATION_SIZE:
    #        parent1, parent2 = random.sample(parents, 2)
    #        child = ga.crossover(parent1, parent2)
    #        child = ga.mutate(child, MUTATION_RATE, MUTATION_STRENGTH)
    #        new_population.append(child)
    #
    #    population = new_population

    end_time = time.time()
    print(f"Hoàn tất huấn luyện sau {end_time - start_time:.2f} giây.")
    print("Bộ trọng số tốt nhất tìm được (ví dụ):")
    print(config.STANDARD_WEIGHTS) # In ra bộ trọng số tốt nhất

if __name__ == "__main__":
    print("LƯU Ý: Đây là file khung.")
    print("Người dùng cần hiện thực src/genetic_algorithm.py trước khi chạy file này.")
    # run_training() # Bỏ comment khi người dùng đã sẵn sàng