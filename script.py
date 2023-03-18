import pandas as pd
import json


class Drug:
    def __init__(self, _id, drug_name, iv_fluid, storage, pH, incompatible_drugs, type_of_incompatibility):
        self.id = _id
        self.drug_name = drug_name
        self.iv_fluid = iv_fluid
        self.storage = storage
        self.pH = str(pH).strip()
        self.incompatible_drugs = incompatible_drugs
        self.type_of_incompatibility = type_of_incompatibility


class TypeOfIncompatibility:
    def __init__(self, mix, type_, reason):
        self.dose = mix
        self.type = type_
        self.reason = reason


def incompatibilityArr(incompatible_drugs):
    res = [x.strip() for x in incompatible_drugs.split(",") if len(x.strip()) != 0]
    for i in range(len(res)):
        res[i] = res[i].replace(".", "").strip().lower()
    return res


def typeArr(type_of_incompatibility):
    arr = []
    res = [x.strip() for x in type_of_incompatibility.split("\n") if len(x.strip()) != 0]

    for i in range(len(res)):
        res[i] = [x.strip() for x in res[i].split(":")]
        if len(res[i]) == 2:
            if "compatible but" in res[i][1]:
                res[i][1] = res[i][1].split("but")
            else:
                res[i][1] = res[i][1].split(".")

    for i in range(len(res)):
        if len(res[i]) == 2:
            t = TypeOfIncompatibility(res[i][0].strip().replace("\n", ""),
                                      res[i][1][0].strip(),
                                      ".".join(res[i][1][1:]).strip())
            json_t = json.dumps(t.__dict__, indent=4)
            arr.append(json.loads(json_t))

    return arr


def demo(type_):
    pass


if __name__ == "__main__":
    df = pd.read_excel(r"C:\Users\91928\Downloads\IV incompatible drug data (Complete).xlsx")
    final_data = []
    print(len(df))

    for i in range(11, 81):
        drug = Drug(i + 1,
                    df.iloc[i]["Drug Name"].strip(),
                    df.iloc[i]["Diluents"].strip(),
                    df.iloc[i]["Storage"].strip(),
                    df.iloc[i]["pH"],
                    incompatibilityArr(df.iloc[i]["Incompatible Drugs"]),
                    typeArr(df.iloc[i]["Type Of Incompatibility"]))

        json_obj = json.dumps(drug.__dict__, indent=4)
        final_data.append(json.loads(json_obj))

    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(final_data, f, ensure_ascii=False, indent=4)

