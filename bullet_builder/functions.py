import math


def Compose(func_a, func_b):
    return lambda x: func_a(func_b(x))


def Periodic(f, period):
    return lambda x: f(x % period)


def Piecewise(functions, conditions, fallback=lambda x: 0):
    def _f(x):
        for i, condition in enumerate(conditions):
            if condition(x):
                return functions[i](x)
        return fallback(x)
    return _f


def Transform(f, a, b, c, d):
    return lambda x: a * f(c * x + d) + b


def Polynomial(coefficients):
    def _f(x):
        result = 0
        for coefficient in coefficients:
            result = result * x + coefficient
        return result
    return _f


def Logit(base):
    return lambda x: math.log(x / (1 - x), base)


def LogitNormalDensity(mu, sigma):
    c = 1 / (sigma * math.sqrt(2 * math.pi))
    k = 2 * sigma * sigma
    return lambda x: c * 1 / (x * (1 - x)) * math.exp(-k * (math.log(x / (1 - x)) - mu) ** 2)


def Logistic(base):
    return lambda x: base ** x / (base ** x + 1)


def SineSquaredTransition(t0, t1, h0, h1):
    xi = math.pi / (2 * (t1 - t0))
    zeta = h1 - h0

    def _f(x):
        z = math.sin(xi * (x - t0))
        return zeta * z * z + h0
    return _f


def LogisticTransition(t0, t1, h0, h1, cutoff=7):
    t2 = 1 / 2 * (t0 + t1)
    a = cutoff / (t1 - t2)
    zeta = h1 + h0
    return lambda x: zeta / (math.exp(a * (t2 - x)) + 1) + h0


def SineWave(period, extremum, t0, h0):
    c = 2 * math.pi / (period)
    return lambda x: extremum * math.sin(c * (x - t0)) + h0


def SinusoidalWave(dx, dy, t0, h0):
    c = math.pi / dx
    dy /= 2
    return lambda x: dy * (-math.cos(c * (x - t0)) + 1) + h0


def AsymmetricTriangleWave(dx1, dx2, dy, t0, h0):
    m1 = dy / dx1
    m2 = -dy / dx2
    return Periodic(
        Piecewise(
            [lambda x: m1 * (x - t0) + h0, lambda x: m2 *
             (x - (t0 + dx1 + dx2)) + h0],
            [lambda x: 0 <= x - t0 < dx1,
             lambda x: dx1 <= x - t0 < dx1 + dx2]
        ),
        dx1 + dx2
    )


def TriangleWave(dx, dy, t0, h0):
    return AsymmetricTriangleWave(period / 2, period / 2, extremum, t0, h0)


def AsymmetricRectangleWave(dx1, dx2, dy, t0, h0):
    return Periodic(
        Piecewise(
            [lambda x: h0, lambda x: h0 + dy],
            [lambda x: 0 <= x - t0 < dx1,
             lambda x: dx1 <= x - t0 < dx1 + dx2]
        ),
        dx1 + dx2
    )


def RectangleWave(dx, dy, t0, h0):
    return AsymmetricRectangleWave(dx, dx, dy, t0, h0)


def SawtoothWave(dx, dy, t0, h0):
    return Periodic(lambda x: dy / dx * (x - t0) + h0, dx)


def DoOnceAt(t0):
	return Piecewise([lambda x: 1], [lambda x: x == t0])

def DoAt(points):
	return Piecewise([lambda x: 1], [lambda x: x in points])
