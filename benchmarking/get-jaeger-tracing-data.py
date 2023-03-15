import requests
import argparse
import sys
import time
import datetime

# OPERATION_NAMES = ["runtime.v1.RuntimeService/RunPodSandbox",
#                    "runtime.v1.RuntimeService/CreateContainer",
#                    "runtime.v1.RuntimeService/StartContainer",
#                    "runtime.v1.RuntimeService/StopContainer",
#                    "runtime.v1.RuntimeService/RemoveContainer",
#                    "runtime.v1.RuntimeService/StopPodSandbox",
#                    "runtime.v1.RuntimeService/RemovePodSandbox"]

def createCsvFromResult(processedDict):
    result = ""
    for key in processedDict:
        operationSpans = processedDict[key]
        result += "{}\n{},{}\n".format(key, "startTime", "duration")
        for span in operationSpans:
            result += "{},{}\n".format(str(datetime.datetime.utcfromtimestamp(span["startTime"]/1000000)), str(span["duration"]))
        result += "\n"

    return result

def createTextOutputFromResult(processedDict):
    result = ""
    for key in processedDict:
        operationSpans = processedDict[key]
        result += "{}, {} durations:\n{:40s} {}\n".format(key, len(operationSpans), "startTime", "duration")
        for span in operationSpans:
            result += "{:40s} {}\n".format(str(datetime.datetime.utcfromtimestamp(span["startTime"]/1000000)), str(span["duration"]))
        result += "\n"

    return result


def processSpansAndTraces(url):
    result = {
        "runtime.v1.RuntimeService/RunPodSandbox": [],
        "runtime.v1.RuntimeService/CreateContainer": [],
        "runtime.v1.RuntimeService/StartContainer": [],
        "runtime.v1.RuntimeService/StopContainer": [],
        "runtime.v1.RuntimeService/RemoveContainer": [],
        "runtime.v1.RuntimeService/StopPodSandbox": [],
        "runtime.v1.RuntimeService/RemovePodSandbox": []
    }
    for key in result:
        output = getQueryOutput(url, key)

        if output["errors"] != None:
            return "request failed"

        traceList = output["data"]
        if len(traceList) == 0:
            return "no results from query"

        for trace in traceList:
            spans = trace["spans"]
            for span in spans:
                operationName = span["operationName"]
                result[operationName].append(span)

    return result

def getQueryOutput(url, operationName):
    return requests.get(url + "/api/traces", { "service": "containerd", "operation": operationName}).json()

def handleQueryOutput(url, csv):    
    processedDict = processSpansAndTraces(url)

    if csv is not None:
        with open(csv, "w+") as csv_file:
            csv_file.write(createCsvFromResult(processedDict))
            return "csv output written to " + csv
    else:
        return createTextOutputFromResult(processedDict)
    

def main():
    parser = argparse.ArgumentParser(description="Get jaeger tracing data.")
    parser.add_argument("url", help="url for accessing jaeger")
    parser.add_argument("-c", "--csv", help="output csv file, otherwise print out json data")
    args = parser.parse_args(sys.argv[1:])

    currentTime = time.time()

    print(handleQueryOutput(args.url, args.csv))

if __name__ == "__main__":
    main()
