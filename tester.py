import glob
import subprocess


def main():
    # tests_answer = glob.glob("tests/semantic/*_error.txt")
    tests_path = glob.glob("tests/semantic/*.cl")
    tests_answer = [x[:-3]+'_error.txt' for x in tests_path]

    tests_expected = []
    for t in tests_answer:
        with open(t) as file:
            tests_expected.append(file.readlines()[0][:-1])

    tests_obtained = []
    for t in tests_path:
        process = subprocess.Popen(['python', 'src/compiler.py', t],
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        answer, error = process.communicate()
        tests_obtained.append(answer.decode('utf-8')[:-1])

    for i in range(0, len(tests_obtained)):
        obtained = tests_obtained[i]
        expected = tests_expected[i]
        if obtained[:9] != expected[:9] and obtained[10:] == expected[10:]:
            print([tests_path[i], expected[:9], obtained[:9]])
            continue
        if obtained != expected:
            print([tests_path[i], expected, obtained])


if __name__ == '__main__':
    main()
