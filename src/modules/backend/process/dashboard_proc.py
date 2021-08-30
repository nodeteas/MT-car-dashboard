#!/usr/bin/python

"""
Contains main methods for running each job.

"""

from bs4 import BeautifulSoup
import requests

from backend.utility_ops.anc_utility import check_pagination, retrieve_vehicles
from backend.utility_ops.utility import check_path, write_to_log


def web_scraping_proc(job_name="Car Web-Scraper",
                dataset_dir="ancira_dataset/",
                all_used_dataset="ancira_car_listing.csv",
                mt_dataset="ancira_manual_cars.csv"):
    """
	Web scraper that pulls data and creates a dataset to track manual transmission and automatic transmission cars.

	PARAMETERS
		job_name : str
			Name of the process or job
		dataset_dir : str
		    directory or name of folder to save the dataset
		all_used_dataset : str
		    name of the csv file to save all used vehicles
		mt_dataset : str
		    name of the csv file to save manual transmission vehicles

	RETURNS
		Nothing
	"""

    write_to_log(msg=f"Now starting {job_name} process")

    domain = 'https://www.ancira.com'
    home_link = '/used-car-truck-suv-for-sale-san-antonio-tx.html?pn=100'  # subquery
    home_url = domain + home_link

    write_to_log(msg=f"Requesting {home_url}")
    res = requests.get(home_url)
    write_to_log(msg=f"Request message - {res}")

    write_to_log(msg=f"Getting content using BeautifulSoup")
    soup = BeautifulSoup(res.content, 'lxml')

    write_to_log(msg=f"Checking pagination links")
    page_list = check_pagination(soup, home_link)

    # all cars no matter the transmission
    write_to_log(msg=f"Retrieving vehicle information")
    veh_df = retrieve_vehicles(page_list, domain)

    write_to_log(msg=f"{veh_df.shape[0]} rows retrieved.")
    write_to_log(msg=f"{veh_df.shape[1]} columns retrieved.")
    write_to_log(msg=f"Column names are {veh_df.columns}")

    check_path(dataset_dir)
    dataset_path = dataset_dir + all_used_dataset
    veh_df.to_csv(dataset_path, index=False)
    write_to_log(msg=f"{veh_df.shape[0]} rows saved.")
    write_to_log(msg=f"{veh_df.shape[1]} columns saved.")

    # manual transmission cars only
    write_to_log(msg=f"Retrieving manual transmission data")
    mt_vehicles = veh_df[veh_df["transmission"].str.lower() == "manual"]

    write_to_log(msg=f"{mt_vehicles.shape[0]} rows retrieved.")
    write_to_log(msg=f"{mt_vehicles.shape[1]} columns retrieved.")
    write_to_log(msg=f"Column names are {mt_vehicles.columns}")

    dataset_path = dataset_dir + mt_dataset
    mt_vehicles.to_csv(dataset_path, index=False)
    write_to_log(msg=f"{mt_vehicles.shape[0]} rows saved.")
    write_to_log(msg=f"{mt_vehicles.shape[1]} columns saved.")

    write_to_log(msg=f"Process finished running! \n")