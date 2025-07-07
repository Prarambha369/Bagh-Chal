# Bagh-Chal: Tiger and Goats

Bagh-Chal (Nepali: बाघ चाल) is a traditional strategy board game from Nepal, played between two players: tigers and goats. The game is played on a 5x5 grid. One player controls four tigers, and the other controls up to twenty goats.

## Features
- Classic Bagh-Chal logic and rules
- Playable in three ways:
  - **Web version:** Modern, ancient-inspired UI (`index.html`)
  - **Python Tkinter version:** Simple GUI (`run.py`)
  - **C++ Console version:** Terminal-based (`baghchal.cpp`)

## How to Play
- **Tigers** try to capture 5 goats to win.
- **Goats** try to block all tigers so they cannot move.
- The game starts with tigers at the four corners. Goats are placed one by one on empty intersections.
- After all 20 goats are placed, both tigers and goats can move.
- Tigers can jump over adjacent goats to capture them.

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