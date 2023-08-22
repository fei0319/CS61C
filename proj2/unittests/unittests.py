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
        t.check_scalar("a0", 32)

        t.execute()

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
        t.check_scalar("a0", 32)
        t.execute()

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

    def test_simple(self):
        from random import randint
        t = AssemblyTest(self, "dot.s")

        length = 30
        v0 = [randint(1, 100) for _ in range(length)]
        v1 = [randint(1, 100) for _ in range(length)]
        s0, s1 = 1, 1

        t.input_array("a0", t.array(v0))
        t.input_array("a1", t.array(v1))
        t.input_scalar("a2", length)
        t.input_scalar("a3", s0)
        t.input_scalar("a4", s1)

        t.call("dot")

        t.check_scalar("a0", self.dot(v0, v1, length, s0, s1))
        t.execute()
    
    def test_stride(self):
        from random import randint
        t = AssemblyTest(self, "dot.s")

        s0, s1 = randint(1, 5), randint(1, 5)
        length = randint(10, 25)
        size = max(s0, s1) * length
        v0 = [randint(1, 100) for _ in range(size)]
        v1 = [randint(1, 100) for _ in range(size)]

        t.input_array("a0", t.array(v0))
        t.input_array("a1", t.array(v1))
        t.input_scalar("a2", length)
        t.input_scalar("a3", s0)
        t.input_scalar("a4", s1)

        t.call("dot")

        t.check_scalar("a0", self.dot(v0, v1, length, s0, s1))
        t.execute()
    
    def test_multiple(self):
        for _ in range(20):
            self.test_simple()
        for _ in range(10):
            self.test_stride()
    
    def test_error32(self):
        from random import randint
        t = AssemblyTest(self, "dot.s")

        s0, s1 = randint(1, 5), randint(1, 5)
        length = 0
        size = max(s0, s1) * length
        v0 = [randint(1, 100) for _ in range(size)]
        v1 = [randint(1, 100) for _ in range(size)]

        t.input_array("a0", t.array(v0))
        t.input_array("a1", t.array(v1))
        t.input_scalar("a2", length)
        t.input_scalar("a3", s0)
        t.input_scalar("a4", s1)

        t.call("dot")
        t.check_scalar("a0", 32)
        t.execute()
    
    def test_error33(self):
        from random import randint
        t = AssemblyTest(self, "dot.s")

        s0, s1 = randint(1, 5), 0
        length = 10
        size = max(s0, s1) * length
        v0 = [randint(1, 100) for _ in range(size)]
        v1 = [randint(1, 100) for _ in range(size)]

        t.input_array("a0", t.array(v0))
        t.input_array("a1", t.array(v1))
        t.input_scalar("a2", length)
        t.input_scalar("a3", s0)
        t.input_scalar("a4", s1)

        t.call("dot")
        t.check_scalar("a0", 33)
        t.execute()

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
        raise NotImplementedError("TODO")
        # TODO
        # load address of output array
        # TODO

        # call the matmul function
        t.call("matmul")

        # check the content of the output array
        # TODO

        # generate the assembly file and run it through venus, we expect the simulation to exit with code `code`
        t.execute(code=code)

    def test_simple(self):
        self.do_matmul(
            [1, 2, 3, 4, 5, 6, 7, 8, 9], 3, 3,
            [1, 2, 3, 4, 5, 6, 7, 8, 9], 3, 3,
            [30, 36, 42, 66, 81, 96, 102, 126, 150]
        )

    @classmethod
    def tearDownClass(cls):
        print_coverage("matmul.s", verbose=False)


class TestReadMatrix(TestCase):

    def do_read_matrix(self, fail='', code=0):
        t = AssemblyTest(self, "read_matrix.s")
        # load address to the name of the input file into register a0
        t.input_read_filename("a0", "inputs/test_read_matrix/test_input.bin")

        # allocate space to hold the rows and cols output parameters
        rows = t.array([-1])
        cols = t.array([-1])

        # load the addresses to the output parameters into the argument registers
        raise NotImplementedError("TODO")
        # TODO

        # call the read_matrix function
        t.call("read_matrix")

        # check the output from the function
        # TODO

        # generate assembly and run it through venus
        t.execute(fail=fail, code=code)

    def test_simple(self):
        self.do_read_matrix()

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
        raise NotImplementedError("TODO")
        # TODO
        # call `write_matrix` function
        t.call("write_matrix")
        # generate assembly and run it through venus
        t.execute(fail=fail, code=code)
        # compare the output file against the reference
        t.check_file_output(outfile, "outputs/test_write_matrix/reference.bin")

    def test_simple(self):
        self.do_write_matrix()

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

    def test_simple0_input0(self):
        t = self.make_test()
        out_file = "outputs/test_basic_main/student0.bin"
        ref_file = "outputs/test_basic_main/reference0.bin"
        args = ["inputs/simple0/bin/m0.bin", "inputs/simple0/bin/m1.bin",
                "inputs/simple0/bin/inputs/input0.bin", out_file]
        # call classify function
        t.call("classify")
        # generate assembly and pass program arguments directly to venus
        t.execute(args=args)

        # compare the output file and
        raise NotImplementedError("TODO")
        # TODO
        # compare the classification output with `check_stdout`

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

    def test0(self):
        self.run_main("inputs/simple0/bin", "0", "2")

    def test1(self):
        self.run_main("inputs/simple1/bin", "1", "1")
