# Demo setup

This is work in progress

## How to use

1. Configure cluster to desired state.

2. Run the `pre_run.sh` script

```console
usage: ./scripts/pre_run.sh -p <use prometheus: "true" or "false">
```

3. Start jaeger on the same node with `jaeger.sh`.

4. Run the test with `run_test.sh`.

```console
usage: ./scripts/run_test.sh
    -n <number of stress-ng containers in increment>
    -i <increments>
    -l <filename label>
    -s <time to sleep waiting to query results>"
```

5. To remove installed resources, run `destroy-deployment.sh`.

## How to setup tracing

https://github.com/containerd/containerd/blob/main/docs/tracing.md