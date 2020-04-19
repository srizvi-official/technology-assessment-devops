#!/usr/bin/env python
"""
Validates that all the needed fields are present and fails the build if not
"""
import os
import json

import boto3
import botocore
import yaml


PIPELINES_FILE = 'pipelines.yml'
PIPELINES_FILE_JSON = 'pipelines.json'
PIPELINES_STATE_LOCAL_FILE = 'pipelines_state.json'
MANDATORY_FIELDS = {'pipeline', 'service', 'repo', 'path', 'product', 'domain'}
WARN_FIELDS = {'product', 'domain'}
TEMPORARY_FIELDS = {'serviceName'}
ALL_FIELDS = MANDATORY_FIELDS | TEMPORARY_FIELDS | WARN_FIELDS
PRODUCT_OPTIONS = {'yourAccount-1', 'yourAccount-2', 'yourAccount-3', 'yourAccount-4', 'DevOps'}
PIPELINES_STATE_BUCKET_NAME = 'cicd-pipelines-state'
PIPELINES_STATE_S3_KEY= 'pipelines.json'
CONFLUENCE_DEBUG_PAGE = 'link to your confluence CICD docs'
SLACK_SUPPORT_CHANNEL = 'link to your slack channel'


def download_state_from_s3():
    """ This assumes the pipelines state file from the pipeline generator
    exists in S3 and downloads the latest one.
    """
    s3_resource = boto3.resource('s3')
    print('Downloading pipelines state file from S3')
    try:
        s3_resource.Bucket(PIPELINES_STATE_BUCKET_NAME).download_file(
            PIPELINES_STATE_S3_KEY,
            PIPELINES_STATE_LOCAL_FILE,
        )
    except botocore.exceptions.ClientError as err:
        if err.response['Error']['ResponseCode'] == 404:
            print('Statefile not found on S3, nothing to check')
        else:
            print('Unexpected error: ', err.__dict__)
        raise SystemExit('Could not download state file from S3, please ask here: ', SLACK_SUPPORT_CHANNEL)
    else:
        print('State file download: SUCCESS!')
        return True


def get_pipelines_as_set(pipelines_list):
    """ Converts a pipeline from dictionary into a set
    for easier diff computing
    """
    return {tuple(sorted(item for item in pipeline.items() if item[0] in ALL_FIELDS)) for pipeline in pipelines_list}


def get_state_from_s3():
    """ Parses the state file downloaded from S3 into a python
    dictionary and returns it as a set of tuples for easier computing
    """
    print('Parsing state file...')
    with open(PIPELINES_STATE_LOCAL_FILE, 'r') as remote_state:
        try:
            remote_pipelines = json.load(remote_state)
        except json.JSONDecodeError:
            raise SystemExit('Corrupt JSON syntax on downloaded state file, please ask here: ', SLACK_SUPPORT_CHANNEL)
        else:
            print('DONE!')
            return get_pipelines_as_set(remote_pipelines['pipelines'])


def parse_pipelines_file():
    """ Parses the current pipelines.yml into a dictionary and
    returns it as a set of tuples for easier computing
    """
    print('Parsing local pipeline registry')
    with open(PIPELINES_FILE, 'r') as pipelines_stream:
        pipelines_file = yaml.load(pipelines_stream)

    print('DONE!')
    return get_pipelines_as_set(pipelines_file['pipelines'])


def get_pipelines_to_check():
    """ Computes the difference between the pipelines from the
    state file in S3 and the current pipelines.yml to know which
    pipelines we need to check the declaration is valid or not
    """
    download_state_from_s3()
    current_pipelines = parse_pipelines_file()
    old_pipelines = get_state_from_s3()
    print('Computing diff...')
    pipelines_to_check = current_pipelines - old_pipelines
    return pipelines_to_check


def check_pipeline(pipeline):
    """ Checks if the given pipeline is contract compliant
    by making sure the needed fields are present
    """
    pipeline_fields = set(pipeline.keys())
    mandatory = MANDATORY_FIELDS - pipeline_fields
    warn = WARN_FIELDS - pipeline_fields
    tmp = TEMPORARY_FIELDS - pipeline_fields
    repo_in_phab = check_repo_in_phab(pipeline)
    http_protocol = check_repo_url_protocol(pipeline)


    if tmp:
        print('Warning: These fields are needed for reporting purposes, please add them to your pipeline', tmp)
    if warn:
        print('Warning: These fields are going to be required soon, please add them to your pipeline', warn)
    if mandatory:
        return {'message': 'ERROR: These fields are mandatory, pleasee add them to your pipeline {}'.format(mandatory)}
    if repo_in_phab:
        return {'message': 'ERROR: {} repo must not be in phabricator'.format(pipeline['pipeline'])}
    if http_protocol:
        return {'message': 'ERROR {} repo url protocol must be ssh'.format(pipeline['pipeline'])}


def check_repo_in_phab(pipeline):
    """ Checks if the repo is hosted in phabricator.
    We are moving away from it so no new repos should be created
    """
    repo = pipeline['repo']
    return repo.startswith('ssh://any-name@vault.phacility.com')


def check_repo_url_protocol(pipeline):
    """ We''ve had issues with http pipelines, so, we enforce
    ssh to be used, we must fail the pipeline if the repo is not
    using ssh.

    This should be moved to an OPA policy once we get it working
    """
    repo = pipeline['repo']
    return repo.startswith('https://') or repo.startswith('http://')


def validate_pipelines():
    """ Validates that the modified or added pipelines are valid
    otherwise it exits with an error
    """
    pipelines_to_check = get_pipelines_to_check()
    offending_pipelines = []

    print('Checking pipelines:\n', pipelines_to_check)
    for pipeline in pipelines_to_check:
        pipeline_dict = {key: value for key, value in pipeline}
        error_message = check_pipeline(pipeline_dict)
        if error_message:
            pipeline_dict.update(error_message)
            offending_pipelines.append(pipeline_dict)

    if offending_pipelines:
        for pipeline in offending_pipelines:
            print(pipeline['pipeline'], pipeline['message'])

        raise SystemExit('I\'ve found some errors, perhaps you can find answers here: ', CONFLUENCE_DEBUG_PAGE)

    print('All good')
    

if __name__ == '__main__':
    validate_pipelines()
