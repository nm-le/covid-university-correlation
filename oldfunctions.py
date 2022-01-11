def creating_covid_dic(uni: University) -> dict:
    """Returns a dictionary mapping the amount of COVID-cases to a day."""
    with open('Datasets/Ontario_Covid_Dataset.csv', encoding="utf-8") as covid_data:
        csv_reader = csv.reader(covid_data)

        dates = []
        covid_cases = []

        for row in csv_reader:
            date = row[1]
            if date != 'Accurate_Episode_Date':  # to forcefully ignore first line
                case_latitude = row[16]
                case_longitude = row[17]

                # convert date to days since march 20, 2020
                dt_object = datetime.datetime.strptime(date, "%Y-%m-%d").date()
                delta = dt_object - INITIAL_DATE

                # Starts counting covid cases since March 20th, 2020
                if delta.days >= 0:
                    uni_latitude = uni.location[0]
                    uni_longitude = uni.location[1]
                    
                    # If university is within range, add the values to that specific university's lists.
                    if within_range(float(case_latitude), float(case_longitude), uni_latitude, uni_longitude, RADIUS):
                        if delta.days not in dates:
                            dates.append(delta.days)
                            covid_cases.append(1)
                        else:
                            index = dates.index(delta.days)
                            covid_cases[index] += 1
                            

        # return file in dictionary format for convenient use in visualization
        return {date: covid_cases for date, covid_cases in zip(dates, covid_cases)}
    
    
def creating_impact_dic(uni: University) -> dict:
    """Creates an impact dic for a singular university

    #     Processes all universities' tweets to only retain useful data. We do this by:
#         1. Keeping only columns 'tweet', 'created_at' and 'name'
#         2. Removing all tweets that do not mention 'COVID' or 'covid' 
#         3. Only keeping tweets that have an impact score of at least 1
#         4. Converting the date from a YYYY-MM-DD format to an integer        representing days since March 20, 2020
    """
    with open(uni.tweet_csv_path, encoding="utf-8") as f:
        csv_reader = csv.reader(f)

        impact_dic = {}

        # iterate throught each row, which includes date, tweet, and hashtag
        for row in csv_reader:
            tweet = row[10]
            hashtag = row[18]

            # Check if the word covid is in the tweet
            if 'COVID' or 'covid' in tweet:
                date = row[3]


                # call calculate_impact_score() to calculate impact score
                impact_score = calculate_impact_score(tweet, hashtag)
                if impact_score != 0:

                    # Change date in datetime object
                    dt_object = datetime.datetime.strptime(
                        date, "%Y-%m-%d").date()

                    # Calculate days since March 20th, 2020    
                    delta = dt_object - INITIAL_DATE

                    # Appending our useful values
                    if delta.days not in impact_dic:
                        impact_dic[delta.days] = impact_score
                    else:
                        impact_dic[delta.days] += impact_score
    return impact_dic