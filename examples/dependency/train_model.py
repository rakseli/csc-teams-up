import time
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--parameter",type=str,help="which parameter set to give the model",default=1)

if __name__ == "__main__":
    args = parser.parse_args()
    print(f"Starting to train a 'model' with parameter {args.parameter}")
    for i in range(10):
        time.sleep(30)
        print("'Trained' for 30 sec")

    print("Done")