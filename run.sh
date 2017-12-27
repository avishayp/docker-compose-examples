#!/usr/bin/env bash

# ./run.sh example2 ==> run single example
#
# ./run.sh ==> run all

# colors
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

pass() {
    echo -e "$GREEN PASSED: $@ $NC"
}

fail() {
    echo -e "$RED FAILED: $@ $NC"
}

trap 'kill $BG_PROBE_PID; exit' SIGINT

bg_probe_exit() {
    # if we have tester service, we take its exit code
    # this has no support in docker-compose, as --exit-code-from aborts on first container exit
    # this function is executed in background
    NAME=${1}_tester_1

    echo "starting background probe for service $NAME"
    while sleep 1 ; do

        STATUS=$(docker inspect "$NAME" --format='{{.State.Status}}' 2>/dev/null)

        if [ "$STATUS" == "exited" ] ; then
            CODE=$(docker inspect "$NAME" --format='{{.State.ExitCode}}')
            echo "$NAME in status $STATUS ($CODE)"
            docker-compose kill
            return $CODE
        fi

        [ -z "$STATUS" ] && echo "$NAME still building..." || echo "$NAME still in status $STATUS... waiting for it to exit"
    done
}

up() {
    clean
    docker-compose up --build
}

clean() {
    docker-compose down --volumes
}

run_example() {
    echo "running $1"
    pushd "$1"
    if has_tester_service ; then
        bg_probe_exit "$1" &
        BG_PROBE_PID=$!
        up
        wait $BG_PROBE_PID
    else
        echo "$1 has no tester service"
        up
    fi
    RES=$?
    [ $RES -eq 0 ] && pass "$1" || fail "$1 (exit code: $RES)"
    clean
    popd
}

run_all() {
    for X in ex* ; do run_example "$X" ; done
}

has_tester_service() {
    docker-compose config --services | grep -q tester
}

[ -z "$1" ] && run_all || run_example $1