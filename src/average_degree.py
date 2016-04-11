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
        # If 'created_at' field does not exist, set timestamp as 0.
        #print "KeyError for the key, created_at : timestamp will be 0."
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
    # Size of the window
    window_size = 60   
    # Creating the graph for hashtag object
    gr = TimeWindowGraph(window_size=window_size)
    time_threshold = gr.current_time - window_size

    with open(input_filename, 'r') as f_in: # Opening input file to get tweets
        with open(output_filename, 'w') as f_out: # Opening output file
            for line in f_in: # For every tweet
                json_data = json.loads(line) # dict representing tweet

                # Checking for control data (if there is less than 3 fields).
                # In those cases, we will skip the data.
                if len(json_data) < 3:
                    continue

                # Extract timestamp (int) and a list of hashtags (str, case
                # sensitive)
                (timestamp, hashtags) = extract_data(json_data)

                # Check the timestamp first.
                if timestamp <= time_threshold: # too old for our graph.
                    continue # do nothing for this tweet.
                elif timestamp > gr.current_time: # becomes the most recent tweet.
                    # Set current_time for the graph
                    # (it will remove old links older than threshold also)
                    gr.set_current_time(timestamp)

                # New links (for all possible pairs of hashtags) are added here.
                num_hashtags = len(hashtags)
                for i in range(num_hashtags):
                    for j in range(i+1, num_hashtags):

                        # First, check for duplicate hashtags
                        if hashtags[i] == hashtags[j]:
                            continue

                        # Second, try to add both nodes (this method will do nothing
                        # if the given node already exists)
                        gr.add_node(hashtags[i])
                        gr.add_node(hashtags[j])

                        # Third, (1) try to find if the link already exists;
                        # and (2) if so, what the timestamp of that link is.
                        # Here timestamp (epoch time) is a non-negative
                        # integer, so -1 indicates there is no link.
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
