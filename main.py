from DataFetcher import generate_csv

if __name__ == "__main__":
    for year in range(2013, 2023):
        for month in range(1, 13):
            generate_csv(month, year)
            print("Finished creating the CSV files for month " + str(month) + " of year " + str(year) + ".")
        print("Finished creating the CSV files for year " + str(year))
    print("Finished creating the CSV files")
