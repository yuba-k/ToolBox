import argparse
import os
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def type_goal(goal_coordinates):
    try:
        lon, lat = map(float, goal_coordinates.split(","))
        return lon, lat
    except ValueError:
        raise argparse.ArgumentTypeError(
            "\ngoal座標が正しい形式ではありません\nlon,latの形式で入力してください"
        )


def init():
    """init
    グラフ描画の初期設定
    """
    plt.axis("equal")
    plt.title("Route History")
    plt.xlabel("lon")
    plt.ylabel("lat")


def draw_scatter(data, filename, goal_coordinates, saveFlag, displayFlag):
    plt.scatter(data["lon"], data["lat"], color="green")
    if goal_coordinates is not None:
        plt.scatter(goal_coordinates[0], goal_coordinates[1], color="red", marker="*")
    plt.plot(data["lon"], data["lat"], color="green")
    if saveFlag:
        saved_name = os.path.split(filename)[1].split(".")[0]
        print(f'suscessful to save "{saved_name}.png"')
        plt.savefig(saved_name + ".png")
    if displayFlag:
        plt.show()


def main():
    parser = argparse.ArgumentParser(
        description="csvファイルに保存された位置情報データから線付き散布図(移動経路履歴図)を作成する"
    )

    parser.add_argument(
        "-f", "--file", type=Path, help="解析対象のファイルのパス指定", required=True
    )
    parser.add_argument(
        "-s", "--save", action="store_true", help="生成した散布図の保存の有無"
    )
    parser.add_argument(
        "-g",
        "--goal",
        type=type_goal,
        help="ゴール座標(lon,lat)で与える．作成される散布図にゴール座標が表示される",
    )
    parser.add_argument("-d", "--display", action="store_true", help="グラフ表示の有無")

    args = parser.parse_args()
    init()
    try:
        df = pd.read_csv(
            args.file,
            header=None,
            names=["DateTime", "lon", "lat"],
            dtype={"DateTime": str, "lon": float, "lat": float},
        )
    except FileNotFoundError:
        print(
            f"{args.file}を開けませんでした．\nファイル名,パスが正しいことを確認してください"
        )
        return
    df = df.dropna(how="any")
    if df.empty:
        print(f"{args.file}は空です．")
        return
    elif len(df["lon"]) == 1:
        print("データが1セットしかありません\n移動経路図作成には2セット以上が必要です")
        return
    draw_scatter(
        data=df,
        filename=args.file,
        goal_coordinates=args.goal,
        saveFlag=args.save,
        displayFlag=args.display,
    )


if __name__ == "__main__":
    main()
