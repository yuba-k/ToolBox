import argparse
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

def type_goal(i):
    lon,lat = map(float,i.split(","))
    return lon,lat

def main():
    parser = argparse.ArgumentParser(description="csvファイルに保存された位置情報データから線付き散布図(移動経路履歴図)を作成する")

    parser.add_argument("-o","--open",type=str,help="解析対象のファイルのパス指定",required=True)
    parser.add_argument("-s","--save",action="store_true",help="生成した散布図の保存の有無")
    parser.add_argument("-g","--goal",type=type_goal,help="ゴール座標(lon,lat)で与える．作成される散布図にゴール座標が表示される")
    parser.add_argument("-d","--display",action="store_true",help="グラフ表示の有無")

    args = parser.parse_args()

    try:
        df = pd.read_csv(args.open,header=None,names=["lon","lat"],dtype=float)
    except FileNotFoundError:
        print(f"{args.open}を開けませんでした．\nファイル名,パスが正しいことを確認してください")
        return
        
    if df.empty:
        print(f"{args.open}は空です．")
        return
    df = df.dropna(how="any")
    plt.axis("equal")
    plt.scatter(df["lon"],df["lat"],color="green")
    if args.goal is not None:
        plt.scatter(args.goal[0],args.goal[1],color="red",marker="*")
    plt.plot(df["lon"],df["lat"],color="green")
    plt.title(args.open)
    plt.xlabel("lon")
    plt.ylabel("lat")
    plt.xticks(np.arange(min(df["lon"]),max(df["lon"]),(max(df["lon"])-min(df["lon"]))/5))
    plt.yticks(np.arange(min(df["lat"]),max(df["lat"]),(max(df["lat"])-min(df["lat"]))/5))
    if args.save:
        saved_name = os.path.split(args.open)[1].split('.')[0]
        print(f"suscessful to save \"{saved_name}.png\"")
        plt.savefig(saved_name+".png")
    if args.display:
        plt.show()
    
if __name__ == "__main__":
    main()