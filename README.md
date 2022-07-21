# SGAI - Outbreak
This is the repository that Beaverworks' SGAI 2022 will be using to understand
serious games and reinforcement learning.

## Team Courtney II
The best team out there.

## How to run
### VS Code version
DO NOT run main.py when the current directory is SGAI-Outbreak.
You must open the folder SGAI_MK3 with vscode. Then, you can
run main.py from VS Code.
### cmd line version
First, `cd ./SGAI_MK3`. Then, `python main.py`

## How to play
There are basic moves:
- Move - click on a person that you control and a square next to them.
If the square isn't occupied, the person will move to that square.
- Bite - If you are playing as a zombie,
you can click the bite button and then a person next to a zombie
to turn the person into a zombie. NOTE: THIS DOES NOT ALWAYS SUCCEED
BECAUSE GAME MECHANICS MAKE IT SO THAT THERE IS A CHANCE THAT BITING WILL
FAIL. THIS IS NOT A BUG. THIS IS A GAME MECHANIC.
- Heal - If you are playing as the government, you 
can click the cure button and a person or zombie.
If you clicked a zombie, the zombie will become a person again 
(this is curing). If you clicked a person, the person will become
vaccinated (this is vaccination). Vaccination lasts for 5 turns and
gives 100% immunity to being zombified.