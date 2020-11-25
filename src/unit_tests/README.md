# Additional tests for our compiler

These tests were created (some were added from [this](https://github.com/ivangalbans/CoolCompiler/tree/master/TestCases) and [this](https://github.com/afterthat97/cool-compiler/tree/master/examples) repositories) to further test our compiler and are meant to be executed using `pytest`.

The only one of these tests that requires an external program is `codegen_test.py`. It requires a reference compiler to test its output vs our output. We used [this reference compiler](https://github.com/afterthat97/cool-compiler).

To run these tests on your own machine change `PATH_PREFIX` variable at `/src/unit_tests/cmp.sh` script to the correct location on your PC.