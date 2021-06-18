def levenshtein_distance(word1,word2):
    #initialize levenstein distance for word 2 with null string
    distances = [i for i in range(0,len(word2)+1)]

    #compare words
    for letter_index_word1 in range(0,len(word1)):
        current_letter_word1 = word1[letter_index_word1]
        #handle case of null comparisons for diagonal for prior letter
        diagonal_distance = distances[0]
        distances[0] = letter_index_word1+1
        for letter_index_word2 in range(0,len(word2)):
            distances_index = letter_index_word2 + 1 #account for null string at beginning
            if current_letter_word1 == word2[letter_index_word2]:
                #simply copy last diagnol distance as current distance
                current_distance = diagonal_distance
            else:
                current_distance = min(distances[distances_index - 1],distances[distances_index],diagonal_distance) + 1

            #store the prior current distance in the list to diagonal_distance for new comparison
            temp = distances[distances_index]
            distances[distances_index]=current_distance
            diagonal_distance=temp
    return distances.pop()


if __name__ == "__main__":
    test_word = "book"
    test_scores = {"book":0,"back":2,"playground":9,"cat":4,"dog":3,"basic":4,"surfer":6,"garlic":6,"ninja":5}
    print(f"Testing again: {test_word}")
    for word in test_scores.keys():
        score = levenshtein_distance(test_word,word)
        expected = test_scores[word]
        pass_fail = "Pass" if score == expected else "Fail"
        print(f"{word}:\t Expected: {expected} \t Result: {score} ... {pass_fail} ")