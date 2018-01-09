[![CircleCI](https://circleci.com/gh/avishayp/docker-compose-examples.svg?style=svg)](https://circleci.com/gh/avishayp/docker-compose-examples)

# docker-compose examples

Collection of docker-compose examples, ordered in ascending complexity.

### Examples guidelines

 * `docker-compose up` just works
 * Whenever possible, `docker-compose up --exit-code-from tester` just works
 * Zero dependencies
 * Simple

### Run

The only prerequisites are `docker` and `docker-compose`.
 * `./run.sh` would run all examples
 * `tox` does the exact same thing
 * `./run.sh exampleX` runs only exampleX

### Contribution

Additional examples and feedback on existing ones are welcome!
For feedback, it's best to open an issue. For a new example submit a PR.