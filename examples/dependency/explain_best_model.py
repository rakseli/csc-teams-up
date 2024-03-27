import pandas as pd

if __name__ == "__main__":
    df = pd.read_csv("./results/results.csv",header=0)
    print(f"Best result is: {df[df.res == df.res.max()]}")
    