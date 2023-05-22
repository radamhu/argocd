import os
import requests
import sys
import argparse
import pandas as pd
from edc_client import edcSessionHelper

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
    help=(
        "output folder to write results - default = ./out "
        " - will create folder if it does not exist"
    ),
)
parser.add_argument(
    "-b",
    "--sapbw",
    required=True,
    help=(
        "SAP mapping file "
    ),
)

EDC_SAPBW = 'SAP_BW'
EDC_ADLS20 = 'evaweprddls_ingress_all'

def main(args):

    outFolder = "./out"

    #args = args, unknown = parser.parse_known_args()
    args = parser.parse_args(args)

    # setup edc session and catalog url - with auth in the session header,
    # by using system vars or command-line args
    edcHelper.initUrlAndSessionFromEDCSettings(args)
    edcHelper.validateConnection()
    print(f"EDC version: {edcHelper.edcversion_str} ## {edcHelper.edcversion}")

    print(f"command-line args parsed = {args} ")
    print()

    if args.outDir is not None:
        outFolder = args.outDir
        print(f"new out folder={outFolder}")

    if not os.path.exists(outFolder):
        os.makedirs(outFolder + '/lineage_mapping__SAP_BW__evaweprddls_ingress_all/')

    get_sapbw_mapping(args.sapbw, outFolder)


def get_sapbw_mapping(
    path: str, outFolder: str
):
    import os
    if not path or not os.path.exists(path):
        path = '/Users/ZOYUAGAO/Library/CloudStorage/OneDrive-CarlZeissAG/EDM/USECASE/EVA30_USECASE/BW2DATALAKE/Book1.xlsx'

    print(f'open mapping file: {path}')

    try:
        df = pd.read_excel(path, 'XLMapping', skiprows = 6, usecols= 'B:F')
    except Exception as e:
        print('open mapping file error:')
        print(e)
        return
    
    queries = df['QUERY'].unique()

    mapping = []
    all_bw_queries = []
    all_adls_parquets = []
    
    for query in queries:
        query = str(query).strip()

        if len(query) == 0:
            print('Find an empty query... skip...')
            continue

        query_edc = get_dataset_by_name(EDC_SAPBW, query)
        adls20_edc = get_dataset_by_name(EDC_ADLS20, 'all_' + query + '.parquet')

        if not query_edc or not adls20_edc:
            print(f'given BW query or ADLS20 parquet not exists: {query}')
            continue

        queryfields_edc = get_dataset_field_by_dataset_name(EDC_SAPBW, query)
        parquetfields_edc = get_dataset_field_by_dataset_name(EDC_ADLS20, 'all_' + query + '.parquet')

        all_bw_queries.extend(queryfields_edc)
        all_adls_parquets.extend(parquetfields_edc)

        df_query = df.loc[df['QUERY'] == query]

        print(f'start processing query: {query} ...')

        for index, row in df_query.iterrows():
            fieldname = row['Wert']

            if not fieldname:
                continue

            # they have diffent nummeration ...
            numeric = list(range(2, 9))
            if fieldname[0] in [str(n) for n in numeric]:
                fieldname = fieldname[1:]

            for field in queryfields_edc:
                if str(field['name']).lower() == fieldname.lower():

                    # find datalake field

                    for adls20_field in parquetfields_edc:

                        if str(adls20_field['name']).lower() == str(row['Datalake']).lower():

                            mapping.append(
                                {
                                    'BW_QUERY_ID': query_edc['id'],
                                    'BW_QUERY_NAME': query_edc['name'],
                                    'BW_QUERYFIELD_ID': field['id'],
                                    'BW_QUERYFIELD_NAME': field['name'],
                                    'BW_QUERYFIELD_TYPE': field['datatype'],

                                    'DATALAKE_PARQUET_ID': adls20_edc['id'],
                                    'DATALAKE_PARQUET_NAME': adls20_edc['name'],
                                    'DATALAKE_PARQUETFIELD_ID': adls20_field['id'],
                                    'DATALAKE_PARQUETFIELD_NAME': adls20_field['name'],
                                    'DATALAKE_PARQUETFIELD_TYPE': adls20_field['datatype']
                                }
                            )
    
    df = pd.DataFrame(mapping)
    writer = pd.ExcelWriter(outFolder + "/mapping.xlsx", engine='xlsxwriter')
    df.to_excel(writer, sheet_name='mapping', index=False)
    writer.save()

    convert_mapping_to_csv(df, outFolder)

    df = pd.DataFrame(all_bw_queries)
    writer = pd.ExcelWriter(outFolder + "/all_bw_queries.xlsx", engine='xlsxwriter')
    df.to_excel(writer, sheet_name='all_bw_queries', index=False)
    writer.save()

    df = pd.DataFrame(all_adls_parquets)
    writer = pd.ExcelWriter(outFolder + "/all_adls_parquets.xlsx", engine='xlsxwriter')
    df.to_excel(writer, sheet_name='all_adls_parquets', index=False)
    writer.save()


def convert_mapping_to_csv(df: pd.DataFrame, outFolder: str):

    df_csv = pd.DataFrame(columns=['Association','From Connection','To Connection','From Object', 'To Object'])
    df_csv['From Object'] = df['BW_QUERYFIELD_ID'].values
    df_csv['To Object'] = df['DATALAKE_PARQUETFIELD_ID'].values
    df_csv.loc[:, 'Association'] = 'core.DirectionalDataFlow'

    # add dataset
    df_dataset = df.drop_duplicates(subset=['BW_QUERY_ID', 'DATALAKE_PARQUET_ID'], keep='first')
    df_csv_tmp = pd.DataFrame(columns=df_csv.columns)
    df_csv_tmp['From Object'] = df_dataset['BW_QUERY_ID'].values
    df_csv_tmp['To Object'] = df_dataset['DATALAKE_PARQUET_ID'].values
    df_csv_tmp.loc[:, 'Association'] = 'core.DataSetDataFlow'

    df_csv = df_csv_tmp.append(df_csv)
    df_csv.to_csv(outFolder + "/lineage_mapping__SAP_BW__evaweprddls_ingress_all.csv", index=False)


def get_dataset_field_by_dataset_name(
    resource_name: str, dataset_name: str
):
    ret = get_dataset_by_name(resource_name, dataset_name)

    if not ret:
        print(f'dataset not found {resource_name} : {dataset_name}')
        return None

    if resource_name == 'SAP_BW':
        queryparam = f"core.resourceName:(\"{resource_name}\") AND core.classType:(\"com.infa.ldm.warehouse.sapbw.QueryField\")"
    elif resource_name == 'evaweprddls_ingress_all':
        queryparam = f"core.resourceName:(\"{resource_name}\") AND core.classType:(\"com.infa.ldm.file.parquet.PARQUETField\")"

    queryurl = f"{edcHelper.baseUrl}/access/2/catalog/data/objects"
    queryid = '*/' + ret.get('id').rsplit('/', 1)[1] + '/*'
    params = {
        "includeSrcLinks": "false",
        'includeDstLinks': "false",
        "includeRefObjects": "false",
        "pageSize": 500,
        "q": queryparam,
        "fq": f"id:{queryid}"
    }
    print(f"executing query via endpoint: {queryurl} with params={params}")
    print("generate new xdocs...")
    
    try:
        resp = edcHelper.session.get(queryurl, params=params)

        if resp.status_code == 200:
            ret = resp.json()

            print(f"total query fields: {ret.get('metadata').get('totalCount')}")

            queryfields = []

            for item in ret.get('items'):
                fieldid = item.get('id')
                fieldname = None
                fielddescription = None
                fieldtype = None
                fielddisplayname = None

                for attr in item.get('facts'):
                    if attr.get('attributeId') == 'core.name':
                        fieldname = attr.get('value')
                    
                    if attr.get('attributeId') == 'core.description':
                        fielddescription = attr.get('value')
                    
                    if attr.get('attributeId') == 'com.infa.ldm.warehouse.sapbw.Type':
                        fieldtype = attr.get('value')
                    
                    if attr.get('attributeId') == 'com.infa.ldm.file.Datatype':
                        fieldtype = attr.get('value')
                    
                    if attr.get('attributeId') == 'com.infa.ldm.ootb.enrichments.displayName':
                        fielddisplayname = attr.get('value')
                
                queryfields.append({
                    'id': fieldid,
                    'name': fieldname,
                    'description': fielddescription,
                    'datatype': fieldtype,
                    'displayname': fielddisplayname
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

    # manual maintain this lookup...
    if resource_name == 'SAP_BW':
        MAPPING_TABLE = {
            'AMSD1M007_S002_BDA': 'AMSD1M007_S002'
        }

        if dataset_name in MAPPING_TABLE:
            dataset_name = MAPPING_TABLE.get(dataset_name)
        
        queryparam = f"core.resourceName:(\"{resource_name}\") AND core.classType:(\"com.infa.ldm.warehouse.sapbw.Query\") AND core.name:{dataset_name}"
    
    elif resource_name == 'evaweprddls_ingress_all':
        queryparam = f"core.resourceName:(\"{resource_name}\") AND core.classType:(\"com.infa.ldm.file.parquet.PARQUETFile\") AND core.name:{dataset_name}"

    print(f"get dataset 10.5+ version starting extract for resource={resource_name}")
    queryurl = f"{edcHelper.baseUrl}/access/2/catalog/data/objects"
    params = {
        "includeSrcLinks": "false",
        'includeDstLinks': "false",
        'includeRefObjects': 'false',
        "q": queryparam
    }
    print(f"executing query via endpoint: {queryurl} with params={params}")
    
    try:
        resp = edcHelper.session.get(queryurl, params=params)
        
        if resp.status_code == 200:
            ret = resp.json()
            print(f"total results {ret.get('metadata').get('totalCount')}")
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
