import csv


def summarizeResult(outputOfTheT1Algo):
    # outputOfTheT1Algo = list -> each item in the list is a dictonary that looks something like:
    # {'timeItTookForDriverToGetToPassenger': 0.06343763989668617, 'timeItTookFromPickupToDropoff': 0.1664803757009768, 'timeItTookForPassengerToGoFromUnmatchedToDroppedOff': 0.2321906828198852}

    # things to aggregate/summarize:
    # D1 = minimize the amount of time (in minutes) between when they appear as an unmatched passenger, and when they are dropped off at their destination.
    D1list = []



    # D2 = Drivers want to maximize ride profit, defined as the number of minutes they spend driving passengers from pickup to drop-off locations minus the number of minutes they spend driving to pickup passengers
    # so, when D2 is NEGATIVE, that means driver took longer to get to the pick-up location than it took to drive the passenger in their car
    D2list = []


    for item in outputOfTheT1Algo:
        D1list.append(item['timeItTookForPassengerToGoFromUnmatchedToDroppedOff'] * 60) # converting to minutes
        D2list.append((item['timeItTookFromPickupToDropoff'] - item['timeItTookForDriverToGetToPassenger']) * 60) # converting to minutes

    with open('T1_summary.csv', 'w', newline='') as file:
        writer = csv.writer(file)

        # Write headers
        writer.writerow(['D1: timeItTookForPassengerToGoFromUnmatchedToDroppedOff (mins)', 
                         'D2: number of minutes they spend driving passengers from pickup to drop-off locations minus the number of minutes they spend driving to pickup passengers'])

         # Write data rows
        for d1, d2 in zip(D1list, D2list):
            writer.writerow([d1, d2])