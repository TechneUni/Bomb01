import math  # I have to check your math by using my math anyways
import time  # Used for time.sleep() function which just waits for some time

# Importing the bomb files to test them
from bombs.auxiliary import (airConditioningVentilationChecker,
                             mcuCoffeeMakerGoFlag, waterBottleStation)
from bombs.critical import (cryptographicCircleChecker, errorLogLevelChecker,
                            ncHashDerive, parityChecker, passChannel,
                            swapChannel, vIOFlag)

# ===== Helper =================================================================


# Checks if a particular condition is met for a lock
def checkLock(condition, message):
    print(message, end="")
    if condition:
        print("OK")
    else:
        time.sleep(0.5)
        print("FAILED")

    return condition


# ===== Critical lock checks ===================================================


def checkCriticalLocks():
    locksChecked = True

    # vIOFlag lock
    locksChecked = locksChecked and checkLock(
        vIOFlag() > 0,
        "Checking value I/O (vIO) flag..."
    )

    # passChannel lock
    locksChecked = locksChecked and checkLock(
        passChannel(1) == 1,
        "Checking password channel (1)..."
    )
    locksChecked = locksChecked and checkLock(
        passChannel(2) == 2,
        "Checking password channel (2)..."
    )
    locksChecked = locksChecked and checkLock(
        passChannel("a") == "a",
        "Checking password channel (3)..."
    )

    # swapChannel lock
    locksChecked = locksChecked and checkLock(
        swapChannel(1, 2) == (2, 1),
        "Checking swap channel (1)..."
    )
    locksChecked = locksChecked and checkLock(
        swapChannel("asdf", "jkl;") == ("jkl;", "asdf"),
        "Checking swap channel (2)..."
    )

    # ncHashDerive lock
    locksChecked = locksChecked and checkLock(
        ncHashDerive(1, 2) == ((1 + 2) * (1 - 2)) % 256,
        "Checking non-cryptographic hash derivation (1)..."
    )
    locksChecked = locksChecked and checkLock(
        ncHashDerive(3, 4) == ((3 + 4) * (3 - 4)) % 256,
        "Checking non-cryptographic hash derivation (2)..."
    )
    locksChecked = locksChecked and checkLock(
        ncHashDerive(14, 32) == ((14 + 32) * (14 - 32)) % 256,
        "Checking non-cryptographic hash derivation (3)..."
    )

    # parityChecker lock
    locksChecked = locksChecked and checkLock(
        parityChecker(1) == False,
        "Checking parity checker (1)..."
    )
    locksChecked = locksChecked and checkLock(
        parityChecker(2) == True,
        "Checking parity checker (2)..."
    )
    locksChecked = locksChecked and checkLock(
        parityChecker(3) == False,
        "Checking parity checker (3)..."
    )
    locksChecked = locksChecked and checkLock(
        parityChecker(4) == True,
        "Checking parity checker (4)..."
    )

    # cryptographicCircleChecker lock
    def V(x): return (4/3) * math.pi * x**3
    def A(x): return 4 * math.pi * x**2
    locksChecked = locksChecked and checkLock(
        cryptographicCircleChecker(V(3)) == A(3),
        "Checking cryptographic circle checker (1)..."
    )
    locksChecked = locksChecked and checkLock(
        cryptographicCircleChecker(V(25)) == A(25),
        "Checking cryptographic circle checker (2)..."
    )

    if locksChecked:
        print("All critical locks are OK")
    else:
        print("Critical locks are NOT OK")
        print("Critical bomb exploded. MCU data lost.")


# ===== Auxiliary lock checks ==================================================


def checkAuxiliaryLocks():
    locksChecked = True

    # waterBottleStation lock
    def xPos(a, b, c): return (-b + math.sqrt(b**2 - 4*a*c)) / (2*a)
    def xNeg(a, b, c): return (-b - math.sqrt(b**2 - 4*a*c)) / (2*a)
    locksChecked = locksChecked and checkLock(
        waterBottleStation(1, 2, 3) == (xPos(1, 2, 3), xNeg(1, 2, 3)),
        "Checking water bottle station (1)..."
    )
    locksChecked = locksChecked and checkLock(
        waterBottleStation(4, 5, 6) == (xPos(4, 5, 6), xNeg(4, 5, 6)),
        "Checking water bottle station (2)..."
    )

    # airConditioningVentilationChecker lock
    def kToF(x): return (x - 273.15) * (9/5) + 32
    locksChecked = locksChecked and checkLock(
        airConditioningVentilationChecker(300) == True,
        "Checking air conditioning ventilation checker (1)..."
    )
    locksChecked = locksChecked and checkLock(
        airConditioningVentilationChecker(273.15) == False,
        "Checking air conditioning ventilation checker (2)..."
    )

    # mcuCoffeeMakerGoFlag lock
    def gToLbs(x): return x / 453.592
    def cToF(x): return x * (9/5) + 32
    locksChecked = locksChecked and checkLock(
        mcuCoffeeMakerGoFlag(1, 2, False) == (
            gToLbs(1) > 0.25) and (cToF(2) > 102) and False,
        "Checking MCU coffee maker go flag (1)..."
    )
    locksChecked = locksChecked and checkLock(
        mcuCoffeeMakerGoFlag(453.592, 100, False) == (
            gToLbs(453.592) > 0.25) and (cToF(100) > 102) and True,
        "Checking MCU coffee maker go flag (2)..."
    )

    if locksChecked:
        print("All auxiliary locks are OK")
    else:
        print("Auxiliary locks are NOT OK")
        print("Auxiliary bomb exploded. Team morale is at an all-time low.")


# ===== Driver code ============================================================

# Program's entry point
def main():
    checkCriticalLocks()

    print("-----")

    checkAuxiliaryLocks()


# Executes code when main.py is run as a script, but not as an imported module
if __name__ == "__main__":
    main()
