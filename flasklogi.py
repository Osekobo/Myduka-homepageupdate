

# def ngg():
#   print("welcome")
#   print("im thinking")

# ntg = random.randint(1,100)
# n_o_t = 0

# while True:
#  guess = input("Enter your guess(or type 'exit' to quit): ")

#  if guess.lower() == 'exit':
#     print(f"Goodbye! the number to guess was {ntg}.")
#     break

#  if not guess.isdigit():
#     print("Invalid number")
#     continue

#  guess = int(guess)
#  n_o_t += 1

#  if guess < ntg:
#     print("too low")
#  elif guess > ntg:
#     print("too high")
#  else:
#     print(f"correct{n_o_t}")
#     break

# ngg()

from flask import Flask, render_template, request, redirect, url_for, flash, session
import random

app = Flask(__name__)


# @app.route('/ono', methods=['GET', 'POST'])
# def num():
#     ntg = random.randint(1, 6)
#     ntg2 = random.randint(1, 6)
#     return render_template("on.html", ntg=ntg, ntg2 = ntg2)


app.run(debug=True)
