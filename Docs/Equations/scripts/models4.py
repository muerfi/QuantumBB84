import numpy as np
import matplotlib.pyplot as plt

# Parameters
n_bits = 100  # Key length
noise_level = 0.1  # Noise rate (10% errors)

# Generate Alice's key (random bits)
alice_key = np.random.randint(0, 2, n_bits)

# Simulate a noisy channel (Bob receives the key with errors)
bob_key = alice_key.copy()
noise_indices = np.random.choice(n_bits, int(n_bits * noise_level), replace=False)
bob_key[noise_indices] = 1 - bob_key[noise_indices]  # Flip noisy bits

# Compute errors
errors = alice_key != bob_key
error_positions = np.where(errors)[0]
error_counts = np.sum(errors)

# Visualization
plt.figure(figsize=(10, 3))
plt.plot(range(n_bits), alice_key, label="Alice's Key", color="blue", linestyle="--")
plt.plot(range(n_bits), bob_key, label="Bob's Key", color="red", linestyle="-")
plt.scatter(error_positions, bob_key[error_positions], color="black", label="Errors", zorder=5)
plt.xlabel("Bit Position")
plt.ylabel("Bit Value")
plt.title(f"Key Distribution with Noise (Error Rate = {error_counts/n_bits:.2f})")
plt.legend()
plt.grid(True)
plt.savefig("C:/Users/") # Change the path
plt.show()
