import pandas as pd
import os

def lut(sheet_name: str, path: str = None) -> pd.DataFrame:

    if not path:
        path = os.path.dirname(os.path.abspath(__file__)) + '/EDC_LINEAGE.xlsx'

        print(f'EDC_LINEAGE.xlsx PATH here: {path} \n')

    if not os.path.exists(path):
        print('mapping file not found: {path}')
        return

    df = pd.read_excel(path, sheet_name=sheet_name, header=None)
    from_resource = df.at[2, 1]
    to_resource = df.at[2, 2]

    print(f'from {from_resource} to {to_resource}\n')

    for row in range(df.shape[0]): 
       for col in range(df.shape[1]):

           if df.iat[row,col] == 'FROM TABLE':
             row_start = row
             break
    
    df_required = df.loc[row_start + 1:]

    df = pd.DataFrame(columns=['FROM RESOURCE', 'FROM TABLE', 'TO RESOURCE', 'TO TABLE'])
    df['FROM TABLE'] = df_required[df_required.columns[1]].values
    df['TO TABLE'] = df_required[df_required.columns[2]].values
    df.loc[:, 'FROM RESOURCE'] = from_resource
    df.loc[:, 'TO RESOURCE'] = to_resource

    return df
