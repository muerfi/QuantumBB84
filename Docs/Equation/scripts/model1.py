import matplotlib.pyplot as plt

attack_types = ["No Eve", "Intercept-Resend", "Coherent"]
error_rates = [0, 0.25, 0.15]

plt.bar(attack_types, error_rates, color=['green', 'red', 'blue'])
plt.xlabel("Attack Type")
plt.ylabel("Error Rate")
plt.title("Error Rates in BB84 Simulations")
plt.savefig("C:/Users/") #Change the path
plt.show()
