from config_loader import config

key = config["openai_key"]

from openai import OpenAI

rules = """
The sorting system follows specific rules to categorize items into different sections of a grocery store. Here are the rules based on the provided categories. Make no other assumptions about misspellings, and include no commentary in the output other than just the sorted list. 

1. **Milk:**
   - Include items like various types of milk and milk substitutes (e.g., oat milk).

2. **Cheese:**
   - Include various types of cheese, excluding fancy or specialized cheeses.

3. **Fancy Cheese:**
   - This category is not used in the provided sorting system.

4. **Deli:**
   - Include deli items such as sandwich pepperoni and bacon.

5. **Personal Care:**
   - Include personal care items such as diapers, tissues, and liquid Claritin.

6. **Produce:**
   - Include fresh fruits, vegetables, herbs, and other produce items.

7. **Meat:**
   - Include various types of meat like chicken breasts and ground lamb.

8. **Canned Goods:**
   - Include items that come in cans, jars, or similar packaging, such as black beans, tomato paste, and broth.

9. **Cleaning Goods:**
   - Include cleaning supplies like baking soda and trash bags.

10. **Snacks:**
    - Include snack items like granola.

11. **Frozen Foods:**
    - Include items that are typically found in the freezer section, such as frozen waffles and gnocchi.

12. **Pasta:**
    - Include various types of pasta, noodles, or related items.

13. **Baking Supplies:**
    - This category is not used in the provided sorting system.

14. **Other:**
    - Include items that don't fit neatly into the other categories, such as condiments (e.g., salsa), spices (e.g., cumin), and miscellaneous grocery items.

These rules aim to efficiently categorize a diverse list of grocery items into specific sections, making it easier to organize and navigate during a shopping trip.
"""

grocery_list = """
Half and half
Yogurt 
Fruit
Snack cheese
Big tomato sauce x 2
Big whole tomato 
Broth 
Red wine 
Onion x 2
Parm
Italian sausage 
Penne x2
Eggs 
Black beans  
Cilantreeo
Jalapeño
Spinach
Herbs 
Salad greens
Waffles
Good bread
Cooper cheese
Cheddar 
Mexican cheese 
Banana 
Whole grain crackers 
Snap peas 
Cashews 
English muffins 
Jelly
Tommy diapers 
Mac and cheese box
Christmas cookies
"""

def do_grocery_sort(items):
  global rules
  client = OpenAI(
     api_key=key,
   )

  completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
      {"role": "system", "content": f"You are a grocery assistant, sorting grocery lists into categories. Use the below rules to perform the sorting. Under no condition should you include any commentary in the output, such as as stating your assumptions.\n {rules}"},
      {"role": "user", "content": f"Sort the following list:\n{items}"}
    ]
  )

  response = completion.choices[0].message.content
  return response

if __name__ == "__main__":
  print(do_grocery_sort(grocery_list))