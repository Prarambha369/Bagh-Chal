# Bagh-Chal: Tiger and Goats

Bagh-Chal (Nepali: बाघ चाल) is a traditional strategy board game from Nepal, played between two players: tigers and goats. The game is played on a 5x5 grid. One player controls four tigers, and the other controls up to twenty goats.

## Features
- Classic Bagh-Chal logic and rules
- Playable in three ways:
  - **Web version:** Modern, ancient-inspired UI (`index.html`)
  - **Python Tkinter version:** Simple GUI (`run.py`)
  - **C++ Console version:** Terminal-based (`baghchal.cpp`)

## Game Logic Consistency
All versions (Web, Python, C++) now use the same rules and logic:
- 5x5 board, 4 tigers (start at corners), 20 goats
- Goats are placed one by one, then both sides move
- Tigers can jump/capture goats; goats move to adjacent empty spots
- Tigers win by capturing 5 goats
- Goats win by blocking all tigers
- No AI/bot by default; all versions are human vs human

## How to Play
- **Tigers** try to capture 5 goats to win.
- **Goats** try to block all tigers so they cannot move.
- The game starts with tigers at the four corners. Goats are placed one by one on empty intersections.
- After all 20 goats are placed, both tigers and goats can move.
- Tigers can jump over adjacent goats to capture them.

## How to Play (Quick)
- Goats place pieces until all 20 are on the board
- After placement, both tigers and goats take turns moving
- Tigers can jump over goats to capture (removing them)
- Enter moves as prompted (row/col numbers start at 0)

## Version Sync
- The C++ (`baghchal.cpp`), Python (`run.py`), and Web (`index.html`) versions now match in rules and gameplay
- All code is cleaned, comment-free, and easy to read

## Running the Game

### Web Version
Open `index.html` in your browser.

### Python Version
Requires Python 3.
```sh
python3 run.py
```

### C++ Console Version
Requires a C++ compiler (e.g., g++):
```sh
g++ baghchal.cpp -o baghchal
./baghchal
```

## File Overview
- `index.html` — Web version (JS/HTML/CSS)
- `run.py` — Python Tkinter GUI version
- `baghchal.cpp` — C++ console version
- `README.md` — This file

## Credits
- Ancient game of Nepal
- Modern code by contributors

## License
Open source for educational and personal use.