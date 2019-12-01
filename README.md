# Data Science Ontology

[![Build Status](https://github.com/IBM/datascienceontology/workflows/Build%2C%20validate%2C%20and%20publish%20if%20on%20master/badge.svg)](https://github.com/IBM/datascienceontology/actions?query=workflow%3A%22Build%2C+validate%2C+and+publish+if+on+master%22) [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.1401676.svg)](https://doi.org/10.5281/zenodo.1401676)

The [Data Science Ontology](https://www.datascienceontology.org/) is a knowledge
base about data science that aims to:

- catalog and formalize the concepts of data science
- semantically annotate popular software packages for data science
- power new AI assistants for data scientists

To learn more about the Data Science Ontology,
[start here](https://www.datascienceontology.org/help).

The Data Science Ontology is young but growing! We welcome contributions of 
concepts and annotations.
[Learn how to contribute](https://www.datascienceontology.org/help/contribute).
For improvements to the web frontend, please visit the dedicated frontend
[repository](https://github.com/IBM/datascienceontology-frontend).

## Uploading to a CouchDB database

The following steps assume using the [IBM Cloud free tier], but can be adjusted
to other CouchDB services.

1. [Create a Cloudant resource](https://cloud.ibm.com/catalog/services/cloudant).
2. On the Service Details page, choose **Launch Cloudant Dashboard**.
3. On the Databases page, choose **Create Database**.
4. Name your database `data-science-ontology`, choose **Non-partitioned** and
   choose **Create**.
5. On the Account page, under the Settings tab, copy the External Endpoint
   (preferred) value, and assign it to the `COUCH_URL` environment variable
   (note: do not use a trailing slash).
6. Use [IAM] to set up an API key and assign it to the `IAM_API_KEY` environment
   variable.
7. Run `npm run upload`.

If you want to re-run step 7 after a new build, run `npm run clean-couchdb`
first. Note that this removes all non-design documents from your database.

[IBM Cloud free tier]: https://www.ibm.com/cloud/free/
[IAM]: https://cloud.ibm.com/iam/overview
