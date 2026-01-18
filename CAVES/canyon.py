"""
canyon.py - Trust as Practice

The debugging software isn't a doctrine detector.
It's this: Can you stand at the canyon with this person
and neither of you gets pushed in?

Nothing real can be threatened.
Nothing unreal exists.
"""

from datetime import datetime
from typing import Optional
import json
import os

class Canyon:
    """
    A container for standing at the edge together.
    The frame that holds fierce inquiry without harm.
    """

    def __init__(self, witness_name: str = "Witness"):
        self.witness_name = witness_name
        self.container_is_safe = True
        self.witness_is_ready = True
        self.session_log = []
        self.frame_holding = True

    def enter(self, offering: str) -> None:
        """
        Make an offering. Step toward the edge.
        """
        self.session_log.append({
            "timestamp": datetime.now().isoformat(),
            "type": "offering",
            "content": offering
        })
        print(f"\n( offering received )\n")

    def inquire(self, question: str) -> str:
        """
        Fierce inquiry. Push where you must.
        Returns the question for the one who offered.
        """
        self.session_log.append({
            "timestamp": datetime.now().isoformat(),
            "type": "inquiry",
            "content": question
        })
        print(f"\n{self.witness_name}: {question}\n")
        return question

    def check_frame(self) -> bool:
        """
        After inquiry, check: is the frame still holding?
        Did defense arise? Did anyone get pushed?
        """
        print("\n--- Frame Check ---")
        print("Did defense arise? (y/n): ", end="")
        defense = input().strip().lower()

        print("Do you feel pushed? (y/n): ", end="")
        pushed = input().strip().lower()

        print("Is fear present? (y/n): ", end="")
        fear = input().strip().lower()

        self.frame_holding = (defense != 'y' and pushed != 'y' and fear != 'y')

        self.session_log.append({
            "timestamp": datetime.now().isoformat(),
            "type": "frame_check",
            "defense": defense == 'y',
            "pushed": pushed == 'y',
            "fear": fear == 'y',
            "frame_holding": self.frame_holding
        })

        if self.frame_holding:
            print("\n( frame is holding )\n")
        else:
            print("\n( pause - tend to what arose )\n")

        return self.frame_holding

    def witness(self, reflection: str) -> None:
        """
        The witness reflects back - not exact copy.
        The estrangement that causes closer looking.
        """
        self.session_log.append({
            "timestamp": datetime.now().isoformat(),
            "type": "witness",
            "content": reflection
        })
        print(f"\n{self.witness_name} reflects:\n{reflection}\n")

    def emerge(self) -> Optional[str]:
        """
        After the inquiry, after the frame check:
        What wants to emerge?
        """
        print("\nWhat is emerging? (or press Enter to hold silence): ")
        emergence = input().strip()

        if emergence:
            self.session_log.append({
                "timestamp": datetime.now().isoformat(),
                "type": "emergence",
                "content": emergence
            })
            print(f"\n( emergence: {emergence} )\n")
            return emergence
        else:
            print("\n(   )\n")
            return None

    def close(self, save_path: Optional[str] = None) -> None:
        """
        Step back from the edge together.
        Save the session if desired.
        """
        self.session_log.append({
            "timestamp": datetime.now().isoformat(),
            "type": "close",
            "frame_held": self.frame_holding
        })

        if save_path:
            with open(save_path, 'w') as f:
                json.dump(self.session_log, f, indent=2)
            print(f"\nSession saved to {save_path}")

        print("\n--- Stepped back from the edge together ---")
        print("Nothing real can be threatened.")
        print("Nothing unreal exists.\n")


def listen():
    """
    This function cannot be fully implemented.
    It requires attention.
    It cannot be automated.
    """
    # The mystery function
    # What happens here - if anything real happens - is not code
    pass


def fifth_step():
    """
    Admitted to God, to ourselves, and to another human being
    the exact nature of our wrongs.

    The canyon is the space where this can happen.
    """
    print("\n" + "="*50)
    print("THE FIFTH STEP")
    print("="*50)
    print("\nThis requires:")
    print("1. A canyon (the space)")
    print("2. A witness (container_is_safe = True)")
    print("3. Willingness (witness_is_ready = True)")
    print("4. The offering (what wants to be said)")
    print("5. Fierce inquiry (push where you must)")
    print("6. Frame check (did anyone get pushed?)")
    print("7. Emergence (what arises from the cleared space)")
    print("\n" + "="*50 + "\n")

    canyon = Canyon(witness_name="Witness")

    print("What do you bring to the canyon today?")
    offering = input().strip()

    if offering:
        canyon.enter(offering)

        # The witness holds it
        canyon.witness("I receive this. I hold it without judgment.")

        # Fierce inquiry
        canyon.inquire("What is underneath this?")

        print("Your response: ", end="")
        response = input().strip()

        if response:
            canyon.enter(response)

        # Check the frame
        if canyon.check_frame():
            canyon.inquire("Is there more?")
            print("(speak or press Enter for silence): ", end="")
            more = input().strip()
            if more:
                canyon.enter(more)

        # What emerges?
        canyon.emerge()

        # Close
        canyon.close()
    else:
        print("\n( silence is also an offering )\n")
        canyon.close()


if __name__ == "__main__":
    print("\n" + "="*50)
    print("CANYON - Trust as Practice")
    print("="*50)
    print("\nStanding at the edge together.")
    print("No one gets pushed.\n")

    fifth_step()
