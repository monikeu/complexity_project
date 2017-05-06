import logging
import timeit
from argparse import ArgumentParser
from math import log2, sqrt

import numpy

from complexity_project.ClassNotFoundException import ClassNotFoundException


def my_import(name):
    components = name.split('.')
    mod = __import__(components[0])
    for comp in components[1:]:
        mod = getattr(mod, comp)
    if mod is None:
        raise ClassNotFoundException
    return mod


def approximate(x, y, degree):
    return numpy.polyfit(x, y, degree)


def squared_error_x(coeff, x, y):
    err = []
    for i in range(0, len(x)):
        err.append(abs(coeff[0] * x[i] + coeff[1] - y[i]))
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


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('class_or_fun', help=HELP, type=str)
    return parser.parse_args()

HELP = 'Name of your class ,'
' class must inherit from Base. '
'If you want to test function, '
'place it in Base.function method'

times_y = []
n_x = []
errs = []
coeffs = {}
complexities = ["n", "n^2", "n^3", "logn", "nlogn", "sqrt(n)"]
polyvals = {"n": "a*n + b",
            "n^2": "a*n^2 + b*n + c",
            "n^3": "a*n^3 + b*n^2 + cn + d",
            "logn": "a*logn + b",
            "nlogn": "a*nlogn +b",
            "sqrt(x)": "a*sqrt(x) + b"}

logging.basicConfig(filename="logs.txt", level=logging.DEBUG)

logging.info("Start")
args = parse_args()
logging.debug("Arguments parsed")

try:
    my_class = my_import(args.class_or_fun)
    class_object = my_class()

except ClassNotFoundException:
    logging.info("ClassNotFoundException occured")

logging.debug("Created an object of a class")

for i in range(1, 21):
    n_x.append(i*100)

logging.debug("Array with n's created successfully")

for p in range(0, len(n_x)):
    class_object.setup(n_x[p])
    timer = timeit.Timer(class_object.function)
    times_y.append(timer.timeit(number=10))
    class_object.clean_up()
    logging.debug("Measured time no. " + str(p))

logging.debug("Measurements done")

# x
coeff_temp = approximate(n_x, times_y, 1)
print(coeff_temp)
errs.append(squared_error_x(coeff_temp, n_x, times_y))
coeffs["n"] = coeff_temp
logging.debug("Calculated approximation to x")
# print(errs.append(squared_error_x(coeff, n_x, times_y)))


# x^2
coeff_temp = approximate(n_x, times_y, 2)
print(coeff_temp)
errs.append(squared_error_x2(coeff_temp, n_x, times_y))
coeffs["n^2"] = coeff_temp
logging.debug("Calculated approximation to x^2")
# print(errs.append(squared_error_x2(coeff, n_x, times_y)))


# x^3
coeff_temp = approximate(n_x, times_y, 3)
print(coeff_temp)
errs.append(squared_error_x3(coeff_temp, n_x, times_y))
coeffs["n^3"] = coeff_temp
logging.debug("Calculated approximation to x^3")


# log2x
coeff_temp = approximate(numpy.log2(n_x), times_y, 1)
print(coeff_temp)
errs.append(squared_error_logx(coeff_temp, n_x, times_y))
coeffs["logn"] = coeff_temp
logging.debug("Calculated approximation to logx")


# xlog2x
coeff_temp = approximate(n_x * numpy.log2(n_x), times_y, 1)
print(coeff_temp)
errs.append(squared_error_xlogx(coeff_temp, n_x, times_y))
coeffs["nlogn"] = coeff_temp
logging.debug("Calculated approximation to xlogx")


# sqrt(x)
coeff_temp = approximate(numpy.sqrt(n_x), times_y, 1)
print(coeff_temp)
errs.append(squared_error_sqrtx(coeff_temp, n_x, times_y))
coeffs["sqrt(x)"] = coeff_temp
logging.debug("Calculated approximation to sqrt(x)")


print("Square errors \n" + str(errs))
print("Complexities \n" + str(complexities))
print("Complexity O(" + complexities[errs.index(min(errs))] + ")")
print("Function describing time(problem size) dependency: \n" + str(polyvals[complexities[errs.index(min(errs))]]) +
      "\nit's coefficients: \n" + str(coeffs[complexities[errs.index(min(errs))]]))
# print("Coefficients :" + str(coeffs[complexities[errs.index(min(errs))]]))


logging.info("Finished")



