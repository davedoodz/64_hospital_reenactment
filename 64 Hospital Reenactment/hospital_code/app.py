import csv   
import math
import operator
 
# csv file name  
filename = "SURE_64HospitalAssociationChart.csv"   
 
 
### this dictionary will map first_location_id to 0)placed or not (bool) 1)area (int) 2)location_matrix(lst) 3)centre(lst)
location_info = {}
 
selected = []
unselected = []
for i in range(21):
    unselected.append(i)
 
### initializing global variables with data of csv file
lst_area = []   
lst_total_journeys = []
size_square_matrix = 10   
 
 
# journeys   
association_chart = []   
# reading csv file   
with open(filename, 'r') as csvfile:   
    # creating a csv reader object   
    csvreader = csv.reader(csvfile)   
    # jump the room id   
    next(csvreader)   
    # attach every data row by row to a list (not including room_id)   
    for row in csvreader:   
        # last 2 columns of the csv file   
        lst_area.append(int(row[-1]))   
        lst_total_journeys.append(int(row[-2]))   
        #to rows (nested list)   
        association_chart.append(row[1:-2])   
# close   
csvfile.close()
 
### UPGRADE LOCATION_INFO DICT
for i in range (21):
    location_info[i+1] = [False]
    location_info[i+1].append(lst_area[i])
    
### STEP 1: Order generation ###
def ind_hottest_location():   
    '''   
    (None) -> (int)   
    computes from global list total_journeys the index of the hottest location   
    '''   
    i = lst_total_journeys.index(max(lst_total_journeys))   
 
    return i
 
def association_chart_of(index_location):
    '''   
    (None) -> (lst)   
    returns association chart that hottest has with other locations in list
    '''
    # all location connected journey to the hottest
    to_the_location = []
    for i in (association_chart[index_location]):
        if i != '':
            to_the_location.append(int(i))
    
    to_the_location.pop(-1)
    
    for i in (association_chart):
        if i[index_location]!= '':
            to_the_location.append(int(i[index_location]))
            
    return to_the_location
 
 
def ind_2nd_hottest_location():
    
    hottest = ind_hottest_location()
    location = max(association_chart_of(hottest))
    lst = association_chart_of(hottest)
    i = lst.index(location)
    return i
    
        
def order_location_placement():
    '''
    () -> (lst)    
    returns a list of integers i.e: room_id classified from hottest rooms to less hot
    
    () -> [13, 12, 14, 9, 10, 11, 7, 16, 8, 15, 3, 4, 20, 21, 19, 18, 17, 2, 1, 5, 6]
    
    '''
    selected.append(ind_hottest_location()+1)
    selected.append(ind_2nd_hottest_location()+1)
    unselected[ind_hottest_location()] = 999
    unselected[ind_2nd_hottest_location()] = 999
    
    # acculumative score will decide which next location
    sum_journeys = []
    max_ind = []
    
    ac_1st = association_chart_of(ind_2nd_hottest_location())
    ac_2nd = association_chart_of(ind_hottest_location())
    
    for i in range (21):
        sum_journeys.append(ac_1st[i]+ac_2nd[i])
    
    for i in range(16):
        max_journ = 0
        for i in range(21):
            if (sum_journeys[i] > max_journ and unselected[i]!= 999):
                max_journ = sum_journeys[i]
                
        #check for duplicates
        for i in range(21):
            if sum_journeys[i] == max_journ and unselected[i]!= 999:
                max_ind.append(i)
        
        for i in (max_ind):
            selected.append(i+1)
            unselected[i] = 999
            max_ind = []
            for j in range (21):
                sum_journeys[j] += association_chart_of(i)[j]
 
    return selected
 
 
 
### visualize ###
def create_bydefault_square_matrix(l):   
    '''  
    (int) -> (nested_lst)   
    create a square matrix filled with by-default value 0   
    as nested list   
    '''   
    cells = []   
    # generate 10x10 square grid   
    for i in range(l):   
        # initialize location of matrix (list)   
        sub_row_cells = []   
        for j in range (l):   
            # populate the matrix with by default 0   
            sub_row_cells.append(0)   
        #create the nested list   
        cells.append(sub_row_cells)   
    return cells
 
def viz_matrix(lst):  
 
    '''  
    (lst) -> ()   
    prints matrix row by row   
    '''  
    for row in lst:   
        print(row)
 
 
### PLACEMENT ###
 
def place_1st_cell_1st_location():
    '''
    place 1st_cell_1st_location + upgrade the location_info dict + upgrade the list placed
    '''
    x = y = int(size_square_matrix/2 - 1)
    first_first_location_id = id_placement_order[0]
    mtrx_id[y][x] = first_first_location_id
    
    #upgrade location_info dict with 1st cell matrix
    location_info [first_first_location_id].append([[y,x]])
    #upgrade location_info dict [0] placed = True
    location_info [first_first_location_id][0] = True
 
    # upgrade list placed
    placed.append(first_first_location_id)
    
    return [y, x]   
 
def place_remaining_cells_1st_location():
    '''
    place remaining cells of 1st_location + upgrade the location_info dict 
    '''
    first_location_id = id_placement_order[0]
    area = location_info.get(first_location_id)[1]
    first_cell_location = location_info.get(first_location_id)[2][0]
    
    y = first_cell_location[0]
    x = first_cell_location[1]
    
    # area = 2/+
    if area > 1:
        # upgrade location_info dict
        location_info[first_location_id][2].append([y+1, x])
        # place on mtrx_id
        mtrx_id[y+1][x] = first_location_id
        
        # area = 3/+
        if area > 2:
            location_info[first_location_id][2].append([y+1, x+1])
            mtrx_id[y+1][x+1] = first_location_id
            
            # area = 4/+
            if area > 3:
                location_info[first_location_id][2].append([y, x+1])
                mtrx_id[y][x+1] = first_location_id
                
                # area = 5/+
                if area > 4:
                    location_info[first_location_id][2].append([y+2, x])
                    mtrx_id[y+2][x] = first_location_id
                    
                    # area = 6
                    if area > 5:
                        location_info[first_location_id][2].append([y+2, x+1])
                        mtrx_id[y+2][x+1] = first_location_id
        
def find_centre (mtrx):
    '''
    (mtrx/nested lst) -> (lst)
    takes a location matrix as nested list and returns the midpoint of the matrix
 
    >>> find_centre([[4, 4], [5, 4], [5, 5], [4, 5]])
    >>> [4.5, 4.5]
 
    '''
    num_items = len(mtrx)
 
    sum_x = 0
    sum_y = 0
 
    x_mid = 0
 
    y_mid = 0
 
    for i in range(num_items):
        sum_x += mtrx[i][0]
        sum_y += mtrx[i][1]
        x_mid = sum_x/num_items
        y_mid = sum_y/num_items
        
    return [x_mid, y_mid]
 
def pose_first_location():
    '''
    place first location on mtrx_id
    '''
 
    first_location_id = order_location_placement()[0]
    # place the 1st cell of the 1st location
    place_1st_cell_1st_location()
    # place remaining cells
    place_remaining_cells_1st_location()
    # record centre (index 3) in the dict
    location_mtrx = location_info[first_location_id][2]
    centre = find_centre (location_mtrx)
    location_info[first_location_id].append(centre)
    
def occupied_matrix(mtrx):
    '''
    (lst) -> (lst)
    
    if element not equal to 0, it will be considered occupied
    '''
    om = []
    for index1, i in enumerate(mtrx):
        for index2, j in enumerate(i):
            #print(j)
            if j != 0:
                om.append([index1,index2])
    return om
 
def neighbor_cells(cell):
    '''
    (lst) -> (nested lst)
    takes as input a cell and returns its neighbor cells
 
    >>> neighbor_cells([4,4])
    >>> [[3,4],[4,3],[5,4],[4,5]]
    '''
    y = cell[0]
    x = cell[1]
 
    up_neighbor = [y,x-1]
    left_neighbor = [y-1,x]
    down_neighbor = [y, x+1]
    right_neighbor = [y+1,x]
 
    return [up_neighbor, left_neighbor, down_neighbor, right_neighbor]
 
 
def potential_position_for_1st_cell():
    '''
    () -> (nested lst)
 
    returns the adjacent cells of mtrx_id i.e. potential position for the 1st cell
 
    >>> mtrx = [[4,4],[4,5],[5,4],[5,5],[6,4],[6,5]]
    >>> potential_position_for_1st_cell(mtrx)
    >>> [3,4],[4,3],[5,3],[6,3],[7,4],[7,5],[6,6],[5,6],[4,6],[3,5]
 
    '''
    oc = occupied_matrix(mtrx_id)
    unsorted_positions = []
    potential_position_for_1st_cell = []
 
    for i in oc:
        unsorted_positions.append(neighbor_cells(i))
 
    for i in unsorted_positions:
        for j in i:
            if j not in oc and j not in potential_position_for_1st_cell:
                potential_position_for_1st_cell.append(j)
 
    return potential_position_for_1st_cell
 
 
def potential_position_for_remaining_cells(cells):
    '''
    (nested lst) -> (nested lst)
 
    takes as input a list of cells in form of nested list
    and returns its adjacent cells i.e. potential position for the 1st cell
    taking into account of not overlapping with placed cells
    
    '''
    oc = occupied_matrix(mtrx_id)
    unsorted_positions = []
    potential_position_for_next_cell = []
    #print ("oc =", oc)
    
    for i in cells:
        unsorted_positions.append(neighbor_cells(i))
        #potential_position_for_next_cell.append(neighbor_cells(i))
    for i in unsorted_positions:
        for j in i:
            if j not in oc:
                potential_position_for_next_cell.append(j)
    
    return potential_position_for_next_cell
 
def distance_between(loc1, loc2):
    '''
    (lst, lst) -> int
    
    computes the distance between loc1 & loc2
    
    >>> distance_between([1,2], [3,4]) # √(4-2)² + (3-1)² ~ 2.8
    >>> 2.8
    
    '''
    y1 = loc1[0]
    x1 = loc1[1]
    
    y2 = loc2[0]
    x2 = loc2[1]
    
    d = math.sqrt((x2-x1)**2 + (y2-y1)**2)
    
    return d
    
def first_cell_placer(location_id, second_1st_cell):
    '''
    (bool) -> (lst)
    
    among the potential locations, choose the location cell with the lowest
    distance score
    
    the second input is a boolean value taking into account of the special situations
    of the second location. Since there are many alternatives with the same distance score
    for the second, we choose the lower left corner (to be the same as the paper)
    in order to keep the same orientation for easier comparison
    
    '''
    
    # find potential cell loations
    potential_1st_cell_location = potential_position_for_1st_cell()
    
    # dict mapping all potential location to their distance score 
    dst_scores_for_potential_1st_location = {}
    
    for cell_position in potential_1st_cell_location:
        # every position key has a value of 0
        dst_scores_for_potential_1st_location[tuple(cell_position)] = 0
    
        for i in placed:
            centre = location_info[i][3]
            dst_score = distance_between(centre, cell_position)
            
            #take account of how the excel is constructed i.e.: blank spaces
            if (association_chart[i-1][location_id-1]) =='':
                multiplier = int(association_chart[location_id-1][i-1])
                #print('hi')
            else:
                multiplier = int(association_chart[i-1][location_id-1])
            
            # print(multiplier)
            dst_scores_for_potential_1st_location[tuple(cell_position)] += dst_score * multiplier
        
    # if we are placing the second location
    if second_1st_cell == True:
        ys = []
        for y, x in dst_scores_for_potential_1st_location:
            ys.append(y)
        max_y = max(ys)
        
        xs =[]
        for y, x in dst_scores_for_potential_1st_location:
            if y == max_y:
                xs.append(x)
        min_x = min(xs)
        
        first_cell_location = [max_y, min_x]
    
    else:
        # in case of duplicates
        min_value_keys = []
        min_key_value = min(dst_scores_for_potential_1st_location.items(), key=operator.itemgetter(1))[1]
        
        # check for duplicate
        for k, v in dst_scores_for_potential_1st_location.items():
            if v == min_key_value:
                min_value_keys.append(k)
                
        # arbitrarily choose 1st
        first_cell_location = min_value_keys[0]
        
    # place in mtrx_id
    mtrx_id[first_cell_location[0]] [first_cell_location[1]] = location_id
    # upgrade location_info dict with 1st cell matrix
    location_info [location_id].append([first_cell_location])
    # upgrade location_info dict [0] placed = True
    location_info [location_id][0] = True
    
    return first_cell_location
 
 
def count_x (lst):
    dct_count = {}
    for i in lst:
        v = lst.count(i)
        dct_count[i] = v
    return dct_count
 
 
def most_repeated (lst):
    '''
    (dct) -> (lst)
    >>> l = [1,2,1,4,5,3,2,5]
    >>> most_repeated(l)
    >>> [1, 2, 5]
    
    '''
    values = []
    most_repeated_values = []
 
    dct_count = count_x(lst) # {1: 2, 2: 2, 4: 1, 5: 2, 3: 1}
    for k, v in dct_count.items():
        values.append(v)
    
    max_v  = max(values)
    
    for k, v in dct_count.items():
        if v == max_v:
            most_repeated_values.append(k)
            
    return most_repeated_values
 
 
def too_vert_dispersed_warning (area, cell_locations):
    '''
    (int, lst) -> (bool)
    
    >>> too_vert_dispersed_warning (5, [[4,2],[5,2],[4,3],[5,3]])
    >>> True
    
    '''
    xs = []
    for i in cell_locations:
        x = i[1]
        xs.append(x) #[2,2,3,3]
    
    # lst
    most_repeated_xs = most_repeated(xs) #[2,3]
    
    # suffices to count most_repeated_xs index 0, since they all have the same highest count
    c = xs.count(most_repeated_xs[0])
    
    if area == 3 or area == 4:
        if c == 2:
            return True
        elif c > 2:
            return 'over'
    
    elif area == 5 or area == 6:
        if c == 3:
            return True
        elif c > 3:
            return 'over'
    
    return False
 
def too_vert_dispersed_x_value (area, cell_locations):
    '''
    (int, lst) -> (lst)
    
    '''
    xs = []
    for i in cell_locations:
        x = i[1]
        xs.append(x) #[2,2,3,3]
    
    # lst
    most_repeated_xs = most_repeated(xs) #[2,3]
    
    return most_repeated_xs
 
def too_hori_dispersed_warning (area, cell_locations):
    '''
    (int, lst) -> (bool)
    
    >>> too_vert_dispersed_warning (5, [[2,4],[2,5],[3,4],[3,5]])
    >>> True
    
    '''
    xs = []
    for i in cell_locations:
        x = i[0]
        xs.append(x) #[2,2,3,3]
    
    # lst
    most_repeated_xs = most_repeated(xs) #[2,3]
    
    # suffices to count most_repeated_xs index 0, since they all have the same highest count
    c = xs.count(most_repeated_xs[0])
    
    if area == 3 or area == 4:
        if c == 2:
            return True
        elif c > 2:
            return 'over'
    
    elif area == 5 or area == 6:
        if c == 3:
            return True
        elif c > 3:
            return 'over'
    
    return False
 
def too_hori_dispersed_y_value (area, cell_locations):
    '''
    (int, lst) -> (lst)
    
    '''
    xs = []
    for i in cell_locations:
        x = i[0]
        xs.append(x) #[2,2,3,3]
    
    # lst
    most_repeated_xs = most_repeated(xs) #[2,3]
    
    return most_repeated_xs
 
def remaining_cells_placer(location_id, cells_location, area):
    
    # loop through by alway upgrading cell_location in location_info dct
    for i in range(area-1):
        cell_potential_locations = potential_position_for_remaining_cells(cells_location)
 
        # dict mapping all potential location to their distance score 
        dst_scores_for_potential_next_location = {}
    
        for cell_position in cell_potential_locations:
            # too_vert_dispersed_warning (area, cell_locations)
            # every position key has a value of 0
            dst_scores_for_potential_next_location[tuple(cell_position)] = 0
        
            for i in placed:
                centre = location_info[i][3]
                dst_score = distance_between(centre, cell_position)
                #take account of how the excel is constructed i.e.: blank spaces
                if (association_chart[i-1][location_id-1]) =='':
                    multiplier = int(association_chart[location_id-1][i-1])
                else:
                    multiplier = int(association_chart[i-1][location_id-1])
                dst_scores_for_potential_next_location[tuple(cell_position)] += dst_score * multiplier
                
                # if the warning is triggered, penalize the far x with a dummy score of 9999 
                if too_vert_dispersed_warning (area, cells_location):
                    lst_xs_to_penalize = too_vert_dispersed_x_value (area, cells_location)
                    if cell_position[1] in lst_xs_to_penalize:
                        dst_scores_for_potential_next_location[tuple(cell_position)] += 9999
                elif too_hori_dispersed_warning (area, cells_location):
                    lst_ys_to_penalize = too_hori_dispersed_y_value (area, cells_location)
                    if cell_position[0] in lst_ys_to_penalize:
                        dst_scores_for_potential_next_location[tuple(cell_position)] += 9999
                
        ###################################################################################
        min_value_keys = []
        
        min_key_value = min(dst_scores_for_potential_next_location.items(), key=operator.itemgetter(1))[1]
        
        
        # check for duplicate
        for k, v in dst_scores_for_potential_next_location.items():
            if v == min_key_value:
                min_value_keys.append(list(k))
                
        # arbitrarily choose 1st
        next_cell_location = min_value_keys[0]
        
        # upgrade mtrx_id
        mtrx_id[next_cell_location[0]][next_cell_location[1]] = location_id
        # upgrade location_info dict
        location_info[location_id][2].append(next_cell_location)
 
        print(dst_scores_for_potential_next_location)
    
    
# list in order of the procedureal placement 
id_placement_order = order_location_placement()
placed = []
 
#id matrix for viz
mtrx_id = create_bydefault_square_matrix(size_square_matrix)
 
###
pose_first_location()
 
for i, location_id in enumerate(id_placement_order[1:21]):
    if i == 0:
        second_1st_cell = True
    else:
        second_1st_cell = False
        
    first_cell_placer(location_id, second_1st_cell)
    first_cell_location_mtrx = location_info[location_id][2][0]
    # remaining cells placement
    area = location_info[location_id][1]
    cells_location = location_info[location_id][2]
    remaining_cells_placer(location_id, cells_location, area)
    # upgrade placed list
    placed.append(location_id)
    # upgrade location_info with centre
    centre = find_centre(location_info[location_id][2])
    location_info[location_id].append(centre)
 
print('\t')
print(location_info)
print('\t')
viz_matrix(mtrx_id)
print('\t')
print(placed)
 
 
