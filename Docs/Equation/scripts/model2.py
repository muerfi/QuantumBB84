import matplotlib.pyplot as plt
import numpy as np

# Valeurs de theta (de 0 à pi/2)
theta = np.linspace(0, np.pi/2, 100)
# Taux d'erreur = sin^2(theta)
error_rate = np.sin(theta)**2

plt.plot(theta, error_rate, label=r"Error Rate = $\sin^2(\theta)$", color="purple")
plt.xlabel(r"$\theta$ (radians)")
plt.ylabel("Error Rate")
plt.title("Error Rate vs. Attack Angle in Coherent Attack")
plt.legend()
plt.grid(True)
plt.savefig("C:/Users/Neqti/Downloads/figure2.png")
plt.show()
