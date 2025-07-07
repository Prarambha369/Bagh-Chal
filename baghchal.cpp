#include <iostream>
#include <vector>
#include <string>
#include <iomanip>
#include <random>
using namespace std;

const int BOARD_SIZE = 5;
const int EMPTY = 0;
const int TIGER = 1;
const int GOAT = 2;
const int TIGER_PLAYER = 0;
const int GOAT_PLAYER = 1;

struct Move {
    int fromRow, fromCol, toRow, toCol;
};

class BaghChal {
    vector<vector<int>> board;
    int goatsPlaced, goatsCaptured, currentPlayer, phase;
    int selectedRow, selectedCol;
    static const int PLACEMENT_PHASE = 0;
    static const int MOVEMENT_PHASE = 1;
    bool botTiger = false, botGoat = false;
    std::mt19937 rng{std::random_device{}()};

public:
    BaghChal(bool botT = false, bool botG = false) : botTiger(botT), botGoat(botG) {
        board = vector<vector<int>>(BOARD_SIZE, vector<int>(BOARD_SIZE, EMPTY));
        goatsPlaced = goatsCaptured = 0;
        currentPlayer = GOAT_PLAYER;
        phase = PLACEMENT_PHASE;
        selectedRow = selectedCol = -1;
        // Place tigers at corners
        board[0][0] = board[0][4] = board[4][0] = board[4][4] = TIGER;
    }

    void printBoard() {
        cout << "\n    0   1   2   3   4" << endl;
        for (int i = 0; i < BOARD_SIZE; ++i) {
            cout << "  +---+---+---+---+---+" << endl;
            cout << i << " |";
            for (int j = 0; j < BOARD_SIZE; ++j) {
                if (board[i][j] == TIGER) cout << " T |";
                else if (board[i][j] == GOAT) cout << " G |";
                else cout << "   |";
            }
            cout << endl;
        }
        cout << "  +---+---+---+---+---+" << endl;
        cout << "Goats placed: " << goatsPlaced << "/20, Goats captured: " << goatsCaptured << "/5\n";
    }

    bool isValidMove(int fromRow, int fromCol, int toRow, int toCol) {
        if (toRow < 0 || toRow >= BOARD_SIZE || toCol < 0 || toCol >= BOARD_SIZE)
            return false;
        if (board[toRow][toCol] != EMPTY) return false;
        int dr = abs(toRow - fromRow), dc = abs(toCol - fromCol);
        // Only adjacent or jump
        if ((dr == 1 && dc == 0) || (dr == 0 && dc == 1) || (dr == 1 && dc == 1))
            return true;
        if (board[fromRow][fromCol] == TIGER && ((dr == 2 && dc <= 2) || (dc == 2 && dr <= 2))) {
            int midRow = (fromRow + toRow) / 2, midCol = (fromCol + toCol) / 2;
            if (board[midRow][midCol] == GOAT)
                return true;
        }
        return false;
    }

    bool canTigersMove() {
        for (int i = 0; i < BOARD_SIZE; ++i) {
            for (int j = 0; j < BOARD_SIZE; ++j) {
                if (board[i][j] == TIGER) {
                    for (int dr = -2; dr <= 2; ++dr) {
                        for (int dc = -2; dc <= 2; ++dc) {
                            if (dr == 0 && dc == 0) continue;
                            int ni = i + dr, nj = j + dc;
                            if (ni >= 0 && ni < BOARD_SIZE && nj >= 0 && nj < BOARD_SIZE) {
                                if (isValidMove(i, j, ni, nj))
                                    return true;
                            }
                        }
                    }
                }
            }
        }
        return false;
    }

    // Bot logic: pick a random valid move
    bool botMove() {
        vector<pair<int, int>> froms, tos;
        if (phase == PLACEMENT_PHASE && currentPlayer == GOAT_PLAYER && botGoat && goatsPlaced < 20) {
            // Place goat randomly
            for (int i = 0; i < BOARD_SIZE; ++i)
                for (int j = 0; j < BOARD_SIZE; ++j)
                    if (board[i][j] == EMPTY) froms.emplace_back(i, j);
            if (froms.empty()) return false;
            auto [r, c] = froms[rng() % froms.size()];
            board[r][c] = GOAT;
            goatsPlaced++;
            if (goatsPlaced == 20) phase = MOVEMENT_PHASE;
            currentPlayer = TIGER_PLAYER;
            return true;
        } else {
            // Movement phase
            for (int i = 0; i < BOARD_SIZE; ++i) {
                for (int j = 0; j < BOARD_SIZE; ++j) {
                    if ((currentPlayer == TIGER_PLAYER && botTiger && board[i][j] == TIGER) ||
                        (currentPlayer == GOAT_PLAYER && botGoat && board[i][j] == GOAT)) {
                        for (int dr = -2; dr <= 2; ++dr) {
                            for (int dc = -2; dc <= 2; ++dc) {
                                if (dr == 0 && dc == 0) continue;
                                int ni = i + dr, nj = j + dc;
                                if (ni >= 0 && ni < BOARD_SIZE && nj >= 0 && nj < BOARD_SIZE && isValidMove(i, j, ni, nj)) {
                                    froms.emplace_back(i, j);
                                    tos.emplace_back(ni, nj);
                                }
                            }
                        }
                    }
                }
            }
            if (froms.empty()) return false;
            int idx = rng() % froms.size();
            int fr = froms[idx].first, fc = froms[idx].second, tr = tos[idx].first, tc = tos[idx].second;
            if (board[fr][fc] == TIGER && abs(tr - fr) == 2 && abs(tc - fc) <= 2) {
                int mr = (fr + tr) / 2, mc = (fc + tc) / 2;
                if (board[mr][mc] == GOAT) {
                    board[mr][mc] = EMPTY;
                    goatsCaptured++;
                }
            }
            board[tr][tc] = board[fr][fc];
            board[fr][fc] = EMPTY;
            currentPlayer = 1 - currentPlayer;
            return true;
        }
        return false;
    }

    void play() {
        while (true) {
            printBoard();
            if (goatsCaptured >= 5) {
                cout << "\nTigers win!\n";
                break;
            }
            if (phase == MOVEMENT_PHASE && !canTigersMove()) {
                cout << "\nGoats win!\n";
                break;
            }
            if ((botGoat && currentPlayer == GOAT_PLAYER) || (botTiger && currentPlayer == TIGER_PLAYER)) {
                cout << "Bot is thinking...\n";
                botMove();
                continue;
            }
            if (phase == PLACEMENT_PHASE && goatsPlaced < 20 && currentPlayer == GOAT_PLAYER) {
                cout << "Goat Placement Phase. Enter row and col to place goat: ";
                int r, c; cin >> r >> c;
                if (r < 0 || r >= BOARD_SIZE || c < 0 || c >= BOARD_SIZE || board[r][c] != EMPTY) {
                    cout << "Invalid placement. Try again.\n";
                    continue;
                }
                board[r][c] = GOAT;
                goatsPlaced++;
                if (goatsPlaced == 20) phase = MOVEMENT_PHASE;
                currentPlayer = TIGER_PLAYER;
            } else {
                if (currentPlayer == TIGER_PLAYER) cout << "Tiger's turn. ";
                else cout << "Goat's turn. ";
                cout << "Enter from_row from_col to_row to_col: ";
                int fr, fc, tr, tc; cin >> fr >> fc >> tr >> tc;
                if (fr < 0 || fr >= BOARD_SIZE || fc < 0 || fc >= BOARD_SIZE ||
                    tr < 0 || tr >= BOARD_SIZE || tc < 0 || tc >= BOARD_SIZE) {
                    cout << "Invalid coordinates. Try again.\n";
                    continue;
                }
                if (board[fr][fc] == EMPTY) {
                    cout << "No piece at source. Try again.\n";
                    continue;
                }
                if (currentPlayer == TIGER_PLAYER && board[fr][fc] != TIGER) {
                    cout << "Select a tiger. Try again.\n";
                    continue;
                }
                if (currentPlayer == GOAT_PLAYER && board[fr][fc] != GOAT) {
                    cout << "Select a goat. Try again.\n";
                    continue;
                }
                if (!isValidMove(fr, fc, tr, tc)) {
                    cout << "Invalid move. Try again.\n";
                    continue;
                }
                // Execute move
                if (board[fr][fc] == TIGER && abs(tr - fr) == 2 && abs(tc - fc) <= 2) {
                    int mr = (fr + tr) / 2, mc = (fc + tc) / 2;
                    if (board[mr][mc] == GOAT) {
                        board[mr][mc] = EMPTY;
                        goatsCaptured++;
                    }
                }
                board[tr][tc] = board[fr][fc];
                board[fr][fc] = EMPTY;
                currentPlayer = 1 - currentPlayer;
            }
        }
    }
};

int main() {
    cout << "🐅 Bagh-Chal: Tiger and Goats (C++ Console Edition) 🐐\n";
    cout << "Select mode: 1) Human vs Human  2) Human vs Bot (Bot=Tigers)  3) Human vs Bot (Bot=Goats): ";
    int mode; cin >> mode;
    BaghChal game(mode==2, mode==3);
    game.play();
    return 0;
}
