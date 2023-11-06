#from flatten_json import flatten
import json
import csv
import os
import collections.abc

def flatten_json(y):
    """_summary_
    Decription: flatten out list nested in dictionary
    Args:
        y (json): python json object

    Returns:
        dictionary: out
    """
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '_')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '_')
                i += 1
        else:
            out[name[:-1]] = x

    flatten(y)
    return out

def rearrange_data(data, folder_path, file_name):
    """_summary_
    Decription: gets file name from a path, without file extension
    Args:
        data (dictionary): python dictionary
        
        "configuration.targetResourceId": "xxxxxxxxxxxx",
        "configuration.targetResourceType": "AWS::::Account",
        "configuration.complianceType": "NON_COMPLIANT",
        "accountId": "xxxxxxxxxxxx",
        "configuration.configRuleList": [ ## can be array of dict, or just dict
            {
            "configRuleName": "s3-account-level-public-access-blocks-periodic-conformance-pack-wxpi4uvvj",
            "configRuleArn": "arn:aws:config:ap-southeast-1:xxxxxxxxxxxx:config-rule/aws-service-rule/config-conforms.amazonaws.com/config-rule-iqaoko",
            "configRuleId": "config-rule-iqaoko",
            "complianceType": "NON_COMPLIANT"
            },
        {
            
        folder_path (string): directory of folder
        
        file_name (string): output file name without extension
            
    Returns:
        -NA-
    """
    
    output_file_name = folder_path + file_name + ".csv"
    """
    
    """

    headers = ["configuration.targetResourceId", "configuration.targetResourceType","configuration.complianceType","accountId" ]
    data_headers = ["configRuleName", "configRuleArn", "configRuleId", "complianceType"]
    
    all_headers = headers + data_headers
    with open(output_file_name, 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
        
        spamwriter.writerow(all_headers)
        for d in data["results"]:
            print_arr = []
            base_arr = []
            for r in d: ## each resource
                        
                if r != "configuration.configRuleList":
                    base_arr.append(d[r])
                    
                else:
                    
                    print_arr.extend(base_arr)

                    ## check if its an array
                    if isinstance(d[r], collections.abc.Sequence):
                        for idx, c in enumerate(d[r]): ## configrulelist array
                            print_arr.extend(c.values())
                            spamwriter.writerow(print_arr)
                    else:        
                        ## when configrulelist is not an array, just a dict
                        print_arr.extend(c.values())
                        spamwriter.writerow(print_arr)
                        
                    print_arr = []
                    
                            
def get_file_name( file_path ):
    """_summary_
    Decription: gets file name from a path, without file extension
    Args:
        file_path (string): absolute path of file

    Returns:
        string: file name
    """
    base=os.path.basename(file_path)
    file_name = os.path.splitext(base)[0]

    return file_name

folder_path = "<folder_of_json>/"
folder_list = os.listdir(folder_path)

for folder in folder_list:
    ## if not a json file, skip
    if not "json" in folder:
        continue
    
    data_abs_path = folder_path + folder
    # Opening JSON file
    f = open(data_abs_path)
    
    # returns JSON object as 
    # a dictionary
    data = json.load(f)
    func_data = flatten_json(data)
    rearrange_data(data, folder_path, get_file_name(data_abs_path))
