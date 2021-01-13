import yaml
import sys

if sys.version_info >= (3,0):
    file_path = str(input("Full path or relevant path to jmx list everything: \n"))
    name = str(input("Name for new config files:\n "))
else:
    file_path = str(raw_input("Full path or relevant path to jmx list everything: \n"))
    name = str(raw_input("Name for new config files:\n "))  

f = open(file_path, "r")
lines = f.readlines()

numeric_type = [
    "long",
    "int",
    "float",
    "double",
    "java.lang.Double",
    "java.lang.Float",
    "java.lang.Integer",
    "java.lang.Long",
    "java.util.concurrent.atomic.AtomicInteger",
    "java.util.concurrent.atomic.AtomicLong",
    "java.lang.Number",
    "class java.lang.Double",
    "class java.lang.Float",
    "class java.lang.Integer",
    "class java.lang.Long",
    "class java.util.concurrent.atomic.AtomicInteger",
    "class java.util.concurrent.atomic.AtomicLong",
    "class java.lang.Number"
]

non_numeric_type = [
    "java.lang.String",
    "java.lang.Object",
    "java.lang.Boolean",
    "boolean",
    "class java.lang.Object",
    "class java.lang.Boolean",
    "class java.lang.String"
]

numeric_hash = {}
non_numeric_hash={}
all_beans_hash={}
conf_hash = {"conf": []}
conf_hash_numeric = {"conf": []}
conf_hash_non_numeric = {"conf": []}

beanlist = []
for line in lines: 
    if "Not Matching" in line:
        beanlist.append(line)

for i in range(len(beanlist)):
    beanlist[i] = beanlist[i].split("Bean name: ")[1]

for bean in beanlist:
    split_bean = bean.split(" - Attribute name: ")[0]
    final_bean = (bean.split(" - Attribute name: ")[1]).split("  - Attribute type: ")
    final_bean.append(split_bean)
    types = final_bean[1].strip('\n')
    if types in numeric_type:
        if final_bean[2] in numeric_hash:
            if final_bean[0].strip('\n') in numeric_hash[final_bean[2]]["attribute"]:
                pass
            else:
                numeric_hash[final_bean[2]]["attribute"].append(final_bean[0])
        else:
            numeric_hash[final_bean[2]] = {}
            numeric_hash[final_bean[2]]["attribute"] = final_bean[0].split()
            numeric_hash[final_bean[2]]["bean_name"] = final_bean[2]
            numeric_hash[final_bean[2]]["domain"] = final_bean[2].split(":")[0]
    else:
        if final_bean[2] in non_numeric_hash:
            if final_bean[0].strip('\n') in non_numeric_hash[final_bean[2]]["attribute"]:
                pass
            else:
                non_numeric_hash[final_bean[2]]["attribute"].append(final_bean[0])
        else:
            non_numeric_hash[final_bean[2]] = {}
            non_numeric_hash[final_bean[2]]["attribute"] = final_bean[0].split()
            non_numeric_hash[final_bean[2]]["bean_name"] = final_bean[2]
            non_numeric_hash[final_bean[2]]["domain"] = final_bean[2].split(":")[0]
    if final_bean[2] in all_beans_hash:
        if final_bean[0].strip('\n') in all_beans_hash[final_bean[2]]["attribute"]:
            pass
        else:
            all_beans_hash[final_bean[2]]["attribute"].append(final_bean[0])
    else:
        all_beans_hash[final_bean[2]] = {}
        all_beans_hash[final_bean[2]]["attribute"] = final_bean[0].split()
        all_beans_hash[final_bean[2]]["bean_name"] = final_bean[2]
        all_beans_hash[final_bean[2]]["domain"] = final_bean[2].split(":")[0]

for key, value in numeric_hash.items():
    temp_hash = {}
    temp_hash["include"] = value
    conf_hash_numeric["conf"].append(temp_hash)

for key, value in non_numeric_hash.items():
    temp_hash = {}
    temp_hash["include"] = value
    conf_hash_non_numeric["conf"].append(temp_hash)

for key, value in all_beans_hash.items():
    temp_hash = {}
    temp_hash["include"] = value
    conf_hash["conf"].append(temp_hash)

conf_all = name + ".yaml"
conf_numeric = name + "_numeric.yaml"
conf_non_numeric = name + "_non_numeric.yaml"

with open(conf_all, 'w') as outfile:
    yaml.dump(conf_hash, outfile, default_flow_style=False)

with open(conf_numeric, 'w') as outfile:
    yaml.dump(conf_hash_numeric, outfile, default_flow_style=False)

with open(conf_non_numeric, 'w') as outfile:
    yaml.dump(conf_hash_non_numeric, outfile, default_flow_style=False)

print("files created:")
print(conf_all)
print(conf_numeric)
print(conf_non_numeric)