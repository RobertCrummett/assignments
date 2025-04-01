import numpy as np
from matplotlib import pyplot as plt

data = np.loadtxt("profile.txt")
x = data[:,0] * 1000
z = data[:,1] / 100 / 1000

# Vertical gravity field due to a prism of infinite 
# extent in one horizontal direction
def gz(x, a, b, h2, h1):
    assert a < b, "a must be less than b"
    if h1 == h2:
        return 0
    elif h1 > h2:
        h2, h1 = h1, h2

    k = 6.67e-11 # SI units
    s = 1000 * 0.17 # kg / m^3
    g2 = h2 * (np.arctan2((x - a), h2) + np.arctan2((b - x), h2)) + \
         (x - a) / 2 * np.log(np.abs((x - a)**2 + h2**2)) + \
         (b - x) / 2 * np.log(np.abs((b - x)**2 + h2**2))
    g1 = h1 * (np.arctan2((x - a), h1) + np.arctan2((b - x), h1)) + \
         (x - a) / 2 * np.log(np.abs((x - a)**2 + h1**2)) + \
         (b - x) / 2 * np.log(np.abs((b - x)**2 + h1**2))
    return 2 * k * s * (g2 - g1)

h1 = 23 * 1000
h2 = 34 * 1000

def F(data_locations, model):
    total = np.zeros_like(data_locations)
    ab = np.linspace(data_locations[0], data_locations[-1], model.size + 1, endpoint=True)

    for _a, _b, _dh in zip(ab[:-1], ab[1:], model):
        total += gz(data_locations, _a, _b, h2, h2 - _dh)
    return total

def J(data_locations, model):
    pert = 100
    model_p = model.copy()
    jacobian = np.zeros((data_locations.size, model.size))

    for i in range(model.size):
        model_p[i] += pert
        jacobian[:,i] = (F(data_locations, model_p) - F(data_locations, model)) / pert
        model_p[i] = model[i]
    return jacobian

def backtracking(objective_function, data_locations, model, update, jacobian):
    alpha = 1
    rho = 0.925
    c = 0.1
    f = F(data_locations, model)
    maxiter = 1000
    iter = 0
    while F(data_locations, model + alpha * update) > f + c * alpha * jacobian @ update:
        alpha *= rho
        iter += 1
        if iter > maxiter:
            raise ValueError("Max iterations have been reached while back tracking")
    return alpha

model_locations = np.linspace(0, 462.5, 100) * 1000
model = np.ones_like(model_locations) * 9000 # np.random.rand(model_locations.size) * 8000
dx = abs(model_locations[1] - model_locations[0])
WmTWm = dx * np.eye(model_locations.size)

beta = 1e-18
jacobian = J(x, model)
g = jacobian.T @ (F(x, model) - z) + beta * WmTWm @ model
H = jacobian.T @ jacobian + beta * WmTWm
delta = np.linalg.solve(H, -g)

alpha = backtracking(x, model, delta, jacobian)

model += delta

plt.plot(x, F(x, model) * 100 * 1000)
# plt.plot(x, z * 100 * 1000) #F(x, model))
# plt.plot(model_locations, F(model_locations, model) * 100 * 1000)
plt.show()

# beta = 1e-4
# jacobian = J(x, model)
# g = jacobian.T @ (F(x, model) - z) + beta * WmTWm @ model
# H = jacobian.T @ jacobian + beta * WmTWm
# 
# delta = np.linalg.solve(H, -g)
# 
# model += delta
# print(delta)
# 
# jacobian = J(x, model)
# g = jacobian.T @ (F(x, model) - z) + beta * WmTWm @ model
# H = jacobian.T @ jacobian + beta * WmTWm
# delta = np.linalg.solve(H, -g)
# 
# print(delta)
