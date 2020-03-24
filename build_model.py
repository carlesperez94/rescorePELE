from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import StandardScaler
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import tree
from sklearn.tree import DecisionTreeRegressor  
import numpy as np


def get(csv1, csv2, field="ic50"):
    X_df = pd.read_csv(csv1, index_col=0).drop(["path"], axis=1)
    X_df["be_norm"] = [v/n for v, n in zip(X_df["be"].values, X_df["atoms"].values)]
    X_df = X_df.drop(["toten", "weight"], axis=1) 
    print(X_df)
    ys = pd.read_csv(csv2)[field]
    y = [-5.82,
-4.70,   
-5.11,
-5.39,
-4.65,
-5.54,
-4.88,
-5.39,
-4.66,
-5.68,
-5.82,
-7.29,
-6.01,
-5.70,
-4.90,
2.00,
2.00,
-4.00
]
    print(y)
    X = StandardScaler().fit_transform(X_df)
    print("Without scaling")
    #reg = LinearRegression().fit(X, y)
    reg = LinearRegression().fit(X, y)
    print(reg.score(X, y), reg.coef_, reg.intercept_)
    plt.bar(list(X_df), reg.coef_)
    plt.savefig("feature_importance.png")
    pred = reg.predict(X)
    fig, ax = plt.subplots()
    ax.set_ylabel("pic50 expb")
    ax.set_xlabel("pic50 prediction")
    ax.scatter(pred, y)
    plt.savefig("correlation.png")
    
    
    
    clf = tree.DecisionTreeRegressor(max_depth=4)
    tree.plot_tree(clf.fit(X, y), feature_names=list(X_df))
    plt.savefig("tree.png")
  

    for column in list(X_df):
        fig, ax = plt.subplots() 
        ax.set_ylabel("ic50")
        ax.set_xlabel(column)
        ax.scatter(X_df[column], y)
        plt.savefig(column+".png")
  

    for column in list(X_df):
        fig, ax = plt.subplots() 
        ax.set_ylabel("ic50")
        ax.set_xlabel(column)
        ax.set_ylim([0,20])
        ax.scatter(X_df[column], y)
        plt.savefig(column+"lim.png")
  

    
    
