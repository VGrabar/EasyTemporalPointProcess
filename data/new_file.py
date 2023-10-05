import pickle
import pandas as pd
from glob import glob
from tqdm import tqdm

dataset = "Age"

for subset in ["test", "dev", "train"]:
    print(dataset)
    print(subset)
    folder = "new_data/" + dataset

    sequences = glob(folder + "/" + subset + "/*.csv")
    max_event = 0

    df = pd.read_csv(sequences[-1])
    d = {"dim_process": max_event + 1, subset: []}

    for seq in tqdm(sequences):
        df = pd.read_csv(seq)
        curr_seq = []
        if df["event"].max() > max_event:
            max_event = df["event"].max()

        seq_id = seq.split("/")[-1]
        seq_id = seq.split(".")[0]
        curr_seq["id"] = int(seq_id)

        prev_time = 0
        for ind in df.index:
            seq_elem = {}
            seq_elem["time_since_last_event"] = df["time"][ind]/86400 - prev_time
            seq_elem["time_since_start"] = df["time"][ind]/86400
            prev_time = df["time"][ind]/86400
            seq_elem["type_event"] = df["event"][ind]
            curr_seq.append(seq_elem)
        d[subset].append(curr_seq)

    d["dim_process"] = max_event + 1
    print(d["dim_process"])


    with open(dataset + "/" + subset + '.pkl', 'wb') as handle:
        pickle.dump(d, handle)
        #pickle.dump(d, handle, protocol=pickle.HIGHEST_PROTOCOL)
