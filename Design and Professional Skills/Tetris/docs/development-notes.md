# Tetris development notes

## Deferred seed visibility question

Saved on 23 November 2026 for possible later discussion.

The authoritative process in `client.py` reads the `SEED` environment variable to initialise its piece generator. The player-side process in `server.py` receives shapes through the text protocol; that protocol does not transmit the seed or random-generator state.

The grading system's process-launch configuration is absent from this repository. Whether `SEED` is also present in the player's environment is therefore unknown. Running within the same grading infrastructure does not establish that both processes share environment variables.

This is an unresolved question about environment isolation, not a confirmed source of future-piece information. No seed inspection or prediction has been implemented. The algorithm should work using the current piece and the single preview provided by the documented interface.

Relevant sources: [authoritative process](../client.py), [player-side process](../server.py), [assignment brief](assignment4.pdf).
