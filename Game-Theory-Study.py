import npyscreen
import random
import textwrap
import os
import sys
import subprocess

def maximize_window():
    if os.name == "nt":  # Windows
        os.system("mode 800")  # Set the command prompt to a large size

    elif sys.platform == "darwin":  # macOS
        # Using AppleScript to try and maximize the terminal window
        script = """
            tell application "Terminal"
                activate
                do script ""
                set bounds of front window to {0, 0, 1400, 900}
            end tell
        """
        os.system(f"osascript -e '{script}'")

    elif sys.platform == "linux" or sys.platform == "linux2":  # Linux
        # This is a basic example for xterm. Adjust according to the terminal emulator in use.
        os.system("xterm -maximized &")


# Call the function at the start of your program
maximize_window()
# Define the main application class


class GameTheoryApp(npyscreen.NPSAppManaged):
    def onStart(self):
        self.addForm('MAIN', MainMenuForm, name="Game Theory - Main Menu")
        self.addForm('CONCEPTS', ConceptForm, name="Game Theory - Concepts")
        self.addForm('SIMULATIONS', SimulationForm,
                     name="Game Theory - Simulations")

# Main Menu Form


class MainMenuForm(npyscreen.ActionFormMinimal):
    def create(self):
        self.menu = self.add(npyscreen.TitleSelectOne, max_height=4, name="Choose an Option:", values=[
                             "Explore Concepts", "Run Simulations", "Exit"], relx=2, rely=2, max_width=40)

        # Bordered textbox for program details with corrected attribute
        program_info = ["Program Name: Game Theory Explorer",
                        "Version: 1.0.0", "Release Date: 15th Sept 2023"]
        self.program_details = self.add(npyscreen.BoxTitle, name="Program Details",
                                        values=program_info, relx=45, rely=2, max_width=40, max_height=6)

    def on_ok(self):
        if not self.menu.value:
            npyscreen.notify_confirm(
                "Select an option and then click OK", title="Error")
            return

        if self.menu.value[0] == 0:
            self.parentApp.switchForm('CONCEPTS')
        elif self.menu.value[0] == 1:
            self.parentApp.switchForm('SIMULATIONS')
        else:
            self.parentApp.switchForm(None)
# Concept Exploration Form

class ConceptForm(npyscreen.ActionFormMinimal):
    def create(self):
        self.concept = self.add(npyscreen.TitleSelectOne, max_height=9, name="Choose a Concept:",
                                values=["Prisoner's Dilemma", "Chicken (Game of Chicken)", "Stag Hunt", "Nash Equilibrium", "Dominant and Dominated Strategies", "Pure-Strategy Nash Equilibrium", "Folk's Theorem", "Grim Trigger Strategy", "Back to Main Menu"])
        self.explanation = self.add(
            npyscreen.MultiLineEdit, value="Choose a concept to see its explanation.", editable=False, relx=2, rely=12)

    def on_ok(self):
        if not self.concept.value:
            npyscreen.notify_confirm(
                "Select an option and then click OK", title="Error")
            return

        if self.concept.value[0] == 8:
            self.parentApp.switchForm('MAIN')
        else:
            explanations = [
                "Prisoner's Dilemma: A standard example of a game analyzed in game theory that shows why two completely rational individuals might not cooperate, even if it appears that it is in their best interests to do so.",
                "Chicken (Game of Chicken): A game in which two players drive towards each other on a collision course. One must swerve, or both may die in the crash, but if one driver swerves and the other does not, the one who swerved will be called a 'chicken', meaning a coward.",
                "Stag Hunt: A game which describes a conflict between safety and social cooperation. Two hunters can either jointly hunt a stag or individually hunt a rabbit. The stag provides more meat, but requires cooperation.",
                "Nash Equilibrium: A solution concept of a non-cooperative game involving two or more players in which each player is assumed to know the equilibrium strategies of the other players, and no player has anything to gain by changing only their own strategy.",
                "Dominant and Dominated Strategies: A strategy is dominant if, regardless of what any other players do, the strategy earns a player a larger payoff than any other. It is dominated if some other strategy always earns a greater payoff for that player.",
                "Pure-Strategy Nash Equilibrium: A situation where each player in a game has chosen a strategy and no player can benefit by changing his or her strategy while the other players keep theirs unchanged.",
                explain_folks_theorem()[0],
                "Grim Trigger Strategy: In repeated games, a player using this strategy cooperates as long as the other player cooperates, but defects forever as soon as the other player defects.",
                ""  # Back to Main Menu has no explanation
            ]

        if self.concept.value[0] == 8:
            self.parentApp.switchForm('MAIN')
        else:
            wrapped_text = textwrap.fill(
                explanations[self.concept.value[0]], width=60)
            self.explanation.value = wrapped_text
            self.explanation.display()

# Simulation Form

class SimulationForm(npyscreen.ActionFormMinimal):
    def create(self):
       # Sidebar for simulation options with more space
        self.simulation = self.add(npyscreen.TitleSelectOne, max_height=6, name="Choose a Simulation:", values=[
                                   "Prisoner's Dilemma", "Chicken (Game of Chicken)", "Stag Hunt", "Infinitely Repeated Prisoner's Dilemma", "Voting Game", "Back to Main Menu"], relx=2, rely=2, max_width=50)

        # Adjusted positioning for the explanation box
        self.explanation = self.add(npyscreen.MultiLineEdit, value="Choose a simulation to see its explanation.",
                                    editable=False, relx=54, rely=2, max_height=6, max_width=40)

        # Result of the simulation
        self.result = self.add(npyscreen.MultiLineEdit, value="Run a simulation to see its result.",
                               editable=False, relx=2, rely=9, max_height=6, max_width=92)

        # Graphics box
        self.graphics = self.add(
            npyscreen.BoxTitle, name="Graphics:", max_height=10, relx=54, rely=9, max_width=40)

    def on_ok(self):
        if not self.concept.value:
            npyscreen.notify_confirm(
                "Select an option and then click OK", title="Error")
            return

        if self.concept.value[0] == 8:
            self.parentApp.switchForm('MAIN')
        else:
            simulations = [simulate_prisoners_dilemma, simulate_game_of_chicken, simulate_stag_hunt,
                        simulate_infinitely_repeated_prisoners_dilemma, simulate_voting_game]
            explanations = [
                "Prisoner's Dilemma: Two prisoners must decide to cooperate with or betray each other. It showcases how individuals might not cooperate, even if it seems best to do so.",
                "Chicken (Game of Chicken): Two players drive towards each other on a collision course. One must swerve, or both may crash. The game describes risk and reward.",
                "Stag Hunt: Describes a conflict between safety and social cooperation. Two hunters can either jointly hunt a stag or individually hunt a rabbit.",
                "Infinitely Repeated Prisoner's Dilemma: A simulation where the prisoner's dilemma is played repeatedly, showcasing the long-term effects of decisions.",
                "Voting Game: A game that showcases how individuals might vote based on different strategies and the overall outcome of collective decisions."
            ]

        if self.simulation.value[0] == 5:
            self.parentApp.switchForm('MAIN')
        else:
            result, graphic = simulations[self.simulation.value[0]]()
            wrapped_result = textwrap.fill(result, width=85)
            wrapped_explanation = textwrap.fill(
                explanations[self.simulation.value[0]], width=50)

            self.result.value = wrapped_result
            self.explanation.value = wrapped_explanation
            self.graphics.values = graphic

            self.graphics.display()
            self.result.display()
            self.explanation.display()

# Define the game simulations


def simulate_infinitely_repeated_prisoners_dilemma():
    rounds = 100  # We'll simulate for 100 rounds to keep it computationally feasible
    actions = ['Cooperate', 'Defect']
    history = []

    p1_choice = random.choice(actions)
    p2_choice = random.choice(actions)

    for r in range(rounds):
        if 'Defect' in history:
            p1_choice = 'Defect'
            p2_choice = 'Defect'
        else:
            p1_choice = random.choice(actions)
            p2_choice = random.choice(actions)

        history.append((p1_choice, p2_choice))

    table = ["Round | P1 Choice | P2 Choice", "------+----------+----------"]
    for r, (p1, p2) in enumerate(history, 1):
        table.append(f"{r}     | {p1}      | {p2}")

    result = "Infinitely Repeated Prisoner's Dilemma simulated for 100 rounds using Grim Trigger Strategy."

    return (result, table)


def explain_folks_theorem():
    explanation = (
        "Folk's Theorem in Game Theory:\n\n"
        "Folk's Theorem states that in infinitely repeated games, any outcome is a Nash equilibrium "
        "if the sum of the benefits to all players in any deviant strategy, appropriately discounted, "
        "is no greater than the minimum of the sum of the benefits to all the players given their current strategies.\n\n"
        "Implications for Prisoner's Dilemma:\n"
        "In the context of the repeated prisoner's dilemma, it suggests that cooperation can be sustained "
        "as an equilibrium in the repeated game, even if players are tempted to defect in the one-shot game. "
        "This is because the future discounted benefits of cooperating can outweigh the one-time benefit of defecting."
    )
    return (explanation, [])

def simulate_legislative_bargaining():
    legislators = ['A', 'B', 'C']
    budget = 100
    proposals = {
        'A': (60, 25, 15),
        'B': (30, 50, 20),
        'C': (20, 20, 60)
    }

    proposing_legislator = random.choice(legislators)
    proposed_split = proposals[proposing_legislator]

    # Simple majority voting
    votes = [1 if proposed_split[i] >= (
        budget / len(legislators)) else 0 for i in range(len(legislators))]

    table = [
        "Legislator | Proposed Share | Vote",
        "-----------+----------------+-----",
        f"A          | {proposed_split[0]}             | {'Y' if votes[0] else 'N'}",
        f"B          | {proposed_split[1]}             | {'Y' if votes[1] else 'N'}",
        f"C          | {proposed_split[2]}             | {'Y' if votes[2] else 'N'}"
    ]

    if sum(votes) > len(legislators) / 2:
        result = f"Proposal by {proposing_legislator} is accepted."
    else:
        result = f"Proposal by {proposing_legislator} is rejected."

    return (result, table)

def simulate_prisoners_dilemma():
    actions = ["betray", "stay silent"]
    prisoner1_choice = random.choice(actions)
    prisoner2_choice = random.choice(actions)
    if prisoner1_choice == "betray" and prisoner2_choice == "betray":
        return ("Both prisoners chose to betray. Both get 2 years in prison.", ["+----+", "| BB |", "+----+", "Both betray."])
    elif prisoner1_choice == "betray" and prisoner2_choice == "stay silent":
        return ("Prisoner 1 chose to betray and goes free. Prisoner 2 chose to stay silent and gets 3 years in prison.", ["+----+", "| BS |", "+----+", "P1 betrays, P2 silent."])
    elif prisoner1_choice == "stay silent" and prisoner2_choice == "betray":
        return ("Prisoner 1 chose to stay silent and gets 3 years. Prisoner 2 chose to betray and goes free.", ["+----+", "| SB |", "+----+", "P1 silent, P2 betrays."])
    else:
        return ("Both prisoners chose to stay silent. Both get 1 year in prison.", ["+----+", "| SS |", "+----+", "Both stay silent."])


def simulate_game_of_chicken():
    actions = ["swerve", "continue"]
    player1_choice = random.choice(actions)
    player2_choice = random.choice(actions)
    if player1_choice == "swerve" and player2_choice == "continue":
        return ("Player 1 swerves. Player 2 continues.", ["+----+", "| SC |", "+----+", "Player 1 swerves."])
    elif player1_choice == "continue" and player2_choice == "swerve":
        return ("Player 1 continues. Player 2 swerves.", ["+----+", "| CS |", "+----+", "Player 2 swerves."])
    elif player1_choice == "swerve" and player2_choice == "swerve":
        return ("Both players swerve.", ["+----+", "| SS |", "+----+", "Both swerve."])
    else:
        return ("Both players continue and crash.", ["+----+", "| CC |", "+----+", "Both continue."])


def simulate_stag_hunt():
    actions = ["hunt stag", "hunt rabbit"]
    hunter1_choice = random.choice(actions)
    hunter2_choice = random.choice(actions)
    if hunter1_choice == "hunt stag" and hunter2_choice == "hunt stag":
        return ("Both hunters cooperate and catch a stag.", ["+----+", "| SS |", "+----+", "Both hunt stag."])
    elif hunter1_choice == "hunt stag" and hunter2_choice == "hunt rabbit":
        return ("Hunter 1 hunts stag but gets nothing. Hunter 2 hunts rabbit and gets a small reward.", ["+----+", "| SR |", "+----+", "P1 hunts stag, P2 hunts rabbit."])
    elif hunter1_choice == "hunt rabbit" and hunter2_choice == "hunt stag":
        return ("Hunter 1 hunts rabbit and gets a small reward. Hunter 2 hunts stag but gets nothing.", ["+----+", "| RS |", "+----+", "P1 hunts rabbit, P2 hunts stag."])
    else:
        return ("Both hunters hunt rabbits and get a small reward.", ["+----+", "| RR |", "+----+", "Both hunt rabbits."])


def simulate_voting_game():
    candidates = ['X', 'Y', 'Z']
    voter_preferences = {
        'Voter1': ['X', 'Y', 'Z'],
        'Voter2': ['Y', 'Z', 'X'],
        'Voter3': ['Z', 'X', 'Y']
    }

    votes = {candidate: 0 for candidate in candidates}

    for voter, preference in voter_preferences.items():
        votes[preference[0]] += 1  # Each voter votes for their top choice

    winner = max(votes, key=votes.get)

    table = [
        "Candidate | Votes",
        "----------+------",
        f"X         | {votes['X']}",
        f"Y         | {votes['Y']}",
        f"Z         | {votes['Z']}"
    ]

    result = f"Candidate {winner} wins the election."

    return (result, table)


def simulate_grim_trigger():
    rounds = 5
    actions = ['Cooperate', 'Defect']
    history = []

    p1_choice = random.choice(actions)
    p2_choice = random.choice(actions)

    for r in range(rounds):
        if 'Defect' in history:
            p1_choice = 'Defect'
            p2_choice = 'Defect'
        else:
            p1_choice = random.choice(actions)
            p2_choice = random.choice(actions)

        history.append((p1_choice, p2_choice))

    table = [
        "Round | P1 Choice | P2 Choice",
        "------+----------+----------"
    ]
    for r, (p1, p2) in enumerate(history, 1):
        table.append(f"{r}     | {p1}      | {p2}")

    result = "Grim Trigger Strategy played for 5 rounds."

    return (result, table)

if __name__ == "__main__":
    app = GameTheoryApp()
    app.run()