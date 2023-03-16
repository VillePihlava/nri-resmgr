import requests
import argparse
import sys
import time
import datetime

def createCsvFromResult(metric, values, start, end):
    result = "start,{}\nend,{}\n".format(datetime.datetime.utcfromtimestamp(start), datetime.datetime.utcfromtimestamp(end))
    result += "\n{},{}\n".format("field", "value")
    for key in metric:
        result += "{},{}\n".format(key, metric[key])

    result += "\n{},{}\n".format("time", "value")
    for value in values:
        result += "{},{}\n".format(str(value["time"]), value["value"])

    return result

def createTextOutputFromResult(metric, values, start, end):
    result = "start: {}\nend: {}\n".format(datetime.datetime.utcfromtimestamp(start), datetime.datetime.utcfromtimestamp(end))
    result += "\nmetric:\n{:40s} {}\n".format("field", "value")
    for key in metric:
        result += "{:40s} {}\n".format(key, metric[key])

    result += "\nvalues:\n{:40s} {}\n".format("time", "value")
    for value in values:
        result += "{:40s} {}\n".format(str(value["time"]), value["value"])

    return result


def processValues(values):
    result = []
    for value in values:
        result.append({"time": datetime.datetime.utcfromtimestamp(value[0]), "value": value[1]})

    return result

def getQueryOutput(url, query, start, end):
    return requests.get(url + "/api/v1/query_range", { "query": query, "start": start, "end": end, "step": 15 }).json()

def handleQueryOutput(output, csv, start, end):
    if output["status"] != "success":
        return "request failed"
    
    resultList = output["data"]["result"]
    if len(resultList) == 0:
        return "no results from query"
    
    functionResult = ""
    for result in resultList:
        values = processValues(result["values"])

        if csv is not None:
            functionResult += createCsvFromResult(result["metric"], values, start, end)
        else:
            functionResult += createTextOutputFromResult(result["metric"], values, start, end)
    
    if csv is not None:
        with open(csv, "w+") as csv_file:
            csv_file.write(functionResult)
            return "csv output written to " + csv
        
    return functionResult

def main():
    parser = argparse.ArgumentParser(description="Get prometheus timeseries data. Example queries: "
                                                 "\"rate(container_cpu_usage_seconds_total[1m]\", "
                                                 "\"container_memory_usage_bytes\", and "
                                                 "\"container_working_set_in_bytes\".")
    parser.add_argument("url", help="url for accessing prometheus")
    parser.add_argument("-q", "--query", required=True, help="the prometheus query")
    parser.add_argument("-d", "--duration", type=int, default=60, help="the duration in seconds which ends in the time the program was run")
    parser.add_argument("-s", "--start", type=int, help="the start of the Prometheus query interval")
    parser.add_argument("-e", "--end", type=int, help="the end of the Prometheus query interval")
    parser.add_argument("-c", "--csv", help="output csv file, otherwise print out json data")
    args = parser.parse_args(sys.argv[1:])

    queryOutput = {}
    if args.start is not None and args.end is not None:
        queryOutput = getQueryOutput(args.url, args.query, args.start, args.end)
        print(handleQueryOutput(queryOutput, args.csv, args.start, args.end))
    else:
        currentTime = time.time()
        queryOutput = getQueryOutput(args.url, args.query, currentTime - args.duration, currentTime)
        print(handleQueryOutput(queryOutput, args.csv, currentTime - args.duration, currentTime))

if __name__ == "__main__":
    main()