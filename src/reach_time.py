from datetime import datetime, timedelta


def give_default_dates():
    # get date one day ago
    currentDateAndTime = datetime.now() - timedelta(days = 1)
    # get date 1 day and 5 mins. ago
    current_minus_5_min = datetime.now() - timedelta(minutes = 5) - timedelta(days = 1)

    # turn date into string
    start = str(currentDateAndTime.date())
    # turn date into the format which is used on url
    start = start + "T"
    start = start + str(currentDateAndTime.time())[0:12] + "Z"
    
    # turn end date into string
    end = str(current_minus_5_min.date())
    # turn end date into the format which is used on url
    end = end + "T"
    end = end + str(current_minus_5_min.time())[0:12] + "Z"
    
    # return processed dates
    return start, end


# 2023-02-21T10:59:25.479Z
# Output: The current date and time is 2022-03-19 10:05:39.482383
