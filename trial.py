con = "hi mama\n at\ttula     v     rra \n\n\n\n varii"

print(con)
print("strip")
con = con.replace("\n", "")
con = con.replace("  ", "")
con = con.replace("\t", "")
print(con)