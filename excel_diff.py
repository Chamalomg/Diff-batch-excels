import os

import numpy as np
import pandas as pd

main_dir = "D:\Documents\Programmes\pour_papa\data"
output_dir = "D:\Documents\Programmes\pour_papa\diff"
file1 = "data/PNI_PEL_juridiction=2008=20210531.xls"
file2 = "data/PNI_PEL_juridiction=2016=20210531.xls"


# file1 = "data/test1.xls"
# file2 = "data/test2.xls"

# df1 = pd.read_excel(file1, index_col=None, header=None)
# df2 = pd.read_excel(file2, index_col=None, header=None)


def diff_pd(df1, df2):
    """Identify differences between two pandas DataFrames"""
    if df2.equals(df1):
        return None
    assert (df1.columns == df2.columns).all(), \
        "DataFrame column names are different"
    if any(df1.dtypes != df2.dtypes):
        "Data Types are different, trying to convert"
        df2 = df2.astype(df1.dtypes)
    else:
        # need to account for np.nan != np.nan returning True
        diff_mask = (df1 != df2) & ~(df1.isnull() & df2.isnull())
        ne_stacked = diff_mask.stack()
        changed = ne_stacked[ne_stacked]
        print(changed)
        print(changed.to_frame(name='A'))
        changed.index.names = ['ligne', 'col']
        difference_locations = np.where(diff_mask)
        changed_from = df1.values[difference_locations]
        changed_to = df2.values[difference_locations]
        df = pd.DataFrame({'from': changed_from, 'to': changed_to},
                          index=changed.index)
        changes = changed.to_frame(name='A').axes
        df['changed'] = changes
        return df


def diff_path(file1, file2):
    df1 = pd.read_excel(file1, index_col=None, header=None)
    df2 = pd.read_excel(file2, index_col=None, header=None)
    return diff_pd(df1, df2)


def create_csv(df, output_dir, name):
    path = output_dir + "\\" + name + ".csv"
    df.to_csv(path, index=False, header=True)


def create_pairs(main_dir):
    paths = []
    for root, dirs, files in os.walk(main_dir):
        for f_name in files:
            if ".xls" in f_name:
                path = os.path.join(root, f_name)
                paths.append(path)
    paths.sort()
    pairs = [[paths[i], paths[i + 1]] for i in range(0, len(paths), 2)]
    return pairs


def main():
    pairs = create_pairs(main_dir)
    for f1, f2 in pairs:
        # print(f1, f2, "\n")
        diff = diff_path(f1, f2)
        if diff is not None:
            # print(diff)
            create_csv(diff, output_dir, f1.split("\\")[-1].split(".")[0])
        else:
            print("no diff")


main()
print("finished")
# diff = pd.concat([df1, df2]).drop_duplicates(keep=False)
# fdiff = diff_pd(df1, df2)
# print(fdiff)
