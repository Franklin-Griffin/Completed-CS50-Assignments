from cs50 import get_string

text = get_string("Text: ")
length = len(text)
L = 0.0
S = 0.0
# Word count (the first letter will not be a space, so make sure to count the first word)
W = 1.0
for i in text:
    if i.isalpha():
        L += 1
    elif i == ' ':
        W += 1
    elif i == '.' or i == '?' or i == '!':
        S += 1

# Normalize based on word count
L = L * 100.0 / W
S = S * 100.0 / W

# Coleman-Liau index test
index = round(0.0588 * L - 0.296 * S - 15.8)

if index < 1:
    print("Before Grade 1")
elif (index > 16):
    print("Grade 16+")
else:
    print(f"Grade {index}")