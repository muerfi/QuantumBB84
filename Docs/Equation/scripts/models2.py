import matplotlib.pyplot as plt
import numpy as np

# Theta values (from 0 to π/2)
theta = np.linspace(0, np.pi/2, 100)
# Error rate = sin²(theta)
error_rate = np.sin(theta)**2

plt.plot(theta, error_rate, label=r"Error Rate = $\sin^2(\theta)$", color="purple")
plt.xlabel(r"$\theta$ (radians)")
plt.ylabel("Error Rate")
plt.title("Error Rate vs. Attack Angle in Coherent Attack")
plt.legend()
plt.grid(True)
plt.savefig("C:/Users/") # Change the path
plt.show()
