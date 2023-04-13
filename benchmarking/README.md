# Demo setup

This is work in progress

## How to use

1. Configure cluster to desired state.

2. Run the `pre_run.sh` script. This deploys Jaeger and Prometheus. Example:

```console
./scripts/pre_run.sh
```

```console
usage: ./scripts/pre_run.sh -p <use prometheus: "true" or "false">
```

3. Wait for the Jaeger and Prometheus pods to be ready.

4. Run the test with `run_test.sh`. Example:

```console
./scripts/run_test.sh -n 10 -i 9 -l baseline
```

```console
usage: ./scripts/run_test.sh
    -n <number of stress-ng containers in increment>
    -i <increments>
    -l <filename label>
    -s <time to sleep waiting to query results>
```

5. To remove installed resources, run `destroy-deployment.sh`.

6. Repeat steps 1-5 for each desired setup and **label each setup with different labels that are not substrings of each other**.

7. Generate graphs with `plot-graphs.py`. If you use labels `baseline`, `template`, and `topology-aware` you can use the `post_run.sh` script.

8. Remove all files from the output directory to not have overlapping labels (filenames).

## How to setup tracing

https://github.com/containerd/containerd/blob/main/docs/tracing.md
