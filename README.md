Joes Racer

A fun and competitive multiplayer racing game built with Python and Pygame. Challenge your friends, dodge obstacles, and collect health packs to keep your car running!

**Features**
Two-player mode: Compete against another player on a shared track.
Health System: Lose health when hitting obstacles and regain it by collecting health packs.
Dynamic Gameplay: Randomized obstacles, moving challenges, and health packs keep each race exciting.
Ready Up and Countdown: Players must signal they're ready before the game begins.

**Prerequisites**
Before you can run the game, make sure you have the following installed:

Python 3.7+
Pygame (install using pip install pygame)

**Installation and Setup**
Clone this repository:

bash
Copy code
git clone https://github.com/your-username/joesracer.git
cd joesracer

**Install dependencies:**

bash
Copy code
pip install pygame

**Ensure the following asset files are in the same directory as the script:**

player1_car.png
player2_car.png
obstacle.png
death.png
heart.png
Note: If these files are missing, the game will use colored placeholders.

**Run the game:**

bash
Copy code
python joesracer.py


**Repository Structure**
bash
Copy code
joesracer/
├── joesracer.py       # Main Python script
├── README.md          # Project documentation
├── LICENSE            # License file
├── player1_car.png    # Player 1's car image
├── player2_car.png    # Player 2's car image
├── obstacle.png       # Obstacle image
├── death.png          # Death animation image
└── heart.png          # Health pack image

**How to Play**
Both players must press their respective "Ready" keys:
Player 1: R
Player 2: P
Use the following controls to move your car:
Player 1: W (up), A (left), S (down), D (right)
Player 2: Arrow keys: ↑ (up), ← (left), ↓ (down), → (right)
Avoid obstacles and collect health packs to stay in the game.
First player to lose all their health loses the game!

**License**
See the LICENSE file for details.
