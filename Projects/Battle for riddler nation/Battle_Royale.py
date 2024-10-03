import random
import pandas as pd


def randomize_list_to_sum(length, total_sum):
    weights = []
    nums = []
    for i in range(length):
        weights.append(random.random())

    total = sum(weights)

    for weight in weights:
        nums.append(round((weight / total) * total_sum))

    current_sum = sum(nums)
    while current_sum != total_sum:
        index = random.randint(0, len(nums) - 1)
        if current_sum > total_sum and nums[index] > 0:
            nums[index] -= 1
        elif current_sum < total_sum:
            nums[index] += 1
        current_sum = sum(nums)
    return nums

def row_to_list(row):
    values = []
    for i in range(10):
        values.append(row.iloc[i])
    return values

def data_frame_to_list(df):
    rows = []
    for index, row in df.iterrows():
        rows.append(row_to_list(row))
    return rows

def castle_game(split1, split2):
    split1_points = 0
    split2_points = 0
    for i in range(10):
        if split1[i] > split2[i]:
            split1_points += i
        elif split1[i] < split2[i]:
            split2_points += i
        else:
            split1_points += i / 2
            split2_points += i / 2
    return split1_points, split2_points

def get_win_percentage(split, solutions):
    total_wins = 0
    for solution in solutions:
        split_points, solution_points = castle_game(split, solution)
        total_wins += 1 if split_points > solution_points else 0
    return total_wins / len(solutions)

def random_non_repeating_numbers(lower_bound, upper_bound, count):
    all_numbers = []
    random_choices = ()
    for i in range(lower_bound, upper_bound):
        all_numbers.append(i)
    for i in range(count):
        index = random.randint(0, len(all_numbers) - 1)
        random_choices = random_choices + (all_numbers[index],)
        all_numbers.pop(index)
    return random_choices

def mutate(split, mutate_count, mutate_strength):
    for i in range(mutate_count):
        source, destination = random_non_repeating_numbers(0, len(split) - 1, 2)
        amount = min(split[source], mutate_strength)
        split[source] -= amount
        split[destination] += amount

def crossover(split1, split2):
    total = sum(split1)
    weights = []
    for i in range(len(split1)):
        r = random.randint(1, 2)
        if r == 1:
            weights.append(split1[i])
        else:
            weights.append(split2[i])
    weights_total = sum(weights)
    offspring = [round((weights[i] / weights_total) * total) for i in range(len(weights))]

    current_sum = sum(offspring)
    while current_sum != total:
        index = random.randint(0, len(offspring) - 1)
        if current_sum > total and offspring[index] > 0:
            offspring[index] -= 1
        elif current_sum < total:
            offspring[index] += 1
        current_sum = sum(offspring)

    return offspring



def get_top_solutions(solutions, data, count=5):
    solutions_and_wins = pd.DataFrame(columns=['solution', 'win percentage'])

    for solution in solutions:
        solutions_and_wins.loc[len(solutions_and_wins.index)] = [solution, get_win_percentage(solution, data)]
    sorted_solutions = solutions_and_wins.sort_values(by='win percentage', ascending=False)
    chosen_solutions = sorted_solutions.head(count)

    return [chosen_solutions.iloc[i]['solution'] for i in range(count)]

def populate_gen(top_solutions, count, mutation_constant):
    new_gen = []
    for i in range(len(top_solutions)):
        new_gen.append(top_solutions[i])
    while len(new_gen) - len(top_solutions) < count:
        for i in range(len(top_solutions)):
            s1 = top_solutions[i]
            for j in range(len(top_solutions)):
                s2 = top_solutions[j]
                if i != j:
                    offspring = crossover(s1, s2)
                    mutate(offspring, round(mutation_constant), round(mutation_constant * 0.1) + 1)
                    new_gen.append(offspring)
                    if len(new_gen) - len(top_solutions) >= count:
                        return new_gen
    return new_gen

def check_repeating_values(values, count):
    for i in range(len(values) - 1, len(values) - count, -1):
        if values[i] != values[i-1]:
            return False
    return True

if __name__ == '__main__':
    GENERATIONS = 100
    OFFSPRING_COUNT = 100
    solutions = data_frame_to_list(pd.read_csv('data/castle-solutions.csv'))
    current_solutions = [randomize_list_to_sum(10, 100) for i in range(100)]
    top_solutions = get_top_solutions(current_solutions, solutions)
    best_solution_history = []

    for i in range(GENERATIONS):
        print(f'Generation {i + 1} of {GENERATIONS}')
        print(top_solutions[0], get_win_percentage(top_solutions[0], solutions))
        best_solution_history.append(top_solutions[0])
        mutation_magnitude = GENERATIONS - i
        if i > (GENERATIONS / 10):
            if check_repeating_values(best_solution_history, 3):
                mutation_magnitude = 30
        current_solutions = populate_gen(top_solutions, OFFSPRING_COUNT, mutation_magnitude)
        top_solutions = get_top_solutions(current_solutions, solutions)


