This is my ongoing attempt to build a robot to play Connect Four, and eventually other board games.

Use playervsagent.py to play against the program.

Current capabilities:
When it is the agent's turn, it will look ahead and check for any wins or losses, or future forced wins or losses. If found, it will act accordingly.
If nothing is found, the move will be decided by a randomly generated neural network. It doesn't train yet.

Things to add:
Make the neural network actually learn, and make the focus eventually.
If hard looking ahead remains a strategy, it should look ahead during the opponents turn as well, I've started working on this in the experimental branch.

Of course, I will also be working on programming the hardware code, which is currently in the hardware branch. This will use an Arduino and micro-computer (Raspberry Pi maybe), working together. The Arduino will take Cartesian coordinates via serial and turn them into servo movements. The micro-board will handle the actual gameplay, learning and computer vision, and will send coordinates to the Arduino. Computer vision will probable use OpenCV.
