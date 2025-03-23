import matplotlib.pyplot as plt
import numpy as np

# Fonction pour calculer l'entropie binaire H(p)
def binary_entropy(p):
    p = np.clip(p, 1e-10, 1 - 1e-10)  # Évite log(0)
    return -p * np.log2(p) - (1 - p) * np.log2(1 - p)

# Valeurs de theta (de 0 à pi/2)
theta = np.linspace(0, np.pi/2, 100)
# Taux d'erreur = sin^2(theta)
error_rate = np.sin(theta)**2

# I(A:E) = H(sin^2(theta))
I_AE = binary_entropy(error_rate)

# I(A:B) = 1 - H(sin^2(theta)) (simplifié, capacité maximale moins entropie d'erreur)
I_AB = 1 - binary_entropy(error_rate)

plt.plot(theta, I_AE, label=r"$I(A:E)$", color="red")
plt.plot(theta, I_AB, label=r"$I(A:B)$", color="blue")
plt.xlabel(r"$\theta$ (radians)")
plt.ylabel("Mutual Information (bits)")
plt.title("Mutual Information vs. Attack Angle")
plt.legend()
plt.grid(True)
plt.savefig("C:/Users/Neqti/Downloads/figure3.png")
plt.show()
