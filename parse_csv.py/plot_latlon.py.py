import argparse
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def type_goal(i):
    lon,lat = map(float,i.split(","))
    return lon,lat

def main():
    parser = argparse.ArgumentParser(description="csvファイルに保存された位置情報データから線付き散布図(移動経路履歴図)を作成する")

    parser.add_argument("-o","-open",type=str,help="解析対象のファイルのパス指定",required=True)
    parser.add_argument("-s","-save",action="store_true",help="生成した散布図を保存する",required=True)
    parser.add_argument("-g","-goal",type=type_goal,help="ゴール座標(lon,lat)で与える．作成される散布図にゴール座標が表示される．")

    args = parser.parse_args()

    try:
        df = pd.read_csv(args.o,header=None,names=["lon","lat"])
    except FileNotFoundError:
        print(f"{args.o}を開けませんでした．\nファイル名,パスが正しいことを確認してください")
        exit()
    df = df.dropna(how="any")
    plt.scatter(df["lon"],df["lat"],color="green")
    if args.g is not None:
        plt.scatter(args.g[0],args.g[1],color="red")
    plt.plot(df["lon"],df["lat"],color="green")
    plt.title(args.o)
    plt.xlabel("lon")
    plt.ylabel("lat")
    plt.show()
    
if __name__ == "__main__":
    main()