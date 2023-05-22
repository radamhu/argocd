import os
import io
import requests
import sys
import argparse
import pandas as pd
from fuzzywuzzy import process
from edc_client import edcSessionHelper
from lut import lut
from azure.storage.blob import BlobClient,BlobServiceClient,ContentSettings

# TODO: disable warning
# see: https://stackoverflow.com/questions/27981545/suppress-insecurerequestwarning-unverified-https-request-is-being-made-in-pytho
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

edcHelper = edcSessionHelper.EDCSession()
parser = argparse.ArgumentParser(parents=[edcHelper.argparser])
parser.add_argument(
    "-o",
    "--outDir",
    required=False,
    default='./.temp/',
    help=(
        "output folder to write results - default = ./out "
        " - will create folder if it does not exist"
    ),
)
parser.add_argument(
    "-sn",
    "--sheet_name",
    required=True,
    help=(
        "lookup sheet name"
    ),
)
parser.add_argument(
    "-f",
    "--force",
    required=False,
    default=False,
    help=(
        "force to re-generate the cached downloaded EDC information."
    ),
)

def main(args):
    args = parser.parse_args(args)

    # setup edc session and catalog url - with auth in the session header,
    # by using system vars or command-line args
    edcHelper.initUrlAndSessionFromEDCSettings(args)
    edcHelper.validateConnection()
    print(f"EDC version: {edcHelper.edcversion_str} ## {edcHelper.edcversion}\n")

    print(f"command-line args parsed = {args}\n")
    
    if args.outDir is not None:
        outFolder = args.outDir
        outFolder = os.path.join(outFolder, os.path.splitext(os.path.basename(__file__))[0])
        print(f"new out folder={outFolder}\n")

    if not os.path.exists(outFolder):
        os.makedirs(outFolder)
    
    # https://thats-it-code.com/azure/azure-blob-storage-operation-using-python/
    try:
        connectionstring="DefaultEndpointsProtocol=https;AccountName=czag01r235wetzdpdat9489;AccountKey=Bp3DW8eqQt45C3SLqh6K7KEu/4h3zABmmwyVzFFq/trddvQx+f2k4dhM6Kahi/SFm5jEG4X1GpT/+AStychACg==;EndpointSuffix=core.windows.net" 
        excelcontainer = "catalog-scripts"        
        excelblobname ="EDC_LINEAGE.xlsx" 
        blob_service_client = BlobServiceClient.from_connection_string(connectionstring)
        container_client = blob_service_client.get_container_client(container=excelcontainer)
        blob_client = container_client.get_blob_client(blob=excelblobname)
        blob_client.download_blob().readall() 
        print(f'Downloading {excelblobname} blob ... \n')
        with open(f"./edc_lineage/{excelblobname}", mode="wb") as download_file:
            download_file.write(container_client.download_blob(blob=excelblobname).readall())
    except Exception as e:
        print("Failed to get the blob in the container. Error:" + str(e))
    
    get_mapping(outFolder, args.sheet_name, args.force)


def get_mapping(
    outFolder: str,
    sheet_name: str,
    force: bool = False
):
    df = lut(sheet_name)

    if df.empty:
        print('Mapping reference file is not available.')
        print('Please copy the file to the edc_lineage folder and rename it as EDC_LINEAGE.xlsx')
        print('Processing is interrupted...')
        return

    all_source_resource_fields = []
    all_target_resource_fields = []

    tmp_all_source_resource_fields = outFolder + "/all_source_resource_fields.xlsx"
    tmp_all_target_resource_fields = outFolder + "/all_target_resource_fields.xlsx"

    # check cache...
    if os.path.exists(tmp_all_source_resource_fields):
        print(f'using cache {tmp_all_source_resource_fields}')
        all_source_resource_fields = pd.read_excel(tmp_all_source_resource_fields, sheet_name='all_source_resource_fields')
    
    if os.path.exists(tmp_all_target_resource_fields):
        print(f'using cache {tmp_all_target_resource_fields}')
        all_target_resource_fields = pd.read_excel(tmp_all_target_resource_fields, sheet_name='all_target_resource_fields')

    #if not all_source_resource_fields or all_target_resource_fields:
    #    force = False

    force = True

    if force:
        print(f'ignore cache. generate the temp files...\n')

        all_source_resource_fields = []
        all_target_resource_fields = []

        for index, row in df.iterrows():
            source_resource = row['FROM RESOURCE'].strip()
            source_table = row['FROM TABLE'].strip()
            target_resource = row['TO RESOURCE'].strip()
            target_table = row['TO TABLE'].strip()

            edc_source_table = get_dataset_by_name(source_resource, source_table)
            edc_target_table = get_dataset_by_name(target_resource, target_table)

            if not edc_source_table or not edc_target_table:
                print(f'source_table: \033[1m{source_table}\033[0m IN source_resource : {source_resource} \n',
                      'OR \n', 
                      f'target_table: \033[1m{target_table}\033[0m IN target_resource : {target_resource} \n',
                      'not exists in edc... \n')
                
                continue

            edc_source_table_fields = get_dataset_field_by_dataset_name(source_resource, source_table)
            edc_target_table_fields = get_dataset_field_by_dataset_name(target_resource, target_table)

            all_source_resource_fields.extend(edc_source_table_fields)
            all_target_resource_fields.extend(edc_target_table_fields)

        all_source_resource_fields = pd.DataFrame(all_source_resource_fields)
        all_source_resource_fields.to_excel(outFolder + "/all_source_resource_fields.xlsx", sheet_name='all_source_resource_fields', index=False)

        all_target_resource_fields = pd.DataFrame(all_target_resource_fields)
        all_target_resource_fields.to_excel(outFolder + "/all_target_resource_fields.xlsx", sheet_name='all_target_resource_fields', index=False)

    mapping_table_matched = pd.DataFrame()

    for index, row in df.iterrows():
        source_table = row['FROM TABLE'].strip()
        target_table = row['TO TABLE'].strip()

        print(f'source_table  \033[1m{source_table}\033[0m -  target_table \033[1m{target_table}\033[0m')
        
        edc_current_source_table_fields = all_source_resource_fields[all_source_resource_fields['dataset_name'] == source_table].copy()
        edc_current_target_table_fields = all_target_resource_fields[all_target_resource_fields['dataset_name'] == target_table].copy()

        edc_current_target_table_fields_matched = []
        similarity = []

        source_dataset_id = None
        target_dataset_id = None

        for i in edc_current_source_table_fields.name:

            if not source_dataset_id:
                source_dataset_id = edc_current_source_table_fields.iloc[0]['dataset_id']
            
            if not target_dataset_id:
                target_dataset_id = edc_current_target_table_fields.iloc[0]['dataset_id']

            ratio = process.extract(i, edc_current_target_table_fields.name, limit=1)
            edc_current_target_table_fields_matched.append(edc_current_target_table_fields.loc[ratio[0][2]]['id'])
            similarity.append(ratio[0][1])

            edc_current_source_table_fields['dataset_id'] = source_dataset_id
            edc_current_source_table_fields['target_dataset_id'] = target_dataset_id

        edc_current_source_table_fields['target_id'] = edc_current_target_table_fields_matched
        edc_current_source_table_fields['similarity'] = similarity
        
        mapping_table_matched = pd.concat([mapping_table_matched, edc_current_source_table_fields])

    print('saving mapping.xlsx ...')
    df = pd.DataFrame(mapping_table_matched)
    df.to_excel(outFolder + "/mapping.xlsx", sheet_name='mapping', index=False)
    
    # TODO: fixed code matching threshold 90
    mapping_table_matched = mapping_table_matched[mapping_table_matched['similarity'] > 90]

    print('saving mapping_filtered.xlsx ...')
    df = pd.DataFrame(mapping_table_matched)
    df.to_excel(outFolder + "/mapping_filtered.xlsx", sheet_name='mapping_filtered', index=False)

    convert_mapping_to_csv(df, outFolder)


def convert_mapping_to_csv(df: pd.DataFrame, outFolder: str):

    df_csv = pd.DataFrame(columns=['Association','From Connection','To Connection','From Object', 'To Object'])
    df_csv['From Object'] = df['id'].values
    df_csv['To Object'] = df['target_id'].values
    df_csv.loc[:, 'Association'] = 'core.DirectionalDataFlow'

    # add dataset
    df_csv_tmp = pd.DataFrame(columns=df_csv.columns)
    df_csv_tmp['From Object'] = df['dataset_id'].values
    df_csv_tmp['To Object'] = df['target_dataset_id'].values
    df_csv_tmp.loc[:, 'Association'] = 'core.DataSetDataFlow'
    df_csv_tmp = df_csv_tmp.drop_duplicates(subset=['From Object', 'To Object'])

    print('saving mapping.csv ...')
    df_csv = pd.concat([df_csv_tmp, df_csv])
    df_csv.to_csv(outFolder + "/mapping.csv", index=False)


def get_dataset_field_by_dataset_name(
    resource_name: str, dataset_name: str
):
    ret = get_dataset_by_name(resource_name, dataset_name)

    if not ret:
        print(f'dataset not found {resource_name} : {dataset_name}')
        return None

    if resource_name == 'evaweprddls_ingress_all':        
        dataset_class = 'com.infa.ldm.file.parquet.PARQUETField'
    elif resource_name == 'synapse_evaprdsynspallservice':
        dataset_class = 'com.infa.ldm.relational.Column'
    else:
        print(f'unknown data source given in this lineage pipeline: {resource_name}')
        return

    queryurl = f"{edcHelper.baseUrl}/access/2/catalog/data/objects"
    queryid = '*/' + ret.get('id').rsplit('/', 1)[1] + '/*'
    params = {
        "includeSrcLinks": "false",
        'includeDstLinks': "false",
        "includeRefObjects": "false",
        "pageSize": 500,
        "q": f"core.resourceName:(\"{resource_name}\") AND core.classType:(\"{dataset_class}\")",
        "fq": f"id:{queryid}"
    }
    print(f'def get_dataset_field_by_dataset_name: \033[1m{resource_name}\033[0m - \033[1m{dataset_name}\033[0m via api...')

    dataset_id = ret.get('id')
    
    try:
        resp = edcHelper.session.get(queryurl, params=params)

        if resp.status_code == 200:
            ret = resp.json()

            print(f"\t total query fields: {ret.get('metadata').get('totalCount')}")

            queryfields = []

            for item in ret.get('items'):
                fieldid = item.get('id')
                fieldname = None

                for attr in item.get('facts'):
                    if attr.get('attributeId') == 'core.name':
                        fieldname = attr.get('value')
                
                queryfields.append({
                    'dataset_name': dataset_name,
                    'dataset_id': dataset_id,
                    'id': fieldid,
                    'name': fieldname
                })
            
            return queryfields

        else:
            print(
                f"api call returned non 200 status_code: {resp.status_code} "
                f" {resp.text}"
            )
    except requests.exceptions.RequestException as e:
        print("Exception raised when executing edc query: " + queryurl)
        print(e)


def get_dataset_by_name(
    resource_name: str, dataset_name: str
):
    if resource_name == 'evaweprddls_ingress_all':        
        dataset_class = 'com.infa.ldm.file.parquet.PARQUETFile'
    elif resource_name == 'synapse_evaprdsynspallservice':
        dataset_class = 'com.infa.ldm.relational.Table'
    else:
        print(f'unknown data source given in this lineage pipeline: {resource_name}')
        return

    queryurl = f"{edcHelper.baseUrl}/access/2/catalog/data/objects"
    params = {
        "includeSrcLinks": "false",
        'includeDstLinks': "false",
        'includeRefObjects': 'false',
        "q": f"core.resourceName:(\"{resource_name}\") AND core.classType:(\"{dataset_class}\") AND core.name:{dataset_name}"
    }
    print(f'def get_dataset_by_name: resource_name = \033[1m{resource_name}\033[0m - dataset_name = \033[1m{dataset_name}\033[0m via api...')
    
    try:
        resp = edcHelper.session.get(queryurl, params=params)
        
        if resp.status_code == 200:
            ret = resp.json()
            print(f"\t total results {ret.get('metadata').get('totalCount')} ")
            items = ret.get('items')
            id = None

            for item in items:
                for fact in item['facts']:
                    if fact["attributeId"] == "core.name" and fact['value'] == dataset_name:
                        id = item['id']

            if id:
                return {
                    'name': dataset_name,
                    'id': id
                }
            else:
                return None
        else:
            print(
                f"api call returned non 200 status_code: {resp.status_code} "
                f" {resp.text}"
            )

    except requests.exceptions.RequestException as e:
        print("Exception raised when executing edc query: " + queryurl)
        print(e)


# call main - if not already called or used by another script
if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
