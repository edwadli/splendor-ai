# splendor-ai
Splendor and AIs that play it

When running the code, make sure you are in the base directory. Sample run (sanity check):
```
python -B -m src.hello_world
```

## Bot Tournament

To run the round robin tournament:
```
python -B -m src.game.tournament.round_robin_main
```

## Development

To run all unit tests:
```
./src/run_all_tests.sh
```

To clear .pyc files:
```
find . -name '*.pyc' -delete
```
