# s1_preprocessor
Python package for preprocessing Sentinel-1 imagery from AWS Open Data Registry into orthorectified, calibrated geotiffs.
Includes collateral for GBDX task deployment.

This package includes two CLI tools:
*1. compile_archive.py:*

This tool will download a Sentinel-1 image from the Registry of Open Data on AWS (https://registry.opendata.aws/sentinel-1/) and compile it into the SAFE format specification (https://sentinel.esa.int/web/sentinel/user-guides/sentinel-1-sar/data-formats/safe-specification). This format is required for the data to be compatible with the ESA SNAP Toolbox and the PyroSAR Python bindings.

*2. geocode.py:*

This tool simply wraps the excellent and highly useful SNAP geocode function provided by the PyroSAR Python package (https://github.com/johntruckenbrodt/pyroSAR) into a CLI. Most of the standard inputs to the geocode function are exposed via the CLI, with the exception that most inputs requiring lists have been simplified to single text inputs, and the `gpt_exceptions` option has been removed entirely. A few inputs have also been added for convenience, including a `bbox` argument (for image subsetting) and a `utm` option for the `t_srs` input, which will automatically select a UTM zone into which the image will be project (based on the centroid of the S-1 scene). The source code for the geocode function can be found here: https://github.com/johntruckenbrodt/pyroSAR/blob/master/pyroSAR/snap/util.py#L14.

------------
## Installation

### General
#### Requirements
- ESA SNAP Executables (http://step.esa.int/main/download/snap-download/)
    - Once installed, the path to the SNAP bin subfolder must be added to your system PATH variable. e.g. `export PATH="$PATH:/Applications/snap/bin/"`
    - Configuring the path with vary by OS. For Mac and Linux, you can edit your ~/.bash_profile by adding the line above, save, then run `source ~/.bash_profile`.
- AWS account and credentials:
    - User must have AWS credentials. This can include any credentials in the standard AWS CLI credential provider chain. Credentials can also be passed directly to the geocode CLI via arguments at runtime. For more information, see: https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html#cli-quick-configuration and https://docs.aws.amazon.com/sdk-for-java/v1/developer-guide/credentials.html.

### Development
#### Requirements:
- General requirements listed above
- Anaconda or Miniconda

#### To set up your local development environment:
This will install the s1_preprocessor package from the local repo in editable mode.
Any changes to Python files within the local repo should immediately take effect in this environment.

1. Clone the repo
`git clone https://github.com/GeoBigData/s1_processor.git`

2. Move into the local repo
`cd s1_preprocessor`

3. Create conda virtual environment
`conda env create -f environment.yml`

4. Activate the environment
`source activate s1_preprocessor`

5. Install Python package
`pip install -r requirements_dev.txt`

### Common Issues:
- TBD
