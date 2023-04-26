import math 
import random

path_list_with_lengths = []

def data_input():
    print("----SELECTING NUMBER OF POINTS----")
    try:
        pts = input("Write number of points on the map\n")
        pts_dict = {}
        for x in range(int(pts)):
            x = input("Add the point. Separate X axis from Y axis with a ','. Don't add points with the same name. For example: A(5,2)\n")
            x = x.strip()
            point_name, point_params = x.split("(")
            point_params = point_params.replace(")", "")
            params_x, params_y = point_params.split(",")
            params = (int(params_x), int(params_y))
            if not point_name.isalnum():
               return f"Start program again and provide correct data." 
            pts_dict[point_name] = params
    except:
        print("Data has been provided incorrectly!")
        return f"Start program again and provide correct data."

    return pts_dict

def generate_path(my_dict):
    my_path = []
    unavailable_keys = list(my_dict.keys())
    while len(unavailable_keys) > 0:
        my_key = random.choice(unavailable_keys)
        my_path.append(my_key)
        unavailable_keys.remove(my_key)
    my_path.append(my_path[0]) 
    return my_path

def path_length_counter(my_dict, my_path_to_count):
    starting_len = 0
    for x in range(len(my_path_to_count)-1):
        tuple_1 = my_dict[my_path_to_count[x]]
        tuple_2 = my_dict[my_path_to_count[x+1]]
        path_length = math.sqrt((tuple_2[0]-tuple_1[0])**2 + (tuple_2[1]-tuple_1[1])**2)
        starting_len += path_length
    full_len = starting_len
    return full_len

def path_shuffle(my_path, tabu_dict: dict, tabu_iter):
    new_path = my_path
    idx_1 = random.randint(0, len(new_path)-2)
    idx_2 = random.randint(0, len(new_path)-2)
    if not tabu_dict:
        tabu_dict = {}
    if idx_1 != idx_2:
        if (new_path[idx_1], new_path[idx_2]) not in tabu_dict or (new_path[idx_2], new_path[idx_1]) not in tabu_dict:
            new_path[idx_1], new_path[idx_2] = new_path[idx_2], new_path[idx_1]
            new_path.pop()
            new_path.append(new_path[0])
            temp_x, temp_y = new_path[idx_1], new_path[idx_2]
            tabu_dict[(temp_x, temp_y)] = tabu_iter
            for move, iter in tabu_dict.items():
                if iter == 1:
                    del tabu_dict[move]
                else:
                    tabu_dict[move] = iter - 1
            return new_path
        else:
            return path_shuffle(new_path, tabu_dict, tabu_iter)
    else:
        return path_shuffle(new_path, tabu_dict, tabu_iter)

def ts_algorithm(iterations):
    data = data_input()
    n_path = generate_path(data)
    path_list_with_lengths.append((n_path, path_length_counter(data, n_path)))
    tabu_iters = input("How many iterations to drop elements for swapped elements in tabu list? ")  
    tabu_iters = int(tabu_iters) 
    tab_dic = []
    while iterations != 0:
        tmp = path_shuffle(n_path.copy(), tab_dic, tabu_iters)
        path_list_with_lengths.append((tmp, path_length_counter(data, tmp)))
        iterations -= 1
    print("Paths with lengths: ")
    print(path_list_with_lengths)
    print("Shortest path: ")
    shortest = min([el[1] for el in path_list_with_lengths])
    for el in path_list_with_lengths:
        if el[1] == shortest:
            print(el)



if __name__ == "__main__":
    iterations_to_stop = input("Select amount of iterations to stop search ")
    iterations_to_stop = int(iterations_to_stop)
    ts_algorithm(iterations_to_stop)
    
