import time
import argparse
import numpy as np
import os 
rng = np.random.default_rng()
parser = argparse.ArgumentParser()
parser.add_argument("--parameter",type=int,help="which parameter set to give the model",default=1)
parser.add_argument("--output_dir",type=str,help="which parameter set to give the model",default="./results")

if __name__ == "__main__":
    args = parser.parse_args()
    if not os.path.exists(args.output_dir):
        os.mkdir(args.output_dir)
    rint = rng.integers(low=0, high=100, size=1)
    print(f"Starting to train a 'model' with parameter {args.parameter}",flush=True)
    for i in range(10):
        time.sleep(2)
        print(f"Iteration {i}, 'trained' for 2 sec",flush=True)
    print("Done",flush=True)
    if not os.path.exists(f"{args.output_dir}/results.csv"):  
        with open(f"{args.output_dir}/results.csv", "w") as f:
            f.write("param,res\n")
            f.write(f"{args.parameter},{rint[0]}\n")
    else:
         with open(f"{args.output_dir}/results.csv", "a") as f:
            f.write(f"{args.parameter},{rint[0]}\n")