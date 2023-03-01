import requests
import json
import argparse
import sys
import time

# Promethes query examples:
#   rate(container_cpu_usage_seconds_total[1m])
#   container_memory_usage_bytes
#   container_working_set_in_bytes

def getQueryOutput(url, query, start, end):
    return requests.get(url + "/api/v1/query_range", { "query": query, "start": start, "end": end, "step": 15 }).json()

def main():
    parser = argparse.ArgumentParser(description="Get prometheus timeseries data.")
    parser.add_argument("url", help="url for accessing prometheus")
    parser.add_argument("-q", "--query", required=True, help="the prometheus query")
    parser.add_argument("-d", "--duration", type=int, default=60, help="the duration in seconds which ends in the time the program was run")
    # TODO implement csv
    parser.add_argument("-c", "--csv", help="output csv file, otherwise print out json data")
    args = parser.parse_args(sys.argv[1:])

    currentTime = time.time()
    queryOutput = getQueryOutput(args.url, args.query, currentTime - args.duration, currentTime)
    print(json.dumps(queryOutput, indent=2))

if __name__ == "__main__":
    main()