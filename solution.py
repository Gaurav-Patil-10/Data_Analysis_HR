import pandas as pd
import requests
import os


# scroll down to the bottom to implement your solution


if __name__ == '__main__':


   if not os.path.exists('../Data'):
       os.mkdir('../Data')


   # Download data if it is unavailable.
   if ('A_office_data.xml' not in os.listdir('../Data') and
       'B_office_data.xml' not in os.listdir('../Data') and
       'hr_data.xml' not in os.listdir('../Data')):
       print('A_office_data loading.')
       url = "https://www.dropbox.com/s/jpeknyzx57c4jb2/A_office_data.xml?dl=1"
       r = requests.get(url, allow_redirects=True)
       open('../Data/A_office_data.xml', 'wb').write(r.content)
       print('Loaded.')


       print('B_office_data loading.')
       url = "https://www.dropbox.com/s/hea0tbhir64u9t5/B_office_data.xml?dl=1"
       r = requests.get(url, allow_redirects=True)
       open('../Data/B_office_data.xml', 'wb').write(r.content)
       print('Loaded.')


       print('hr_data loading.')
       url = "https://www.dropbox.com/s/u6jzqqg1byajy0s/hr_data.xml?dl=1"
       r = requests.get(url, allow_redirects=True)
       open('../Data/hr_data.xml', 'wb').write(r.content)
       print('Loaded.')


       # All data in now loaded to the Data folder.

   df_a = pd.read_xml('../Data/A_office_data.xml')
   df_b = pd.read_xml('../Data/B_office_data.xml')
   df_hr = pd.read_xml('../Data/hr_data.xml')
   df_a.index = ['A' + str(x) for x in df_a.iloc[:, 7]]
   df_b.index = ['B' + str(x) for x in df_b.iloc[:, 7]]
   df_hr.set_index('employee_id', inplace=True)

   df = pd.concat([df_a, df_b])


   df = df.merge(df_hr, left_index=True, right_index=True, indicator=True)
   df.sort_index(inplace=True)
   df.drop(columns=['employee_office_id', '_merge'], inplace=True)

   # print(df.sort_values(by=['average_monthly_hours'], ascending=False).loc[:, 'Department'].head(10).values.tolist())

   # print(df.query("salary == 'low' & Department == 'IT'").loc[:, 'number_project'].sum().tolist())

   # print(df.loc[['A4', 'B7064', 'A3033'], ['last_evaluation', 'satisfaction_level']].values.tolist())

   def count_bigger_5(arr):
       return sum(arr > 5)

   grouped_data = df.groupby('left').agg({
       "number_project": ["median", count_bigger_5],
       "time_spend_company": ["mean", "median"],
       "Work_accident": ["mean"],
       "last_evaluation": ["mean", "std"],
   })

   # print( grouped_data.round(2) )

   pivot_ = df.pivot_table(index=['Department'] , columns=['left','salary'] , values=['average_monthly_hours'],aggfunc='median')

   # print(pivot_)
   filtered_table = pivot_[((pivot_['average_monthly_hours','0']['high'] <  pivot_['average_monthly_hours','1']['medium']) |
                            (pivot_['average_monthly_hours','1']['low'] <  pivot_['average_monthly_hours','1']['high'])) ]

   if "RandD" in filtered_table.index:
       filtered_table = filtered_table.drop("RandD")
   if "accounting" in filtered_table.index:
       filtered_table = filtered_table.drop("accounting")

   print(filtered_table['average_monthly_hours'].to_dict())

   pivot_2 = df.pivot_table(index=['time_spend_company'] , columns=['promotion_last_5years'] , values=['last_evaluation','satisfaction_level'],aggfunc=['min','max','mean'])


   filtered_table_2 = pivot_2[
       (pivot_2[("mean", "last_evaluation", 0)] < pivot_2[("mean", "last_evaluation", 1)])]

   if 3 in filtered_table_2.index:
       filtered_table_2 = filtered_table_2.drop(3)

   if 7 in filtered_table_2.index:
       filtered_table_2 = filtered_table_2.drop(7)

   if 8 in filtered_table_2.index:
       filtered_table_2 = filtered_table_2.drop(8)


   print(filtered_table_2.round(2).to_dict())

