# adinfo

Active Directory のユーザー情報を抽出します。

## 環境

* Windows 10 x64 1809
* Python 3.6.5 x64
* Power Shell 6 x64
* Visual Studio Code x64
* Git for Windows x64

## 構築

プロジェクトを clone してディレクトリに移動します。

```powershell
> git clone https://github.com/kerobot/adinfo adinfo
> cd adinfo
```

プロジェクトのための仮想環境を作成して有効化します。

```powershell
> python -m venv venv
> .\venv\Scripts\activate.ps1
```

念のため、仮想環境の pip をアップグレードします。

```powershell
> python -m pip install --upgrade pip
```

依存するパッケージをインストールします。

```powershell
> pip install -r requirements.txt
```

環境変数を設定します。

```powershell
> copy .\.env.sample .\.env
> code .\.env
```

## 実行

ユーザー情報を出力するCSVファイルのパスを指定して実行します。

```powershell
> python .\adinfo c:\temp\adinfo.csv
```
