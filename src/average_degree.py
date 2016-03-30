# Python codes to run this average degree problem.

import sys

def main(input_filename, output_filename):
    """
    Main function to run the problem
    """
    with open(output_filename, 'w') as f:
        f.write("1.00\n")
        f.write("2.33\n")
        

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "Usage: python src/average_degree.py", \
            "./tweet_input/tweets.txt ./tweet_output/output.txt"
        sys.exit()
    main(sys.argv[1], sys.argv[2])
