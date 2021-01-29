import pandas as pd
from datetime import datetime
import csv


#? ======================= Func used ======================= 
def add_Create_At(data,list):
    for date in data['Created At']:
        word=date[0:10]
        # Cut value left date only
        list.append(word)

def add_Current(data,list):
    for time in range (len(data)):
        todaysdate = str(datetime.now())
        #create date&time
        word=todaysdate[0:10]
        # Cut value left date only
        list.append(word)

def get_current_datetime_as_dict():
    n = datetime.now()
    #defind current date
    t = n.timetuple()
    #create tuple date (tuple similar list)
    field_names = ["year",
                "month",
                "day",
                "hour",
                "min",
                "sec",
                "weekday",
                "md",
                "yd"]
    return dict(zip(field_names, t))

def WritetoCSV(data):
	with open('Report_life_User.csv','a',newline='',encoding='utf-8') as file :
		fw = csv.writer(file) # fw = file writer
		fw.writerow(data)
	print('success')

#? ======================= Create New column DATA ======================= 
Create_At=[]  # Only list date
Current=[] # Only list date


#? ======================= Import DATA ======================= 
maindata = pd.read_csv('query_result.csv')  
print(maindata.info()) 


#? Use Func
add_Create_At(maindata,Create_At)
add_Current(maindata,Current)
    # Two Func is changing date,time value to word



#? ======================= Update Value ======================= 
maindata['Created At'] = Create_At
    ## replace value
maindata['currentdate'] = Current
    ## create current date

maindata[['Created At','Last Seen','currentdate']] = maindata[['Created At','Last Seen','currentdate']].apply(pd.to_datetime)
    #change type value
    # .apply(pd.to_datetime) it change type value for operate plus or minus date.
smalldata = maindata[['Created At','Last Seen','currentdate']] 
    # short data




#? ======================= Check date in data ======================= 
if  ((get_current_datetime_as_dict()['month'])-1) != 0:   #! This is prombles
    smalldata = smalldata[smalldata['Created At'].dt.month <= ((get_current_datetime_as_dict()['month'])-1)]
    # This case used by not data between 2 years
else:
    smalldata = smalldata[smalldata['Created At'].dt.year <= ((get_current_datetime_as_dict()['year'])-1)]
    # This case used by data between 2 years




 #? =======================  Check Value month current =======================  
print(('=====================================',(get_current_datetime_as_dict()['month'])-1),'=====================================')





#? ======================= Create column how long to anything ======================= 
smalldata['longSeen'] = abs((smalldata['Last Seen']- smalldata['currentdate']).dt.days)
    ## How long for last seen
smalldata['longCreate'] = abs((smalldata['Created At']- smalldata['currentdate']).dt.days)
    ## How long for create
smalldata['longActive'] = abs((smalldata['Created At']- smalldata['Last Seen']).dt.days)
    ## How long for Active

print(smalldata)


#? Notice zero day
print("================================","Zero Days " , ((smalldata['longActive']  == 0 )).sum() , " Company","================================")


#? ======================= Clear data outstanding ======================= 
smalldata[smalldata['longActive']  <=((smalldata['longActive'] .sum())/len(smalldata))]
    ## longActive must be <= mean longActive

#? ======================= Summary data ======================= 
print('\n')
print('============  Mean value is {} day ============'.format(smalldata['longActive'].mean()))
print('\n')
print('============ describe day ============')
print(smalldata['longActive'].describe())
print('\n')
print('============ frequency ============')
print(smalldata.longActive.value_counts())
print('\n')


#? ======================= Export finished Data ======================= 
smalldata[['Created At','Last Seen','longActive']].to_csv('2companylose.csv')



#? ======================= Export of Summary data ======================= 
cc = [('date {} \ndescribe\n{}\nhow long total active\n{}'.format(datetime.now(),smalldata['longActive'].describe(),smalldata.longActive.value_counts()))]
WritetoCSV(cc)