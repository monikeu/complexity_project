import sys
import logging
import timeit
from argparse import ArgumentParser
from math import log2
import numpy
import time


class ClassNotFoundException(Exception):

    def __init__(self, message):
        super().__init__(message)


def import_class(name):
    try:
        components = name.split('.')
        mod = __import__(components[0])
        for comp in components[1:]:
            mod = getattr(mod, comp)

    except(ImportError, AttributeError):
        raise ClassNotFoundException("Class not found")

    return mod


def approximate(x, y, degree):
    return numpy.polyfit(x, y, degree)


def fun_x(x):
    return x


def fun_x2(x):
    return x**2


def fun_x3(x):
    return x**3


def fun_xlogx(x):
    return x * log2(x)


def fun_logx(x):
    return log2(x)


def fun_const(x):
    return 1


def absolute_error(fun, coeff, x, y):
    err = []
    if len(coeff) > 1:
        for i in range(0, len(x)):
            err.append(abs(coeff[0] * fun(x[i]) + coeff[1] - y[i]))
    else:
        for i in range(0, len(x)):
            err.append(abs(coeff[0] * fun(x[i]) - y[i]))
    return numpy.average(err)


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('class_or_fun', help=HELP, type=str)
    return parser.parse_args()

LIMIT_MES = "Calculation time bigger than 30 seconds " \
            "Result of calculation will be less accurate"

HELP = 'Name of your class ,' \
       ' class must inherit from Base. ' \
       'If you want to test function, ' \
       'place it in Base.function'

times_y = []
n_x = []
errs = []
coeffs = {}
complexities = [
                "n",
                "n^2",
                "n^3",
                "logn",
                "nlogn",
                "sqrt(n)"
]

functions = {
            "n": "a*n + b",
            "n^2": "a*n^2 + +b",
            "n^3": "a*n^3 + b",
            "logn": "a*logn + b",
            "nlogn": "a*nlogn +b",
            "const": "inf"
}

rev_functions = {
            "n": "x = (y - b)/a",
            "n^2": "x = (y - b)/a)^(1/2)",
            "n^3": "x = (y - b)/a ^(1/3)",
            "logn": "2^((y - b)/a)",
            "nlogn": "reverse does not exist",
            "const": "inf"
}

logging.basicConfig(filename="logs.txt", level=logging.DEBUG, filemode='w')

logging.info("Start")
args = parse_args()
logging.debug("Arguments parsed")

try:
    my_class = import_class(args.class_or_fun)
    class_object = my_class()

except ClassNotFoundException:
    print("Class not found")
    logging.info("Class not found")
    sys.exit()

logging.debug("Created an object of a class")

for i in range(1, 300):
    n_x.append(i*25)

logging.debug("Array with n's created successfully")

for p in range(0, len(n_x)):

    class_object.setup(n_x[p])
    timer = timeit.Timer(class_object.function)
    times_y.append(timer.timeit(number=10))
    class_object.clean_up()
    logging.debug("Measured time no. " + str(p))

    if time.process_time() > 30.0:

        print(LIMIT_MES)
        n_x = n_x[:len(times_y)]
        break


logging.debug("Measurements done")

# x
coeff_temp = approximate(n_x, times_y, 1)
errs.append(absolute_error(fun_x, coeff_temp, n_x, times_y))
coeffs["n"] = coeff_temp
logging.debug("Calculated approximation to x")

# x^2
coeff_temp = approximate(numpy.power(n_x, 2), times_y, 1)
errs.append(absolute_error(fun_x2, coeff_temp, n_x, times_y))
coeffs["n^2"] = coeff_temp
logging.debug("Calculated approximation to x^2")

# x^3
coeff_temp = approximate(numpy.power(n_x, 3), times_y, 1)
errs.append(absolute_error(fun_x3, coeff_temp, n_x, times_y))
coeffs["n^3"] = coeff_temp
logging.debug("Calculated approximation to x^3")

# log2x
coeff_temp = approximate(numpy.log2(n_x), times_y, 1)
errs.append(absolute_error(fun_logx, coeff_temp, n_x, times_y))
coeffs["logn"] = coeff_temp
logging.debug("Calculated approximation to logx")

# xlog2x
coeff_temp = approximate(n_x * numpy.log2(n_x), times_y, 1)
errs.append(absolute_error(fun_xlogx, coeff_temp, n_x, times_y))
coeffs["nlogn"] = coeff_temp
logging.debug("Calculated approximation to xlogx")

# const
coeff_temp = approximate(n_x, times_y, 0)
errs.append(absolute_error(fun_const, coeff_temp, n_x, times_y))
coeffs["const"] = coeff_temp
logging.debug("Calculated approximation to const")


# print("Square errors \n" + str(errs))
# print("Complexities \n" + str(complexities))
print("Complexity O(" + complexities[errs.index(min(errs))] + ")")
print("Function describing time(problem size) dependency: \n" +
      str(functions[complexities[errs.index(min(errs))]]) +
      "\nit's coefficients: \n" +
      str(coeffs[complexities[errs.index(min(errs))]]))
print("Function describing problem size(time) dependency: \n" +
      str(rev_functions[complexities[errs.index(min(errs))]]) +
      "\nit's coefficients: \n" +
      str(coeffs[complexities[errs.index(min(errs))]]))

logging.info("Finished")
