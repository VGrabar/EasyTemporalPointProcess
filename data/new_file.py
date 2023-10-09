import pickle
import pandas as pd
from glob import glob
from tqdm import tqdm

dataset = "Age"

#for subset in ["test", "dev", "train"]:
for subset in ["full"]:
    print(dataset)
    print(subset)
    folder = "new_data/" + dataset

    sequences = glob(folder + "/" + subset + "/*.csv")
    max_event = 0

    df = pd.read_csv(sequences[-1])
    #d = {"dim_process": max_event + 1, subset: []}
    d = {"dim_process": max_event + 1, "dev": []}

    for seq in tqdm(sequences):
        df = pd.read_csv(seq)
        curr_seq = []

        seq_id = seq.split("/")[-1]
        seq_id = seq_id.split(".")[0]
        if "(" in seq_id or "clusters" in seq_id:
            print(seq_id)
            continue


        if df["event"].max() > max_event:
            max_event = df["event"].max()

        scale = 1.0
        prev_time = 0
        for ind in df.index:
            seq_elem = {}
            seq_elem["time_since_last_event"] = df["time"][ind]/scale - prev_time
            seq_elem["time_since_start"] = df["time"][ind]/scale
            prev_time = df["time"][ind]/scale
            try:
                seq_elem["type_event"] = df["event"][ind]
            except:
                print(seq_id)
                print(df.head())
                break
            seq_elem["id"] = int(seq_id)
            curr_seq.append(seq_elem)
        #d[subset].append(curr_seq)
        d["dev"].append(curr_seq)

    d["dim_process"] = max_event + 1
    print(d["dim_process"])


    with open(dataset + "/" + subset + '.pkl', 'wb') as handle:
        pickle.dump(d, handle)
        #pickle.dump(d, handle, protocol=pickle.HIGHEST_PROTOCOL)
