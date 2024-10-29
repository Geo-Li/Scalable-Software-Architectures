import pathlib
import sys

from configparser import ConfigParser


###################################################################
#
# configs
#
def get_configs(config_file):
    """
    Retrieves configuration information from the ini file,
    and does some sanity checks for the config params

    Parameters
    ----------
    config_file: config file name to retrieve info from

    Returns
    -------
    baseurl:
    HOST:
    """
    # check if config file exists
    if not pathlib.Path(config_file).is_file():
        print("**ERROR: config file '", config_file, "' does not exist, exiting")
        sys.exit(0)

    # setup base URL to web service:
    configur = ConfigParser()
    configur.read(config_file)
    baseurl = configur.get("client", "webservice")
    # host = configur.get("env", "host")

    # make sure baseurl does not end with /, if so remove:
    if len(baseurl) < 16:
        print("**ERROR**")
        print(
            "**ERROR: baseurl '",
            baseurl,
            "' in .ini file is empty or not nearly long enough, please fix",
        )
        sys.exit(0)

    if baseurl.startswith("https"):
        print("**ERROR**")
        print(
            "**ERROR: baseurl '",
            baseurl,
            "' in .ini file starts with https, which is not supported (use http)",
        )
        sys.exit(0)

    lastchar = baseurl[len(baseurl) - 1]
    if lastchar == "/":
        baseurl = baseurl[:-1]

    # return baseurl, host
    return baseurl
