import logging
import timeit
from math import log2, sqrt

import numpy

from complexity_project.main import return_base


def approximate(x, y, degree):
    return numpy.polyfit(x, y, degree)


def squared_error_x(coeff, x, y):
    err = []
    for i in range(0, len(x)):
        err.append(abs(coeff[0] * x[i] + coeff[1] - y[i])) #y = ax+b
        return numpy.average(err)


def squared_error_x2(coeff, x, y):
    err = []
    for i in range(0, len(x)):
        err.append(abs(coeff[0] * (x[i]**2) + coeff[1] * x[i] + coeff[2] - y[i]))
        return numpy.average(err)


def squared_error_x3(coeff, x, y):
    err = []
    for i in range(0, len(x)):
        err.append(abs(coeff[0] * (x[i]**3) + coeff[1] * (x[i]**2) + coeff[2] * x[i] + coeff[3] - y[i]))
        return numpy.average(err)


def squared_error_logx(coeff, x, y):
    err = []
    for i in range(0, len(x)):
        err.append(abs(coeff[0] * log2(x[i]) + coeff[1] - y[i]))
        return numpy.average(err)


def squared_error_xlogx(coeff, x, y):
    err = []
    for i in range(0, len(x)):
        err.append(abs(coeff[0] * log2(x[i]) * x[i] + coeff[1] - y[i]))
        return numpy.average(err)


def squared_error_sqrtx(coeff, x, y):
    err = []
    for i in range(0, len(x)):
        err.append(abs(coeff[0] * sqrt(x[i]) + coeff[1] - y[i]))
        return numpy.average(err)

logging.basicConfig(filename="logs.txt", level=logging.DEBUG)
logging.info("Start")
times_y = []
n_x = []
class_object = return_base()

for i in range(1, 21):
    n_x.append(i*25)

logging.debug("Array with n's created successfully")

for p in range(0, len(n_x)):
    class_object.setup(n_x[p])
    timer = timeit.Timer(class_object.function)
    times_y.append(timer.timeit(number=10))
    class_object.clean_up()
    logging.debug("Measured time no. " + str(p))
    # print(times_y[p])
    # timer = timeit.Timer(stmt="infun(" + str(n_x[p]) + ")", setup="from __main__ import infun")
    # times_y.append(timer.timeit(number=1))
    # # times_y.append(timeit.timeit(stmt="infun(" + str(n_x[p]) + ")", setup="from __main__ import infun", number=1))
    # logging.debug("Measured time no. " + str(p))
    # print(times_y[p])

# x
errs = []
complexities = ["n", "n^2", "n^3", "logn", "nlogn", "sqrt(n)"]
coeffs ={}


#x
coeff = approximate(n_x, times_y, 1)
print(coeff)
errs.append(squared_error_x(coeff, n_x, times_y))
coeffs["n"] = coeff
logging.debug("Calculated approximation to x")
# print(errs.append(squared_error_x(coeff, n_x, times_y)))

#x^2
coeff = approximate(n_x, times_y, 2)
print(coeff)
errs.append(squared_error_x2(coeff, n_x, times_y))
coeffs["n^2"] = coeff
logging.debug("Calculated approximation to x^2")
# print(errs.append(squared_error_x2(coeff, n_x, times_y)))

#x^3
coeff = approximate(n_x, times_y, 3)
print(coeff)
errs.append(squared_error_x3(coeff, n_x, times_y))
coeffs["n^3"] = coeff
logging.debug("Calculated approximation to x^3")


#log2x
coeff = approximate(numpy.log2(n_x), times_y, 1)
print(coeff)
errs.append(squared_error_logx(coeff, n_x, times_y))
coeffs["logn"] = coeff
logging.debug("Calculated approximation to logx")


#xlog2x
coeff = approximate(n_x*numpy.log2(n_x), times_y, 1)
print(coeff)
errs.append(squared_error_xlogx(coeff, n_x, times_y))
coeffs["nlogn"] = coeff
logging.debug("Calculated approximation to xlogx")

#sqrt(x)
coeff = approximate(numpy.sqrt(n_x), times_y, 1)
print(coeff)
errs.append(squared_error_sqrtx(coeff, n_x, times_y))
coeffs["sqrt(x)"] = coeff
logging.debug("Calculated approximation to sqrt(x)")


print("Square errors \n" + str(errs))
print("Complexities \n" + str(complexities))
print("Complexity O(" + complexities[errs.index(min(errs))] + ")")
print("Coefficients :" + str(coeffs[complexities[errs.index(min(errs))]]))

logging.info("Finished")


