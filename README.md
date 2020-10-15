# Natural Language on Google

Code repository and documentation for Pandera's Natural Language on Google Guide

## Implementation

This guide will be done within the Google Cloud Platform. Please follow along with the following steps on GCP.

### Setting up EDA

The raw csv files for EDA can be downloaded from [this archive](https://drive.google.com/file/d/1O09vZzsDXGM3NexEOEvU5xLVEvQEtUH7/view?usp=sharing) . The notebooks are configured to read these csv files from Cloud Storage, as it is best practice to separate storage and compute, but can be adapted to read from a directory with minor code modifications.

### Training the Model

Within the Artificial Intelligence section of the product list navigation menu, select Natural Language to be brought to the list of Google's Natural Language offerings. Select 'Get started' on AutoML Text & Document Classification. Create a new dataset for multi-label classification and either upload the provided csv file, `TrainingDataLabeled.csv`, which can be found in /src/data/, or designate its location within cloud storage.

After the import is completed, navigate to the train tab and press 'Train' to begin model training. When finished, evaluation metrics can be reviewed within the Evaluate tab. Deploy the model from the Test & Use tab by clicking the 'Deploy Model' button. Take note of the model name.

### Setting up Cloud Functions

From the navigation menu, in the compute section, select Cloud Functions. Create a new function of type HTTP Trigger and allow unauthenticated invocations. After saving, press next to proceed to the next page, where from the dropdown menu 'Source Code', select Zip Upload or Zip from Cloud Storage. The zip to upload is `yelp-cloud-function-1.zip` which can be found in /cloud-funtions/ along with the rest of the functions for this demo. Edit the project id references within the code to match your project. Check the files for the comment: Developer: Edit Here, which can be found above lines that need to be edited to match your project. In addition, change the entry point for the cloud function to `scrape_and_clean`, as this will be the function that is ran within the script, and the runtime to Python 3.7.

This first cloud function scrapes Yelp for restaurant reviews, and preprocesses the data such that it is ready for ML processing. This requires an API key to do, and you must recieve an API key from Yelp. The easiest way to integrate your API key into the code is to set api_key within `CUSTOMFUNCTIONS.PY` to your API key string, though this is very unsecure. In this demo, we've enabled Google's Secret Manager API and masked our API key with it. 

While the first function is triggered by an HTTP request, the following 2 cloud functions are triggered via pub/sub. We need to create the topics for these following functions, so enable the Cloud Pub/Sub API. Within the Big Data group of the navigation menu, open Pub/Sub Topics. Create two topics: `yelp-sentiment-analysis` and `yelp-classification`, with Google-managed keys.

Back within Cloud Functions, create another function and upload the second zip file, `yelp-cloud-function-2.zip`. This time, select the trigger to be Pub/Sub, and the topic as `yelp-sentiment-analysis` with an entry point set to `process_sentiment` and a runtime of Python 3.7. Again, edit the appropriate, designated lines to match your project information. Follow a similar process for the third function, but with the triggering topic set to `yelp-classification`, and the entry point set as `classifier`. Additionally, expand the variables, networking and advanced setting drop-down, and increase the allocated memory to 2 GiB. This third demo requires that the model name and project id be adjusted to reflect your deployed model from earlier. Adjust the appropriate lines within `MAIN.PY` to reflect the location of your deployed model and your project.

With the URL based off of your first function name, you can trigger the jobs using HTTP requests.

The an example body of the request is:

```
{
    "zip": "10001"
}
```


Submit the HTTP request, and the Cloud Function will kick-off the data preprocessing, the sentiment analysis, and the classification for the specified zipcode, culminating in an update to your BigQuery table.

Congratulations!
