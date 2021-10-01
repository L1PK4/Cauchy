import numpy as np

func = lambda x, y : y + np.exp(x)
eps = 1e-6
h0 = 0.3    
x, X = 0., 1.
y = 0.

def step(x, y, h):
	ϕ0 = h * func(x, y)
	ϕ1 = h * func(x + h / 2, y + ϕ0 / 2)
	ϕ2 = h * func(x + h / 2, y + ϕ1 / 2)
	ϕ3 = h * func(x + h, y + ϕ2)
	Δy = (ϕ0 + 2 * ϕ1 + 2 * ϕ2 + ϕ3) / 6
	return y + Δy

def jump(x, y):
	global h0
	h = h0
	yh = step(x, y, h)
	while True:
		yh0 = step(x, y, h / 2)
		yh1 = step(x + h / 2, yh0, h / 2)
		if np.abs(yh - yh1) <= eps:
			return yh, h
		h /= 2
		yh = yh0



def main():
	global func, x, X, h0, eps, y
	if input("Хотите ввести свои данные? [Y/N]\n") == 'Y':
		h0 = float(input("Введите h₀: "))
		func = lambda x, y : eval(input("Введите f(x, y) = "))
		eps = float(input("Введите 𝜀: "))
		x, X = tuple(map(float, input("Введите границы : ").split()))
		y = float(input("Введите y₀ : "))

	x0 = x
	ans = []

	while X - x > eps:
		ans.append((x, y))
		y, h = jump(x, y)
		x += h
		if X - x < h0:
			h0 = X - x

	
	ans.append((X, y))
	for i, xy in enumerate(ans):
		print(f"{i:2})x: {xy[0]:6.6}\t\ty: {xy[1]:6.6}\t\terr: {(np.abs(xy[0] * np.exp(xy[0]) - xy[1])):6.6}")

	import matplotlib.pyplot as plt
	n = 1000
	testx = [x0 + i * (X - x0) / n for i in range(n)]
	testy = list(map(lambda x : x * np.exp(x), testx))
	plt.plot(*zip(*ans), 'b', label='Решение методом')
	plt.plot(testx, testy, 'r', label='Аналитическое решение')
	plt.legend(loc='best')
	plt.show()
	return 0

if __name__ == "__main__":
	main()