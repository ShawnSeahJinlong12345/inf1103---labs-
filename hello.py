#first post
print("===========")
print("Welcome Here")
print("My First Post")
print("===========")    

#second post
username = "cool_creator"   
bio = "Fun Blogger"
followers = 100 

print("Username:", username)
print("Bio:", bio)
print("Followers:", followers)


#third post

followers = 100
followers += 50
print("Day 1:", followers)

followers += 20
print("Day 2:", followers)

followers -= 10
print("Day 3:", followers)


#fourth post

username = input("Enter Username: ")
age = input("Enter Age: ")
category = input("Enter Content Category: ")

print("\nInstagram Profile")
print("===========")
print("Username:", username)
print("Age:", age)
print("Category:", category)


#fifth post

username = input("Enter Username: ")
age = int(input("Enter Age: "))
category = input("Enter Content Category: ")

print("\nInstagram Profile")
print("===========")
print("Username:", username)
print("Age:", age)
print("Category:", category)


if age > 40 and category == "fun":
    print("You are old what is fun for you??")





stock_total = 0
failed_entries = 0

while True:
    stock = input("Enter a stock quantity (or 'quit' to stop): ")

    if stock.lower() == "quit":
        break

    elif not stock.isdigit():   
        print("Error: Invalid input. Please enter a whole number.")
        failed_entries += 1
        continue

    else:
        quantity = int(stock)  # safe to convert now, we know it's a valid number

        if quantity < 0:
            print("Error: Negative numbers are not allowed.")
            failed_entries += 1
            continue

        stock_total += quantity
        print(f"Accepted. Running total: {stock_total}")

        if stock_total > 500:
            print("OVERSTOCK ALERT: Inventory exceeds 500 units!")
            break

print("\n--- Final Report ---")
print(f"Total Units Processed: {stock_total}")
print(f"Number of Failed/Rejected Entries: {failed_entries}")