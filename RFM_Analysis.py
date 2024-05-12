import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
""
df = pd.read_excel("dosya_adi.xlsx",
                   parse_dates=["Order_Date"])
""
df.dropna(inplace= True)
""
tarih = dt.datetime("yıl","gün","ay")
""
df["Gun_farkı"] = (tarih - df["Order_Date"])
df["Gun_farkı"].astype("timedelta64[us]")
df["Gun_farkı"] = df["Gun_farkı"] / np.timedelta64(1, "D")
df.head()
""
kur = {
    "2019-01": 5.80,
    "2019-02": 5.80,
    "2019-03": 5.80,
    "2019-04": 5.80,
    "2019-05": 5.80,
    "2019-06": 5.80,
    "2019-07": 5.80,
    "2019-08": 5.80,
    "2019-09": 5.80,
    "2019-10": 5.80,
    "2019-11": 5.80,
    "2019-12": 5.80,
    "2020-01": 5.95,
    "2020-02": 6.10,
    "2020-03": 6.35,
    "2020-04": 6.75,
    "2020-05": 6.90,
    "2020-06": 6.80,
    "2020-07": 6.88,
    "2020-08": 7.10,
    "2020-09": 7.55,
    "2020-10": 8.00,
    "2020-11": 8.05,
    "2020-12": 7.60,
    "2021-01": 7.35,
    "2021-02": 7.35,
    "2021-03": 7.85,
    "2021-04": 8.25,
    "2021-05": 8.35,
    "2021-06": 8.60,
    "2021-07": 8.55,
    "2021-08": 8.40,
    "2021-09": 8.55,
    "2021-10": 9.20,
    "2021-11": 11.10,
    "2021-12": 13.60,
    "2022-01": 13.45,
    "2022-02": 13.70,
    "2022-03": 14.20,
    "2022-04": 14.70,
    "2022-05": 15.60,
    "2022-06": 16.50,
    "2022-07": 17.25,
    "2022-08": 18.00,
    "2022-09": 18.35,
    "2022-10": 18.55,
    "2022-11": 18.60,
    "2022-12": 18.65
}
print(kur)
liste=[]
for i in range(((len(df["Order_Date"])))):
    liste.append(((df["Revenue"].iloc[i]))/(kur[str(df["Order_Date"].iloc[i])[:7]]))
print(liste)
df["Revenue"] = liste
""
rfmTable = df.groupby(["Phone (Billing)"]).agg( # ,"Member_Name","Email (Billing)",
    {"Gun_farkı":lambda x: x.min(),
     "Phone (Billing)":lambda x: len(x),
     "Revenue":lambda x: x.sum()}).copy()
rfmTable.rename(columns=
                {"Gun_farkı":"Recency",
                 "Phone (Billing)":"Frequency",
                 "Revenue":"Monetary"},inplace=True)
""
quart = rfmTable.quantile(q=[0.2,0.4,0.6,0.8])
quart= quart.to_dict()
""
def RClass(x,p,d):
    if x <= d[p][0.2]:
        return 5
    elif x <= d[p][0.4]:
        return 4
    elif x <= d[p][0.6]:
        return 3
    elif x <= d[p][0.8]:
        return 2
    else:
        return 1
def FMClass(x,p,d):
    if x <= d[p][0.2]:
        return 1
    elif x <= d[p][0.4]:
        return 2
    elif x <= d[p][0.6]:
        return 3
    elif x <= d[p][0.8]:
        return 4
    else:
        return 5
rfmSeg=rfmTable
rfmSeg["R_Quartile"] = rfmSeg["Recency"].apply(RClass, args=("Recency",quart))
rfmSeg["F_Quartile"] = rfmSeg["Frequency"].apply(FMClass, args=("Frequency",quart))
rfmSeg["M_Quartile"] = rfmSeg["Monetary"].apply(FMClass, args=("Monetary",quart))
rfmSeg.head()
""
rfmSeg["RFMScore"] = rfmSeg.R_Quartile.map(str) + rfmSeg.F_Quartile.map(str) + rfmSeg.M_Quartile.map(str)
rfmSeg.head()
""
df1 = df.sort_values(by="Phone (Billing)").copy()
df1.head()
""
listemm=[]
for i in range(len(df)):
    listemm.append(i)
""
df1[""]= listemm
df1.head()
""
df1 = df1.set_index("")
""
df2=df1.groupby("Phone (Billing)").agg({
    "Email (Billing)":lambda x:(str(set(x)))[2:-2]}).copy()
df2.head()
""
rfmSeg = pd.concat([rfmSeg,df2],axis=1)
""
rfmSeg.loc[rfmSeg["RFMScore"]=="555","RFMScore"]="Champions"
rfmSeg.loc[rfmSeg["RFMScore"]=="554","RFMScore"]="Champions"
rfmSeg.loc[rfmSeg["RFMScore"]=="544","RFMScore"]="Champions"
rfmSeg.loc[rfmSeg["RFMScore"]=="545","RFMScore"]="Champions"
rfmSeg.loc[rfmSeg["RFMScore"]=="454","RFMScore"]="Champions"
rfmSeg.loc[rfmSeg["RFMScore"]=="455","RFMScore"]="Champions"
rfmSeg.loc[rfmSeg["RFMScore"]=="445","RFMScore"]="Champions"
rfmSeg.loc[rfmSeg["RFMScore"]=="543","RFMScore"]="Loyal"
rfmSeg.loc[rfmSeg["RFMScore"]=="444","RFMScore"]="Loyal"
rfmSeg.loc[rfmSeg["RFMScore"]=="435","RFMScore"]="Loyal"
rfmSeg.loc[rfmSeg["RFMScore"]=="355","RFMScore"]="Loyal"
rfmSeg.loc[rfmSeg["RFMScore"]=="354","RFMScore"]="Loyal"
rfmSeg.loc[rfmSeg["RFMScore"]=="345","RFMScore"]="Loyal"
rfmSeg.loc[rfmSeg["RFMScore"]=="344","RFMScore"]="Loyal"
rfmSeg.loc[rfmSeg["RFMScore"]=="335","RFMScore"]="Loyal"
rfmSeg.loc[rfmSeg["RFMScore"]=="553","RFMScore"]="Potential Loyalists"
rfmSeg.loc[rfmSeg["RFMScore"]=="551","RFMScore"]="Potential Loyalists"
rfmSeg.loc[rfmSeg["RFMScore"]=="552","RFMScore"]="Potential Loyalists"
rfmSeg.loc[rfmSeg["RFMScore"]=="541","RFMScore"]="Potential Loyalists"
rfmSeg.loc[rfmSeg["RFMScore"]=="542","RFMScore"]="Potential Loyalists"
rfmSeg.loc[rfmSeg["RFMScore"]=="533","RFMScore"]="Potential Loyalists"
rfmSeg.loc[rfmSeg["RFMScore"]=="532","RFMScore"]="Potential Loyalists"
rfmSeg.loc[rfmSeg["RFMScore"]=="531","RFMScore"]="Potential Loyalists"
rfmSeg.loc[rfmSeg["RFMScore"]=="452","RFMScore"]="Potential Loyalists"
rfmSeg.loc[rfmSeg["RFMScore"]=="451","RFMScore"]="Potential Loyalists"
rfmSeg.loc[rfmSeg["RFMScore"]=="442","RFMScore"]="Potential Loyalists"
rfmSeg.loc[rfmSeg["RFMScore"]=="441","RFMScore"]="Potential Loyalists"
rfmSeg.loc[rfmSeg["RFMScore"]=="431","RFMScore"]="Potential Loyalists"
rfmSeg.loc[rfmSeg["RFMScore"]=="453","RFMScore"]="Potential Loyalists"
rfmSeg.loc[rfmSeg["RFMScore"]=="433","RFMScore"]="Potential Loyalists"
rfmSeg.loc[rfmSeg["RFMScore"]=="432","RFMScore"]="Potential Loyalists"
rfmSeg.loc[rfmSeg["RFMScore"]=="423","RFMScore"]="Potential Loyalists"
rfmSeg.loc[rfmSeg["RFMScore"]=="353","RFMScore"]="Potential Loyalists"
rfmSeg.loc[rfmSeg["RFMScore"]=="352","RFMScore"]="Potential Loyalists"
rfmSeg.loc[rfmSeg["RFMScore"]=="351","RFMScore"]="Potential Loyalists"
rfmSeg.loc[rfmSeg["RFMScore"]=="342","RFMScore"]="Potential Loyalists"
rfmSeg.loc[rfmSeg["RFMScore"]=="341","RFMScore"]="Potential Loyalists"
rfmSeg.loc[rfmSeg["RFMScore"]=="333","RFMScore"]="Potential Loyalists"
rfmSeg.loc[rfmSeg["RFMScore"]=="323","RFMScore"]="Potential Loyalists"
rfmSeg.loc[rfmSeg["RFMScore"]=="512","RFMScore"]="New Customers"
rfmSeg.loc[rfmSeg["RFMScore"]=="511","RFMScore"]="New Customers"
rfmSeg.loc[rfmSeg["RFMScore"]=="422","RFMScore"]="New Customers"
rfmSeg.loc[rfmSeg["RFMScore"]=="421","RFMScore"]="New Customers"
rfmSeg.loc[rfmSeg["RFMScore"]=="412","RFMScore"]="New Customers"
rfmSeg.loc[rfmSeg["RFMScore"]=="411","RFMScore"]="New Customers"
rfmSeg.loc[rfmSeg["RFMScore"]=="311","RFMScore"]="New Customers"
rfmSeg.loc[rfmSeg["RFMScore"]=="525","RFMScore"]="Promising"
rfmSeg.loc[rfmSeg["RFMScore"]=="524","RFMScore"]="Promising"
rfmSeg.loc[rfmSeg["RFMScore"]=="523","RFMScore"]="Promising"
rfmSeg.loc[rfmSeg["RFMScore"]=="522","RFMScore"]="Promising"
rfmSeg.loc[rfmSeg["RFMScore"]=="521","RFMScore"]="Promising"
rfmSeg.loc[rfmSeg["RFMScore"]=="515","RFMScore"]="Promising"
rfmSeg.loc[rfmSeg["RFMScore"]=="514","RFMScore"]="Promising"
rfmSeg.loc[rfmSeg["RFMScore"]=="513","RFMScore"]="Promising"
rfmSeg.loc[rfmSeg["RFMScore"]=="425","RFMScore"]="Promising"
rfmSeg.loc[rfmSeg["RFMScore"]=="424","RFMScore"]="Promising"
rfmSeg.loc[rfmSeg["RFMScore"]=="413","RFMScore"]="Promising"
rfmSeg.loc[rfmSeg["RFMScore"]=="414","RFMScore"]="Promising"
rfmSeg.loc[rfmSeg["RFMScore"]=="415","RFMScore"]="Promising"
rfmSeg.loc[rfmSeg["RFMScore"]=="315","RFMScore"]="Promising"
rfmSeg.loc[rfmSeg["RFMScore"]=="314","RFMScore"]="Promising"
rfmSeg.loc[rfmSeg["RFMScore"]=="313","RFMScore"]="Promising"
rfmSeg.loc[rfmSeg["RFMScore"]=="535","RFMScore"]="Need Attention"
rfmSeg.loc[rfmSeg["RFMScore"]=="534","RFMScore"]="Need Attention"
rfmSeg.loc[rfmSeg["RFMScore"]=="443","RFMScore"]="Need Attention"
rfmSeg.loc[rfmSeg["RFMScore"]=="434","RFMScore"]="Need Attention"
rfmSeg.loc[rfmSeg["RFMScore"]=="343","RFMScore"]="Need Attention"
rfmSeg.loc[rfmSeg["RFMScore"]=="334","RFMScore"]="Need Attention"
rfmSeg.loc[rfmSeg["RFMScore"]=="325","RFMScore"]="Need Attention"
rfmSeg.loc[rfmSeg["RFMScore"]=="324","RFMScore"]="Need Attention"
rfmSeg.loc[rfmSeg["RFMScore"]=="331","RFMScore"]="About To Sleep"
rfmSeg.loc[rfmSeg["RFMScore"]=="321","RFMScore"]="About To Sleep"
rfmSeg.loc[rfmSeg["RFMScore"]=="312","RFMScore"]="About To Sleep"
rfmSeg.loc[rfmSeg["RFMScore"]=="221","RFMScore"]="About To Sleep"
rfmSeg.loc[rfmSeg["RFMScore"]=="213","RFMScore"]="About To Sleep"
rfmSeg.loc[rfmSeg["RFMScore"]=="231","RFMScore"]="About To Sleep"
rfmSeg.loc[rfmSeg["RFMScore"]=="241","RFMScore"]="About To Sleep"
rfmSeg.loc[rfmSeg["RFMScore"]=="251","RFMScore"]="About To Sleep"
rfmSeg.loc[rfmSeg["RFMScore"]=="155","RFMScore"]="Cannot Lose Them But Losing"
rfmSeg.loc[rfmSeg["RFMScore"]=="154","RFMScore"]="Cannot Lose Them But Losing"
rfmSeg.loc[rfmSeg["RFMScore"]=="144","RFMScore"]="Cannot Lose Them But Losing"
rfmSeg.loc[rfmSeg["RFMScore"]=="214","RFMScore"]="Cannot Lose Them But Losing"
rfmSeg.loc[rfmSeg["RFMScore"]=="215","RFMScore"]="Cannot Lose Them But Losing"
rfmSeg.loc[rfmSeg["RFMScore"]=="115","RFMScore"]="Cannot Lose Them But Losing"
rfmSeg.loc[rfmSeg["RFMScore"]=="114","RFMScore"]="Cannot Lose Them But Losing"
rfmSeg.loc[rfmSeg["RFMScore"]=="113","RFMScore"]="Cannot Lose Them But Losing"
rfmSeg.loc[rfmSeg["RFMScore"]=="255","RFMScore"]="At Risk"
rfmSeg.loc[rfmSeg["RFMScore"]=="254","RFMScore"]="At Risk"
rfmSeg.loc[rfmSeg["RFMScore"]=="245","RFMScore"]="At Risk"
rfmSeg.loc[rfmSeg["RFMScore"]=="244","RFMScore"]="At Risk"
rfmSeg.loc[rfmSeg["RFMScore"]=="253","RFMScore"]="At Risk"
rfmSeg.loc[rfmSeg["RFMScore"]=="252","RFMScore"]="At Risk"
rfmSeg.loc[rfmSeg["RFMScore"]=="243","RFMScore"]="At Risk"
rfmSeg.loc[rfmSeg["RFMScore"]=="242","RFMScore"]="At Risk"
rfmSeg.loc[rfmSeg["RFMScore"]=="235","RFMScore"]="At Risk"
rfmSeg.loc[rfmSeg["RFMScore"]=="234","RFMScore"]="At Risk"
rfmSeg.loc[rfmSeg["RFMScore"]=="225","RFMScore"]="At Risk"
rfmSeg.loc[rfmSeg["RFMScore"]=="224","RFMScore"]="At Risk"
rfmSeg.loc[rfmSeg["RFMScore"]=="153","RFMScore"]="At Risk"
rfmSeg.loc[rfmSeg["RFMScore"]=="152","RFMScore"]="At Risk"
rfmSeg.loc[rfmSeg["RFMScore"]=="145","RFMScore"]="At Risk"
rfmSeg.loc[rfmSeg["RFMScore"]=="143","RFMScore"]="At Risk"
rfmSeg.loc[rfmSeg["RFMScore"]=="142","RFMScore"]="At Risk"
rfmSeg.loc[rfmSeg["RFMScore"]=="135","RFMScore"]="At Risk"
rfmSeg.loc[rfmSeg["RFMScore"]=="134","RFMScore"]="At Risk"
rfmSeg.loc[rfmSeg["RFMScore"]=="133","RFMScore"]="At Risk"
rfmSeg.loc[rfmSeg["RFMScore"]=="125","RFMScore"]="At Risk"
rfmSeg.loc[rfmSeg["RFMScore"]=="124","RFMScore"]="At Risk"
rfmSeg.loc[rfmSeg["RFMScore"]=="332","RFMScore"]="Hibernating Customers"
rfmSeg.loc[rfmSeg["RFMScore"]=="322","RFMScore"]="Hibernating Customers"
rfmSeg.loc[rfmSeg["RFMScore"]=="233","RFMScore"]="Hibernating Customers"
rfmSeg.loc[rfmSeg["RFMScore"]=="232","RFMScore"]="Hibernating Customers"
rfmSeg.loc[rfmSeg["RFMScore"]=="223","RFMScore"]="Hibernating Customers"
rfmSeg.loc[rfmSeg["RFMScore"]=="222","RFMScore"]="Hibernating Customers"
rfmSeg.loc[rfmSeg["RFMScore"]=="132","RFMScore"]="Hibernating Customers"
rfmSeg.loc[rfmSeg["RFMScore"]=="123","RFMScore"]="Hibernating Customers"
rfmSeg.loc[rfmSeg["RFMScore"]=="122","RFMScore"]="Hibernating Customers"
rfmSeg.loc[rfmSeg["RFMScore"]=="212","RFMScore"]="Hibernating Customers"
rfmSeg.loc[rfmSeg["RFMScore"]=="211","RFMScore"]="Hibernating Customers"
rfmSeg.loc[rfmSeg["RFMScore"]=="111","RFMScore"]="Lost Customers"
rfmSeg.loc[rfmSeg["RFMScore"]=="112","RFMScore"]="Lost Customers"
rfmSeg.loc[rfmSeg["RFMScore"]=="121","RFMScore"]="Lost Customers"
rfmSeg.loc[rfmSeg["RFMScore"]=="131","RFMScore"]="Lost Customers"
rfmSeg.loc[rfmSeg["RFMScore"]=="141","RFMScore"]="Lost Customers"
rfmSeg.loc[rfmSeg["RFMScore"]=="151","RFMScore"]="Lost Customers"
""
rfmSeg = rfmSeg.reset_index()
rfmSeg = rfmSeg.groupby(["RFMScore","Phone (Billing)"]).agg({ #,"Member_Name","Email (Billing)"
    "Email (Billing)":lambda x:x,
    "Recency":lambda x:x,
    "Frequency":lambda x:x,
    "Monetary":lambda x:x})
rfmSeg.head()
""
rfmSeg.to_excel("dosya_adi.xlsx")