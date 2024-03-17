# import crud_api 
# import scraping_script
# import sqlite3
DATABASE_PATH = "..\\data\\pricetracking.db"

import difflib
def compute_similarity(input_string, reference_string):
#The ndiff method returns a list of strings representing the differences between the two input strings.
    diff = difflib.ndiff(input_string, reference_string)
    diff_count = 0
    for line in diff:
      # a "-", indicating that it is a deleted character from the input string.
        if line.startswith("-"):
            diff_count += 1
# calculates the similarity by subtracting the ratio of the number of deleted characters to the length of the input string from 1
    return 1 - (diff_count / len(input_string))
 

#This code is contributed by Edula Vinay Kumar Reddy

# def updatePrices():
#     products_list = crud_api.get_all_products();
#     list = {}
#     for i , name in enumerate(products_list):
#         data = scraping_script.get_prices(name[0])
#         list[name] = data
        
    
#     for l in list:
#         print(l , " ---------> ",list[l])
    
    
def main():
    input_string = "תשבי מלבק"
    reference_string = "יין אדום תשבי מלבק"
    similarity = compute_similarity(input_string, reference_string)
    print(similarity)
    #print(crud_api.get_all_products())
main()




