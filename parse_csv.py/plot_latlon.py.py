import argparse


def main():
    parser = argparse.ArgumentParser(description="csvファイルに保存された位置情報データから線付き散布図(移動経路履歴図)を作成する")

    parser.add_argument("-o","-open",type=str,help="解析対象のファイルのパス指定",required=True)
    parser.add_argument("-s","-save",action="store_true",help="生成した散布図を保存する",required=True)

    args = parser.parse_args()

if __name__ == "__main__":
    main()