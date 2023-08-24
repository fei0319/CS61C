from unittest import TestCase
from framework import AssemblyTest, print_coverage


class TestAbs(TestCase):
    def test_zero(self):
        t = AssemblyTest(self, "abs.s")
        # load 0 into register a0
        t.input_scalar("a0", 0)
        # call the abs function
        t.call("abs")
        # check that after calling abs, a0 is equal to 0 (abs(0) = 0)
        t.check_scalar("a0", 0)
        # generate the `assembly/TestAbs_test_zero.s` file and run it through venus
        t.execute()

    def test_one(self):
        # same as test_zero, but with input 1
        t = AssemblyTest(self, "abs.s")
        t.input_scalar("a0", 1)
        t.call("abs")
        t.check_scalar("a0", 1)
        t.execute()
        
    def test_minus_one(self):
        # Indicates we are creating the test for the `abs.s` file
        t = AssemblyTest(self, "abs.s")
        # Setting the argument register a0 to have value of -1
        t.input_scalar("a0", -1)
        # Calling the abs function
        t.call("abs")
        # The a0 register is now the return value
        # Checking if a0 is now 1
        t.check_scalar("a0", 1)
        t.execute()

    def test_114514(self):
        t = AssemblyTest(self, "abs.s")
        t.input_scalar("a0", -114514)
        t.call("abs")
        t.check_scalar("a0", 114514)
        t.execute()
    
    def test_1919810(self):
        t = AssemblyTest(self, "abs.s")
        t.input_scalar("a0", 1919810)
        t.call("abs")
        t.check_scalar("a0", 1919810)
        t.execute()

    @classmethod
    def tearDownClass(cls):
        print_coverage("abs.s", verbose=False)


class TestRelu(TestCase):
    def test_simple(self):
        t = AssemblyTest(self, "relu.s")
        # create an array in the data section
        array0 = t.array([1, -2, 3, -4, 5, -6, 7, -8, 9])
        # load address of `array0` into register a0
        t.input_array("a0", array0)
        # set a1 to the length of our array
        t.input_scalar("a1", len(array0))
        # call the relu function
        t.call("relu")
        # check that the array0 was changed appropriately
        t.check_array(array0, [1, 0, 3, 0, 5, 0, 7, 0, 9])
        # generate the `assembly/TestRelu_test_simple.s` file and run it through venus
        t.execute()
    
    def test_random(self):
        from random import randint
        t = AssemblyTest(self, "relu.s")
        
        original_arr = [randint(-2**31, 2**31-1) for _ in range(randint(10, 20))]
        arr = t.array(original_arr)
        t.input_array("a0", arr)
        t.input_scalar("a1", len(arr))
        t.call("relu")
        t.check_array(arr, [max(x, 0) for x in original_arr])

        t.execute()
    
    def test_multiple(self):
        for _ in range(10):
            self.test_random()

    def test_error(self):
        from random import randint
        t = AssemblyTest(self, "relu.s")
        
        original_arr = [randint(-2**31, 2**31-1) for _ in range(randint(10, 20))]
        arr = t.array(original_arr)
        t.input_array("a0", arr)
        t.input_scalar("a1", 0)
        t.call("relu")

        t.execute(code=32)

    @classmethod
    def tearDownClass(cls):
        print_coverage("relu.s", verbose=False)


class TestArgmax(TestCase):
    def test_simple(self):
        t = AssemblyTest(self, "argmax.s")
        # create an array in the data section
        original_arr = [1, 1, 4, 5, 1, 4]
        arr = t.array(original_arr)
        # load address of the array into register a0
        t.input_array("a0", arr)
        # set a1 to the length of the array
        t.input_scalar("a1", len(arr))
        # call the `argmax` function
        t.call("argmax")
        # check that the register a0 contains the correct output
        t.check_scalar("a0", max(range(len(arr)), key=lambda x: original_arr[x]))
        # generate the `assembly/TestArgmax_test_simple.s` file and run it through venus
        t.execute()

    def test_random(self):
        t = AssemblyTest(self, "argmax.s")
        from random import randint
        original_arr = [randint(-5, 5) for _ in range(randint(20, 100))]
        arr = t.array(original_arr)
        t.input_array("a0", arr)
        t.input_scalar("a1", len(arr))
        t.call("argmax")
        t.check_scalar("a0", max(range(len(arr)), key=lambda x: original_arr[x]))
        t.execute()
    
    def test_multiple(self):
        for _ in range(15):
            self.test_random()
    
    def test_error(self):
        t = AssemblyTest(self, "argmax.s")
        arr = t.array([1, 1, 4, 5, 1, 4])
        t.input_array("a0", arr)
        t.input_scalar("a1", 0)
        t.call("argmax")
        t.execute(code=32)

    @classmethod
    def tearDownClass(cls):
        print_coverage("argmax.s", verbose=False)


class TestDot(TestCase):
    @classmethod
    def dot(cls, v0, v1, n, s0, s1):
        i0, i1 = 0, 0
        res = 0
        for i in range(n):
            res += v0[i0] * v1[i1]
            i0 += s0
            i1 += s1
        return res

    def random_test(self, length, s0, s1, code=0):
        from random import randint
        t = AssemblyTest(self, "dot.s")

        v0 = [randint(1, 100) for _ in range(length * s0 + 10)]
        v1 = [randint(1, 100) for _ in range(length * s1 + 10)]

        t.input_array("a0", t.array(v0))
        t.input_array("a1", t.array(v1))
        t.input_scalar("a2", length)
        t.input_scalar("a3", s0)
        t.input_scalar("a4", s1)

        t.call("dot")

        t.check_scalar("a0", self.dot(v0, v1, length, s0, s1))
        t.execute(code=code)

    def test_simple(self):
        self.random_test(30, 1, 1)
    
    def test_stride(self):
        from random import randint
        self.random_test(randint(5, 60), randint(1, 5), randint(1, 5))
    
    def test_multiple(self):
        for _ in range(20):
            self.test_simple()
        for _ in range(5):
            self.test_stride()
    
    def test_error32(self):
        self.random_test(0, 1, 1, 32)
        self.random_test(30, 1, 0, 33)

    @classmethod
    def tearDownClass(cls):
        print_coverage("dot.s", verbose=False)


class TestMatmul(TestCase):

    def do_matmul(self, m0, m0_rows, m0_cols, m1, m1_rows, m1_cols, result, code=0):
        t = AssemblyTest(self, "matmul.s")
        # we need to include (aka import) the dot.s file since it is used by matmul.s
        t.include("dot.s")

        # create arrays for the arguments and to store the result
        array0 = t.array(m0)
        array1 = t.array(m1)
        array_out = t.array([0] * len(result))

        # load address of input matrices and set their dimensions
        t.input_array("a0", array0)
        t.input_scalar("a1", m0_rows)
        t.input_scalar("a2", m0_cols)

        t.input_array("a3", array1)
        t.input_scalar("a4", m1_rows)
        t.input_scalar("a5", m1_cols)

        t.input_array("a6", array_out)

        # call the matmul function
        t.call("matmul")

        # check the content of the output array
        t.check_array(array_out, result)

        # generate the assembly file and run it through venus, we expect the simulation to exit with code `code`
        t.execute(code=code)

    def test_simple(self):
        self.do_matmul(
            [1, 2, 3, 4, 5, 6, 7, 8, 9], 3, 3,
            [1, 2, 3, 4, 5, 6, 7, 8, 9], 3, 3,
            [30, 36, 42, 66, 81, 96, 102, 126, 150]
        )
    
    def test_random(self):
        from random import randint
        from numpy import array as matrix

        n, m, k = (randint(3, 20) for _ in range(3))
        a = matrix([randint(0, 10) for _ in range(n * k)]).reshape(n, k)
        b = matrix([randint(0, 10) for _ in range(k * m)]).reshape(k, m)
        result = a.dot(b)

        self.do_matmul(
            list(a.reshape(n * k)), n, k,
            list(b.reshape(k * m)), k, m,
            list(result.reshape(n * m))
        )

    def test_multiple(self):
        for _ in range(20):
            self.test_random()

    def test_error(self):
        self.do_matmul(
            [5, 6, 3], 1, 3,
            [3, 9, 0], 4, 1,
            [3],
            code=34
        )
        self.do_matmul(
            [1], 0, 4,
            [2], 4, 5,
            [3],
            code=34
        )

    @classmethod
    def tearDownClass(cls):
        print_coverage("matmul.s", verbose=False)


class TestReadMatrix(TestCase):

    def do_read_matrix(self, file_name, fail='', code=0):
        t = AssemblyTest(self, "read_matrix.s")
        # load address to the name of the input file into register a0
        t.input_read_filename("a0", file_name + '.bin')

        # allocate space to hold the rows and cols output parameters
        rows = t.array([-1])
        cols = t.array([-1])

        # load the addresses to the output parameters into the argument registers
        t.input_array("a1", rows)
        t.input_array("a2", cols)

        # call the read_matrix function
        t.call("read_matrix")

        # check the output from the function
        with open(f'../{file_name}.txt', 'r') as f:
            arr = list(map(int, f.read().split()))
            n = arr[0]
            m = arr[1]
            arr = arr[2:]

        t.check_array(rows, [n])
        t.check_array(cols, [m])
        t.check_array_pointer("a0", arr)

        # generate assembly and run it through venus
        t.execute(fail=fail, code=code)

    def test_simple(self):
        self.do_read_matrix(file_name="inputs/test_read_matrix/test_input")

    def test_error(self):
        self.do_read_matrix(file_name="inputs/test_read_matrix/test_input", fail="malloc", code=48)
        self.do_read_matrix(file_name="inputs/test_read_matrix/test_input", fail="fopen", code=64)
        self.do_read_matrix(file_name="inputs/test_read_matrix/test_input", fail="fread", code=66)
        self.do_read_matrix(file_name="inputs/test_read_matrix/test_input", fail="fclose", code=65)

    @classmethod
    def tearDownClass(cls):
        print_coverage("read_matrix.s", verbose=False)


class TestWriteMatrix(TestCase):

    def do_write_matrix(self, fail='', code=0):
        t = AssemblyTest(self, "write_matrix.s")
        outfile = "outputs/test_write_matrix/student.bin"
        # load output file name into a0 register
        t.input_write_filename("a0", outfile)
        # load input array and other arguments
        t.input_array("a1", t.array([1, 2, 3, 4, 5, 6]))
        t.input_scalar("a2", 2)
        t.input_scalar("a3", 3)
        # call `write_matrix` function
        t.call("write_matrix")
        # generate assembly and run it through venus
        t.execute(fail=fail, code=code)
        # compare the output file against the reference
        if code == 0:
            t.check_file_output(outfile, "outputs/test_write_matrix/reference.bin")

    def test_simple(self):
        self.do_write_matrix()

    def test_error(self):
        self.do_write_matrix("fopen", 64)
        self.do_write_matrix("fwrite", 67)
        self.do_write_matrix("fclose", 65)

    @classmethod
    def tearDownClass(cls):
        print_coverage("write_matrix.s", verbose=False)


class TestClassify(TestCase):

    def make_test(self):
        t = AssemblyTest(self, "classify.s")
        t.include("argmax.s")
        t.include("dot.s")
        t.include("matmul.s")
        t.include("read_matrix.s")
        t.include("relu.s")
        t.include("write_matrix.s")
        return t

    def base_test(self, fail='', code=0, extra_arg=False):
        t = self.make_test()
        out_file = "outputs/test_basic_main/student0.bin"
        ref_file = "outputs/test_basic_main/reference0.bin"
        args = ["inputs/simple0/bin/m0.bin", "inputs/simple0/bin/m1.bin",
                "inputs/simple0/bin/inputs/input0.bin", out_file]
        if extra_arg:
            args.append("loremipsum")
        # call classify function
        t.call("classify")
        # generate assembly and pass program arguments directly to venus
        t.execute(args=args, fail=fail, code=code)

        if code == 0:
            # compare the output file and reference file
            t.check_file_output(out_file, ref_file)

            # compare the classification output with `check_stdout`
            t.check_stdout("2")

    def test_simple0_input0(self):
        self.base_test()

    def test_error(self):
        self.base_test(fail="malloc", code=48)
        self.base_test(extra_arg=True, code=35)

    @classmethod
    def tearDownClass(cls):
        print_coverage("classify.s", verbose=False)


# The following are some simple sanity checks:
import subprocess, pathlib, os
script_dir = pathlib.Path(os.path.dirname(__file__)).resolve()

def compare_files(test, actual, expected):
    assert os.path.isfile(expected), f"Reference file {expected} does not exist!"
    test.assertTrue(os.path.isfile(actual), f"It seems like the program never created the output file {actual}!")
    # open and compare the files
    with open(actual, 'rb') as a:
        actual_bin = a.read()
    with open(expected, 'rb') as e:
        expected_bin = e.read()
    test.assertEqual(actual_bin, expected_bin, f"Bytes of {actual} and {expected} did not match!")

import utils

class TestMain(TestCase):
    """ This sanity check executes src/main.S using venus and verifies the stdout and the file that is generated.
    """

    def run_main(self, inputs, output_id, label):
        args = [f"{inputs}/m0.bin", f"{inputs}/m1.bin",
                f"{inputs}/inputs/input0.bin",
                f"outputs/test_basic_main/student{output_id}.bin"]
        reference = f"outputs/test_basic_main/reference{output_id}.bin"

        t= AssemblyTest(self, "main.s", no_utils=True)
        t.call("main")
        t.execute(args=args)
        t.check_stdout(label)
        t.check_file_output(args[-1], reference)

    def run_test(self, inputs, output_id):
        args = [f"{inputs}/m0.bin", f"{inputs}/m1.bin",
                f"{inputs}/inputs/input0.bin",
                f"outputs/test_basic_main/student{output_id}.bin"]
        reference = f"outputs/test_basic_main/reference{output_id}.bin"

        from random import randint
        n, m, a, b = (randint(1, 10) for _ in range(4))
        m1 = utils.randmat(n, a)
        m0 = utils.randmat(a, b)
        inp = utils.randmat(b, m)

        score = m0.dot(inp)
        utils.relu(score)
        score = m1.dot(score)

        utils.write_matrix(args[0], m0)
        utils.write_matrix(args[1], m1)
        utils.write_matrix(args[2], inp)
        utils.write_matrix(reference, score)
        score.shape = n*m
        label = str(max(range(n*m), key=lambda x:score[x]))

        t= AssemblyTest(self, "main.s", no_utils=True)
        t.call("main")
        t.execute(args=args)
        t.check_stdout(label)
        t.check_file_output(args[-1], reference)

    def test0(self):
        self.run_main("inputs/simple0/bin", "0", "2")

    def test1(self):
        self.run_main("inputs/simple1/bin", "1", "1")

    def test2(self):
        self.run_test("inputs/custom0/bin", "2")

    def test3(self):
        self.run_test("inputs/custom1/bin", "3")

    def test4(self):
        self.run_test("inputs/custom2/bin", "4")
