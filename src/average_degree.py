# Python codes to run this average degree problem.

import sys
import json
import time

from graph import TimeWindowGraph

def extract_data(json_data):
    """
    To extract timestamp (from 'created_at') and a list of hashtags for each tweet.
    Input:
        json_data (dict): name of the file
    Output:
        timestamp (int): timestamp for the tweet
        hashtags (list of str): a list of hashtags (sorted)
    """
    try:
        str_time = json_data['created_at']
        timestamp = int(time.mktime(time.strptime(str_time, \
                    "%a %b %d %H:%M:%S +0000 %Y")) + 0.5)
                # 0.5 is added to make sure it has the correct integer value.
    except KeyError:
        # If there is not created_at field, set timestamp as 0.
        print "KeyError for the key, created_at : timestamp will be 0."
        timestamp = 0

    try:
        hashtags = sorted([data['text'] for data in
                                json_data['entities']['hashtags']])
    except KeyError as key:
        # If there is no hashtag-related field, there is no hashtag for this tweet
        print "KeyError for the key,", key, ": no hashtag will be used."
        hashtags = []

    return timestamp, hashtags

def main(input_filename, output_filename):
    """
    Main function to run the program
    """
    window_size = 60    # Size of the window
    # Creating the graph for hashtag object
    gr = TimeWindowGraph(window_size=window_size)
    current_time = gr.get_current_time() # current time initialized at 0.
    time_threshold = current_time - window_size

    with open(input_filename, 'r') as f_in: # Opening input file to get tweets
        with open(output_filename, 'w') as f_out: # Opening output file
            for line in f_in:
                json_data = json.loads(line) # dict
                # extract timestamp (int) and a list of hashtags (str, case
                # sensitive)
                (timestamp, hashtags) = extract_data(json_data)

                print timestamp, hashtags

                # Check the timestamp first.
                if timestamp < time_threshold: # too old for our graph.
                    break # do nothing here.
                elif timestamp > current_time: # becomes the most recent tweet.
                    # Set time variables
                    current_time = timestamp
                    gr.set_current_time(timestamp)
                    # Remove old links older than 60-second window
                    gr.remove_old_links()

                # New links are added here.
                num_hashtags = len(hashtags)
                for i in range(num_hashtags):
                    for j in range(i+1, num_hashtags):
                        print hashtags[i], hashtags[j]
                        gr.add_nodes(hashtags[i], hashtags[j])
                        timestamp_link = gr.check_link(hashtags[i], hashtags[j])
                        if timestamp_link < 0: # No link exists.
                            gr.add_link(hashtags[i], hashtags[j], timestamp)
                        elif timestamp_link < timestamp: # old link exists.
                            gr.update_link(hashtags[i], hashtags[j], timestamp)

                # Now writes the degree information to the output file
                f_out.write("%.2f\n"% gr.average_degree())






if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "Usage: python src/average_degree.py", \
            "./tweet_input/tweets.txt ./tweet_output/output.txt"
        sys.exit()
    main(sys.argv[1], sys.argv[2])
