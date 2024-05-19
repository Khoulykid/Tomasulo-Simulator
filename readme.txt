# Tomasulo's Simulator
#### This is a program that simulates Tomasulo's algorithm on some simple instructions.

##### Instructions are mentioned in the report.
## Names & IDs
Ali Elkhouly  900212679

Moaz Hafez  900214137

## Assumptions:

The user would only input capital letters.

The user would not input values outside of scope for jumps (we implemented, but did not test)
        
## What works:
All instructions, but did not test thoroughly on BEQ and RET/CALL.
All Hazards are checked and the instruction execution stals when needed

## Errors:
Did not check on all instructions thoroughly.
We seperated 2 stations for RET and CALL