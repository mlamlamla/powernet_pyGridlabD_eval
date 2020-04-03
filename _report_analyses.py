#Which run
run = 'FinalReport_Jan1d' #'FinalReport_Jul1d'
ind = '0000'

#JANUARY PLOT
settings_file = '/Users/admin/Documents/powernet/powernet_markets_mysql/settings_Jan_1d.csv'
folder = '/Users/admin/Documents/powernet/powernet_markets_mysql/'+run + '_' + ind
folder_nomarket = '/Users/admin/Documents/powernet/powernet_markets_mysql/'+run + '_' + ind
directory = run + '_' + ind + '_vis'

if not os.path.exists(directory):
    os.makedirs(directory)

df_settings = pd.read_csv(settings_file)
s_settings = df_settings.loc[(df_settings['run'] == run) & (df_settings['id'] == int(ind))]

#System
df_system, df_system_nomarket, df_T = sysev.get_systemdata(folder,folder_nomarket,s_settings)
df_system.to_csv(directory+'/df_system.csv')
df_system_nomarket.to_csv(directory+'/df_system_nomarket.csv')
df_T.to_csv(directory+'/df_T.csv')

df_system = pd.read_csv(directory+'/df_system.csv',index_col=[0], parse_dates=True)
df_system_nomarket = pd.read_csv(directory+'/df_system_nomarket.csv',index_col=[0], parse_dates=True)
df_T = pd.read_csv(directory+'/df_T.csv',index_col=[0], parse_dates=True)

sysev.plot_system_prices_week(directory,df_system,s_settings)

#JULY PLOT

settings_file = '/Users/admin/Documents/powernet/powernet_markets_mysql/settings_July_1d.csv'

folder = '/Users/admin/Documents/powernet/powernet_markets_mysql/'+run + '_' + ind
folder_nomarket = '/Users/admin/Documents/powernet/powernet_markets_mysql/'+run + '_' + ind
directory = run + '_' + ind + '_vis'

if not os.path.exists(directory):
    os.makedirs(directory)

df_settings = pd.read_csv(settings_file)
s_settings = df_settings.loc[(df_settings['run'] == run) & (df_settings['id'] == int(ind))]

#System
df_system, df_system_nomarket, df_T = sysev.get_systemdata(folder,folder_nomarket,s_settings)
df_system.to_csv(directory+'/df_system.csv')
df_system_nomarket.to_csv(directory+'/df_system_nomarket.csv')
df_T.to_csv(directory+'/df_T.csv')

df_system = pd.read_csv(directory+'/df_system.csv',index_col=[0], parse_dates=True)
df_system_nomarket = pd.read_csv(directory+'/df_system_nomarket.csv',index_col=[0], parse_dates=True)
df_T = pd.read_csv(directory+'/df_T.csv',index_col=[0], parse_dates=True)

sysev.plot_system_prices_week(directory,df_system,s_settings)


