import numpy as np

func = 	lambda x, y : complex(y.real + y.imag + np.exp(x) * (1 - x*x), 2 * y.real + y.imag)
eps = 1e-5
h0 = 0.3    
x, X = 0., 1.
y = 0. + 0.j


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

# u'(x) = f(x, u, v)
# v'(x) = g(x, u, v)
# alpha beta A такие же

# u = xeˣ 		u' = eˣ + u + v - x²eˣ 	= u + v + eˣ(1 - x²) 
# v = x²eˣ		v' = 2xeˣ + x²eˣ 		= 2u + v
def main():
	global f, x, X, h0, eps, y
	x0 = x
	ans = []

	while X - x > 0:
		ans.append((x, y))
		y, h = jump(x, y)
		x += h
		if X - x < h0:
			h0 = X - x

	
	ans.append((x, y))
	for i, xy in enumerate(ans):
		_x, _y = xy
		print(f"{i:2})x: {xy[0]:6.6}\t\ty: {xy[1].real:6.6} {xy[1].imag:6.6}\t\terr: {(np.abs(complex(_x * np.exp(_x), _x * _x * np.exp(_x)) - xy[1])):6.6}")

	import matplotlib.pyplot as plt
	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')
	n = 1000
	testx = [x0 + i * (X - x0) / n for i in range(n)]
	testy = list(map(lambda x : x * np.exp(x), testx))
	testz = list(map(lambda x : x * x * np.exp(x), testx))
	ans = list(zip(*ans))
	plt.plot(ans[0], list(map(lambda y : y.real, ans[1])), list(map(lambda y : y.imag, ans[1])), label='Решение методом')
	ax.plot(testx, testy, testz, label='Аналитическое решение')
	plt.legend(loc='best')
	plt.show()
	return 0

if __name__ == "__main__":
	main()