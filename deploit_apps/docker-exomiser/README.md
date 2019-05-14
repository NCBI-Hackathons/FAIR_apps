# Exomiser 

## Exomiser -> container -> pipeline -> Run at your peril

### Containarizing Exomiser

Containarization provides a solution to isolate all software dependencies and make an aplication / workflow  reproducible.

In order to containirize Exomiser we started from a Docker base image with Ubuntu and Java8, which is the main dependency for Exomiser to be able to run.

The container pulls the latest publicly available release of `Exomiser v12.0.0` from Github releases, and unzips it inside the container. Modifications to the application property are included to match the genome reference data used for running exomiser. The version selecter for the container is `1811`.

Latest version of exomiser accept parameters and configuration from a YAML file. This YAML file defines input such as VCF files, reference genome version, HPO terms and other parameter configuration. In order to create a directly executable application for Exomiser, without the need to write beforehand the YAML file, we added a `Python` handle script that just do that.

The `Python` script `run.py` takes care of:
* Getting Exomiser input parameters from command line
* Create a YAML file from a template and updating it given parameters received
* Run Exomiser with the YAML file just created

The script also takes care of handling the pointer to the genome reference dataset used for running Exomiser. 

Since reference data is quite large, doesn't make much sense to include it in the container, as it would turn into a +50 GB image...

Instead the fetching of the data, which includes:
* VCF
* Reference Exomiser genome dataset

Will be taken care by a simple Nextflow pipeline.

## Containarized Exomiser pipeline

In order to run Exomiser with a VCF file, reference genome datasets have to be fetched and unzipped for Exomiser to run. We separated the data and file staging part from the container into a pipeline (Nextflow) which will take care of pulling the data into the working directory for Exomiser to run successfully.

The reference dataset has been added as a parameter, allowing flexibility to pull the data from any resource (i.e. cloud, local storage, ftp, ...) and Nextlfow pipeline will automatically take care of fetching the data without having to add any logic to Exomiser process/script.