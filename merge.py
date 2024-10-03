import pandas as pd

def merge_share_info(l1_file, l2_file, l3_file, output_file):
    df1 = pd.read_excel(l1_file)
    df2 = pd.read_excel(l2_file)
    df3 = pd.read_excel(l3_file)

    df3['company'] = df3["公司名称"]
    df2['company'] = df2['股东名称']
    df1['company'] = df1["股东名称"]

    df1 = df1.rename(columns={'公司名称': '公司名称_l1', '统一社会信用代码':"统一社会信用代码_l1", '序号':"序号_l1", 
                            "股东名称":"股东名称_l1", '合伙人名称':"合伙人名称_l1", "持股比例":"持股比例_l1", 
                            "出资比例":"出资比例_l1", "认缴出资额(万元)":"认缴出资额(万元)_l1", "认缴出资日期":"认缴出资日期_l1", 
                            "最终受益股份":"最终受益股份_l1", "实缴出资额(万元)":"实缴出资额(万元)_l1", "实缴出资日期":"实缴出资日期_l1",
                            "首次持股日期":"首次持股日期_l1", "关联产品/机构":"关联产品/机构_l1", "股份类型":"股份类型_l1"}) 

    merged_df = pd.merge(df2, df3, on='company', how='left', suffixes=('_l2', '_l3'))
    merged_df['company'] = merged_df["公司名称_l2"]
    merged2_df = pd.merge(df1, merged_df, on='company',how='left')
    merged2_df = merged2_df.drop(columns=['company'])

    merged2_df.to_excel(output_file, index=False)




def merge_basic_info(l1_file, l2_file, l3_file, output_file):
   
    df1 = pd.read_excel(l1_file)
    df2 = pd.read_excel(l2_file)
    df3 = pd.read_excel(l3_file)

    df1['Layer'] = 'Layer1'
    df2['Layer'] = 'Layer2'
    df3['Layer'] = 'Layer3'

    merged_df = pd.concat([df1, df2, df3], ignore_index=True)
    merged_df.to_excel(output_file, index=False)
