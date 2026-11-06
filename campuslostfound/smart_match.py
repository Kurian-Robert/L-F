def levenshtein_distance(str1, str2):
    # Create a 2D matrix (Dynamic Programming table)
    dp = [[0 for _ in range(len(str2) + 1)] for _ in range(len(str1) + 1)]

    for i in range(len(str1) + 1):
        for j in range(len(str2) + 1):
            if i == 0:
                dp[i][j] = j    # Min operations = j insertions
            elif j == 0:
                dp[i][j] = i    # Min operations = i deletions
            elif str1[i-1].lower() == str2[j-1].lower():
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(dp[i][j-1],      # Insert
                                   dp[i-1][j],      # Remove
                                   dp[i-1][j-1])    # Replace

    return dp[len(str1)][len(str2)]

def find_best_match(search_term, linked_list_head):
    if not linked_list_head:
        return "No items in database."

    best_match = None
    lowest_distance = float('inf')
    
    current = linked_list_head
    while current:
        item_name = current.data["name"]
        dist = levenshtein_distance(search_term, item_name)
        
        # If it's a closer match (fewer edits needed), update the best match
        if dist < lowest_distance:
            lowest_distance = dist
            best_match = item_name
            
        current = current.next

    # If the distance is small enough (4 or fewer edits), consider it a smart match
    if lowest_distance <= 4: 
        return f"Did you mean: '{best_match}'? (Edit distance: {lowest_distance})"
    return "No close matches found."