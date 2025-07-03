import time
import numpy as np 

start_time = time.time()

#movie theater seat arrangement 'x' spots are marked for aisles screen is facing first row 
movie_seats = [
    ['x','x','x','x','x','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','x','x','x','x','x'],
    ['O','O','x','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','x','O','O'],
    ['O','O','x','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','x','O','O'],
    ['O','O','x','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','x','O','O'],
    ['O','O','x','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','x','O','O'],
    ['O','O','x','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','x','O','O'],
    ['O','O','x','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','x','O','O'],
    ['O','O','x','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','x','O','O'],
    ['O','O','x','x','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','x','x','O','O'],
]

def generate_fair_map(movie_seats):
    #initialize map with 0's 
    fair_map = np.zeros_like(movie_seats, dtype = 'object')
    
    rows = len(movie_seats)
    cols = len(movie_seats[0])
    mid = cols // 2
    
    #Compute score for each seat
    for r in range(rows):
        for c in range(cols):
            #skip aisles 
            if movie_seats[r][c] == 'x': 
                fair_map[r][c] = 'x'   
      
            else:
                #assign initial score based on how near the center it is 
                score = max(0, 10 - abs(mid - c))
                
                #adds 3 points to seats that are next to aisle 
                if 0 < c < cols-1:
                    if movie_seats[r][c-1] == 'x' or movie_seats[r][c+1] == 'x':
                        score += 3      
                         
                #since seats next to wall are spaced from center add 3 points
                if c == 0 or c == 1 or c == cols - 2 or c == cols - 1:
                    score += 3 
                     
                #removes 2 point's to first 3 rows in the front of screen 
                if r == 0 or r == 1 or r == 2:
                    score -= 2
                    
                #adds 2 points to the middle back     
                if (rows // 2) <= r <= rows - 1:
                    score += 2 
                    
                #gets rid of negative scores 
                score = max(0, score)
                #assign total score to seat 
                fair_map[r][c] = score
                
    return fair_map
             
def compute_score(block, fair_map):
    #keeps track of all the scores for each seat 
    scores = []
    
    for row, col in block:
        if fair_map[row][col] != 'x':
            score = fair_map[row][col]
            scores.append(score)
            
    #average score 
    return sum(scores) / len(scores)

def greedy(group_size, movie_seats, fair_map):
    #store possible blocks 
    possible_blocks = []
    
    best_block = None
    best_score = -1
    
    row = len(movie_seats)
    col = len(movie_seats[0])

   
    for r in range(row):
        #range to stay in bounds
        for c in range(col - group_size + 1):
            block = [(r, c + i) for i in range(group_size)]
            #if all seats available add to possible blocks 
            if all (movie_seats[row][col] == 'O' for (row, col) in block):
                possible_blocks.append(block)
        
    #get block with best score 
    for block in possible_blocks:
        score = compute_score(block, fair_map)
    
        #assign best score and block if new one found
        if score > best_score:
            best_score = score
            best_block = block
    
    #if no seats available
    if best_block is None:
        print(f"No valid seats for group size {group_size}")
        return 
        
    #assigned seats 
    print(f"best seats: {best_block} score: {best_score}" )
    
    #mark seat as reserved 
    for i, (r, c) in enumerate(best_block):
        movie_seats[r][c] = 'R'
        #leave space to right and left 
        if i == 0 and c - 1 >= 0 and movie_seats[r][c-1] == 'O':  
            movie_seats[r][c-1] = '-'
            
        if i == len(best_block) - 1 and c + 1 < col and movie_seats[r][c+1] == 'O':  
            movie_seats[r][c+1] = '-'
    
    return 

group_sizes = []

##Test cases## 

#1: testing with 1 group 
group_sizes.append(6)

#2:seeing how well it works with a various groups added 
group_sizes.append(5)
group_sizes.append(8)
group_sizes.append(9)
group_sizes.append(3)
group_sizes.append(7)
group_sizes.append(2)
group_sizes.append(5)
group_sizes.append(1)
group_sizes.append(3)
group_sizes.append(2)
group_sizes.append(2)
group_sizes.append(4)
group_sizes.append(3)
group_sizes.append(1)
group_sizes.append(3)
group_sizes.append(6)
group_sizes.append(4)
group_sizes.append(5)
group_sizes.append(7)
group_sizes.append(6)
group_sizes.append(5)
group_sizes.append(3)
group_sizes.append(4)
group_sizes.append(2)
group_sizes.append(2)


#3: testing for when there isn't enough seats for a group 
group_sizes.append(1)
group_sizes.append(2)
group_sizes.append(3)
group_sizes.append(5)
group_sizes.append(2)
group_sizes.append(9)
group_sizes.append(7)
group_sizes.append(5)
group_sizes.append(6)
group_sizes.append(8)

fair_map = generate_fair_map(movie_seats)

#calls greedy algorithm on each group
for group in group_sizes:
    greedy(group, movie_seats, fair_map)

#get rid of ' ' and replace x with . for aisles 
for row in movie_seats:
    print(' '.join(seat if seat != 'x' else '.' for seat in row))

#runtime of algorithm 
print("Process finished --- %s seconds --" % (time.time() - start_time))
        
    
