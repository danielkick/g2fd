# AUTOGENERATED! DO NOT EDIT! File to edit: ../02_FreshStart_2021.ipynb.

# %% auto 0
__all__ = ['prlst', 'prlst2dct', 'dash80', 'mk_uniq_val_dict', 'pr_eq_list', 'mk_df_of_n_similar_cols',
           'mk_df_of_most_similar_cols', 'match_df_cols', 'mk_name_dict', 'find_unrecognized_columns',
           'list_known_experiments', 'find_unrecognized_experiments', 'sanitize_Experiment_Codes',
           'find_unconvertable_datetimes', 'find_unconvertable_numerics', 'sanitize_col',
           'relocate_to_Imputation_Notes', 'safe_create_col', 'cols_astype_string', 'check_df_dtype_expectations',
           'mk_dtype_dict', 'write_out_pkl']

# %% ../02_FreshStart_2021.ipynb 4
# Settings ----
# Helper functions,remove if no longer needed
def prlst(lst): 
    "This is just a helper function to ease formating lists of strings with each entryon a different line."
    print('[')
    for e in lst:
        if e != lst[-1]:
            print("'"+e+"', ")
        else:
            print("'"+e+"'")
    print(']')
    
def prlst2dct(lst): 
    "This is just a helper function to ease formating lists of strings with each entryon a different line."
    print('{')
    for e in lst:
        if e != lst[-1]:
            print("'"+e+"': 'XXXXXXX', ")
        else:
            print("'"+e+"': 'XXXXXXX'")
    print('}')
    
def dash80(dash = '-'): return ''.join([dash for e in range(80)])


# prlst([])
# prlst2dct([])
# dash80()

# %% ../02_FreshStart_2021.ipynb 7
# Helper functions to match up the same data in different dataframes under different columns names

# make a dictionary of column name : unique values
def mk_uniq_val_dict(df1):
    uniq_val_dict = {}
    for df1_col in list(df1.columns):
        uniq_val_dict.update({df1_col:set(df1[df1_col])})
    return(uniq_val_dict)

def pr_eq_list(lst1, lst2): return len(set(lst1) & set(lst2)) / len(set(lst1) | set(lst2))

# take two dictionaries from `mk_uniq_val_dict` and a key to match, return a df of the n closest matches (based on set of column values)
def mk_df_of_n_similar_cols(dct1, key_to_match, dct2, n = 1):
    # key_to_match = 'Experiment_Code'        
    lst = dct1[key_to_match]
    # dct2 = dict1

    keys = dct2.keys()
    similarities = [pr_eq_list(lst, dct2[e]) for e in dct2.keys()]

    similarityDf = pd.DataFrame(
        zip(dct2.keys(), similarities), 
        columns=['Column2', 'PrMatch']
    ).sort_values('PrMatch', ascending=False)
    
    output = similarityDf.head(n)
    output.insert(0, column = 'Column1', value = key_to_match)
    return(output)

# take two dictionaries from `mk_uniq_val_dict` and find the best match for each key in dict1 in dict2. 
def mk_df_of_most_similar_cols(dict1, dict2):
    return( pd.concat( [mk_df_of_n_similar_cols(dct1 = dict1, key_to_match = key, dct2 = dict2, n = 1) for key in dict1.keys() ]) )

# Combine `mk_df_of_most_similar_cols` and `mk_uniq_val_dict` to find the closest matches between two columns in different dfs.
# Should be helpful for finding columns with the same data but different names (e.g. Experiment vs Experiment_Code)
def match_df_cols(df1, df2):
    df1_cols = list(df1.columns)
    df2_cols = list(df2.columns)

    dict1 = mk_uniq_val_dict(df1)
    dict2 = mk_uniq_val_dict(df2)
    
    return(mk_df_of_most_similar_cols(dict1, dict2))

# %% ../02_FreshStart_2021.ipynb 10
def mk_name_dict(name # table meta, phno, soil, wthr, or mgmt
                ):
    'Easily share dictionaries for renaming columns across scripts.'  

    meta_name_dict = {
    'Experiment_Code': 'Experiment_Code', # Unchanged 
    'Treatment': 'Treatment', # Unchanged 
    'City': 'City', # Unchanged 
    'Farm': 'Farm', # Unchanged 
    'Field': 'Field', # Unchanged 
    'Trial_ID (Assigned by collaborator for internal reference)': 'Trial_ID', 
    'Soil_Taxonomic_ID and horizon description, if known': 'Soil_Taxonomic_ID', 
    'Weather_Station_Serial_Number (Last four digits, e.g. m2700s#####)': 'Weather_Station_Serial_Number', 
    'Weather_Station_Latitude (in decimal numbers NOT DMS)': 'Weather_Station_Latitude_Unit_Decimal', 
    'Weather_Station_Longitude (in decimal numbers NOT DMS)': 'Weather_Station_Longitude_Unit_Decimal', 
    'Date_weather_station_placed': 'Weather_Station_Placed_Unit_Datetime', 
    'Date_weather_station_removed': 'Weather_Station_Removed_Unit_Datetime', 
    'In-field weather station serial number': 'Weather_Station_In_Field_Serial_Number', 
    'In-field_weather_station_latitude (in decimal)': 'Weather_Station_In_Field_Latitude_Unit_Decimal', 
    'In-field_weather_station_longitude (in decimal)': 'Weather_Station_In_Field_Longitude_Unit_Decimal', 
    'Previous_Crop': 'Previous_Crop', # Unchanged 
    'Pre-plant_tillage_method(s)': 'Pre_Plant_Tillage', 
    'In-season_tillage_method(s)': 'Post_Plant_Tillage', 
    'Plot_length (center-alley to center-alley in feet)': 'Plot_Length_Unit_Feet', 
    'Alley_length (in inches)': 'Alley_Length_Unit_Inches', 
    'Row_spacing (in inches)': 'Row_Spacing_Unit_Inches', 
    'Type_of_planter (fluted cone; belt cone; air planter)': 'Planter_Type', 
    'Number_kernels_planted_per_plot (>200 seed/pack for cone planters)': 'Kernels_Per_Plot', 
    'System_Determining_Moisture': 'System_Determining_Moisture', # Unchanged 
    'Pounds_Needed_Soil_Moisture': 'Pounds_Needed_Soil_Moisture', # Unchanged 
    'Latitude_of_Field_Corner_#1 (lower left)': 'Field_Latitude_BL', 
    'Longitude_of_Field_Corner_#1 (lower left)': 'Field_Longitude_BL', 
    'Latitude_of_Field_Corner_#2 (lower right)': 'Field_Latitude_BR', 
    'Longitude_of_Field_Corner_#2 (lower right)': 'Field_Longitude_BR', 
    'Latitude_of_Field_Corner_#3 (upper right)': 'Field_Latitude_TR', 
    'Longitude_of_Field_Corner_#3 (upper right)': 'Field_Longitude_TR', 
    'Latitude_of_Field_Corner_#4 (upper left)': 'Field_Latitude_TL', 
    'Longitude_of_Field_Corner_#4 (upper left)': 'Field_Longitude_TL', 
    'Cardinal_Heading_Pass_1': 'Cardinal_Heading', 
    'Local_Check_#1_Pedigree': 'Local_Check_Pedigree_1', 
    'Local_Check_#1_Source': 'Local_Check_Source_1', 
    'Local_Check_#2_Pedigree': 'Local_Check_Pedigree_2', 
    'Local_Check_#2_Source': 'Local_Check_Source_2', 
    'Local_Check_#3_Pedigree': 'Local_Check_Pedigree_3', 
    'Local_Check_#3_Source': 'Local_Check_Source_3', 
    'Local_Check_#4_Pedigree': 'Local_Check_Pedigree_4', 
    'Local_Check_#4_Source': 'Local_Check_Source_4', 
    'Local_Check_#5_Pedigree': 'Local_Check_Pedigree_5', 
    'Local_Check_#5_Source': 'Local_Check_Source_5', 
    'Issue/comment_#1': 'Comment_1', 
    'Issue/comment_#2': 'Comment_2', 
    'Issue/comment_#3': 'Comment_3', 
    'Issue/comment_#4': 'Comment_4', 
    'Issue/comment_#5': 'Comment_5', 
    'Issue/comment_#6': 'Comment_6', 
    'Issue/comment_#7': 'Comment_7', 
    'Issue/comment_#8': 'Comment_8', 
    'Issue/comment_#9': 'Comment_9', 
    'Issue/comment_#10': 'Comment_70'
    }

    phno_name_dict = {
    'Year': 'Year', 
    'Field-Location': 'Experiment_Code', 
    'State': 'State', # Unchanged 
    'City': 'City', # Unchanged 
    'Plot length (center-center in feet)': 'Plot_Length_Unit_Feet', 
    'Plot area (ft2)': 'Plot_Area_Unit_Feet2', 
    'Alley length (in inches)': 'Alley_Length_Unit_Inches', 
    'Row spacing (in inches)': 'Row_Spacing_Unit_Inches', 
    'Rows per plot': 'Rows_Per_Plot', 
    '# Seed per plot': 'Seeds_Per_Plot', 
    'Experiment': 'Experiment', # Unchanged 
    'Source': 'Source', # Unchanged 
    'Pedigree': 'Pedigree', # Unchanged 
    'Family': 'Family', # Unchanged 
    'Tester': 'Tester', # Unchanged 
    'Replicate': 'Replicate', # Unchanged 
    'Block': 'Block', # Unchanged 
    'Plot': 'Plot', # Unchanged 
    'Plot_ID': 'Plot_ID', # Unchanged 
    'Range': 'Range', # Unchanged 
    'Pass': 'Pass', # Unchanged 
    'Date Plot Planted [MM/DD/YY]': 'Planted_Unit_Datetime', 
    'Date Plot Harvested [MM/DD/YY]': 'Harvested_Unit_Datetime', 
    'Anthesis [MM/DD/YY]': 'Anthesis_Unit_Datetime', 
    'Silking [MM/DD/YY]': 'Silking_Unit_Datetime', 
    'Anthesis [days]': 'Anthesis_Unit_Days', 
    'Silking [days]': 'Silking_Unit_Days', 
    'Plant Height [cm]': 'Plant_Height_Unit_cm', 
    'Ear Height [cm]': 'Ear_Height_Unit_cm', 
    'Stand Count [# of plants]': 'Stand_Count_Unit_Number', 
    'Root Lodging [# of plants]': 'Root_Lodging_Unit_Number', 
    'Stalk Lodging [# of plants]': 'Stalk_Lodging_Unit_Number', 
    'Grain Moisture [%]': 'Grain_Moisture_Unit_Percent', 
    'Test Weight [lbs]': 'Test_Weight_Unit_lbs', 
    'Plot Weight [lbs]': 'Plot_Weight_Unit_lbs', 
    'Grain Yield (bu/A)': 'Grain_Yield_Unit_bu_Per_A', 
    "Plot Discarded [enter 'yes' or blank]": 'Discarded', 
    'Comments': 'Phenotype_Comments', 
    'Filler': 'Filler', # Unchanged 
    'Snap [# of plants]': 'Snap_Unit_Number'
    }

    soil_name_dict = {
    'Grower': 'Grower', # Unchanged 
    'Location': 'Experiment_Code', 
    'Date Received': 'Recieved_Date_Unit_Datetime', 
    'Date Reported': 'Processed_Date_Unit_Datetime', 
    'E Depth': 'Depth_Unit_UNK', 
    '1:1 Soil pH': 'Soil_1_to_1_Unit_pH', 
    'WDRF Buffer pH': 'WDRF_Buffer_Unit_pH', 
    '1:1 S Salts mmho/cm': 'Soluable_Salts_Unit_mmho_Per_cm', 
    'Texture No': 'Texture_Number', 
    'Organic Matter LOI %': 'Organic_Matter_Unit_Percent', 
    'Nitrate-N ppm N': 'Nitrates_Unit_ppm', 
    'lbs N/A': 'N_per_Acre_Unit_lbs', 
    'Potassium ppm K': 'K_Unit_ppm', 
    'Sulfate-S ppm S': 'Sulfate_Unit_ppm', 
    'Calcium ppm Ca': 'Ca_Unit_ppm', 
    'Magnesium ppm Mg': 'Mg_Unit_ppm', 
    'Sodium ppm Na': 'Na_Unit_ppm', 
    'CEC/Sum of Cations me/100g': 'Cation_Exchange_Capacity', 
    '%H Sat': 'H_Sat_Unit_Percent', 
    '%K Sat': 'K_Sat_Unit_Percent', 
    '%Ca Sat': 'Ca_Sat_Unit_Percent', 
    '%Mg Sat': 'Mg_Sat_Unit_Percent', 
    '%Na Sat': 'Na_Sat_Unit_Percent', 
    'Mehlich P-III ppm P': 'Mehlich_PIII_P_Unit_ppm', 
    '% Sand': 'Sand_Unit_Percent', 
    '% Silt': 'Silt_Unit_Percent', 
    '% Clay': 'Clay_Unit_Percent', 
    'Texture': 'Texture', # Unchanged 
    'Comments': 'Soil_Comments'
    }

    wthr_name_dict = {
    'Field Location': 'Experiment_Code', 
    'Station ID': 'Weather_Station_ID', 
    'NWS Network': 'NWS_Network', 
    'NWS Station': 'NWS_Station', 
    'Date_key': 'Datetime', 
    'Month': 'Month', # Unchanged 
    'Day': 'Day', # Unchanged 
    'Year': 'Year', # Unchanged 
    'Time': 'Time', # Unchanged 
    'Temperature [C]': 'Temperature_Unit_C', 
    'Dew Point [C]': 'Dew_Point_Unit_C', 
    'Relative Humidity [%]': 'Relative_Humidity_Unit_Percent', 
    'Solar Radiation [W/m2]': 'Solar_Radiation_Unit_W_per_m2', 
    'Rainfall [mm]': 'Rainfall_Unit_mm', 
    'Wind Speed [m/s]': 'Wind_Speed_Unit_m_per_s', 
    'Wind Direction [degrees]': 'Wind_Direction_Unit_Degrees', 
    'Wind Gust [m/s]': 'Wind_Gust_Unit_m_per_s', 
    'Soil Temperature [C]': 'Soil_Temperature_Unit_C', 
    'Soil Moisture [%VWC]': 'Soil_Moisture_Unit_Percent_VWC', 
    'Soil EC [mS/cm]': 'Soil_EC_Unit_mS_per_cm', 
    'UV Light [uM/m2s]': 'UV_Light_Unit_uM_per_m2s', 
    'PAR [uM/m2s]': 'PAR_Unit_uM_per_m2s',
    'CO2 [ppm]': 'CO2_Unit_ppm' # 2020
    }

    mgmt_name_dict = {
    'Location': 'Experiment_Code', 
    'Application_or_treatment': 'Application', 
    'Product_or_nutrient_applied': 'Product', 
    'Date_of_application': 'Date_Datetime', 
    'Quantity_per_acre': 'Amount_Per_Acre', 
    'Application_unit': 'Unit'
    }
    
    
    if name == 'meta':
        return meta_name_dict
    elif name == 'phno':
        return phno_name_dict
    elif name == 'soil':
        return soil_name_dict
    elif name == 'wthr':
        return wthr_name_dict
    elif name == 'mgmt':
        return mgmt_name_dict
    else:
        print('Requested name is not defined')
    

# %% ../02_FreshStart_2021.ipynb 14
# check if there are columns that need to be aded to the naming dictionaries:
def find_unrecognized_columns(df, dct): 
    keys_and_vals = list(dct.keys())
    keys_and_vals.extend(list(dct.values()))
    keys_and_vals
    return([e for e in df.columns if e not in keys_and_vals])

# %% ../02_FreshStart_2021.ipynb 18
def list_known_experiments():
    'Provides a list of the experiments expected for use in `find_unrecognized_experiments`'
    known_exps = [
        'COH1', 'DEH1', 'GAH1', 'GAH2', 'GEH1', 'IAH1', 'IAH2', 'IAH3', 'IAH4', 'ILH1', 'INH1', 
        'MIH1', 'MNH1', 'NCH1', 'NEH1', 'NEH2', 'NEH3', 'NYH2', 'NYH3', 'NYS1', 'SCH1', 'TXH1', 
        'TXH2', 'TXH3', 'WIH1', 'WIH2', 'WIH3',
        'MOH1', 'OHH1' # 2020
                 ]
    return(known_exps)

# %% ../02_FreshStart_2021.ipynb 19
# check Experiment_Code columns for any unexpected columns
def find_unrecognized_experiments(column, 
                                  known_exps = list_known_experiments(), # Either a list of Experiment_Code s or a list of all provided by the default
                                  return_all_exps = False):
#     known_exps = ['COH1', 'DEH1', 'GAH1', 'GAH2', 'GEH1', 'IAH1', 'IAH2', 'IAH3', 'IAH4', 'ILH1', 'INH1', 'MIH1', 'MNH1', 'NCH1', 'NEH1', 'NEH2', 'NEH3', 'NYH2', 'NYH3', 'NYS1', 'SCH1', 'TXH1', 'TXH2', 'TXH3', 'WIH1', 'WIH2', 'WIH3']
    if return_all_exps:
        known_exps.sort()
        return(known_exps)
    else:
        unknown_exps = [str(e) for e in list(set(column)) if e not in known_exps]
        unknown_exps.sort()
        return(unknown_exps)

# find_unrecognized_experiments(soil.Experiment_Code, print_all_exps=True)


# %% ../02_FreshStart_2021.ipynb 20
# sanitize Experiment Codes

def sanitize_Experiment_Codes(df, simple_renames= {}, split_renames= {}):
    # simple renames
    for e in simple_renames.keys():
        mask = (df.Experiment_Code == e)
        df.loc[mask, 'Experiment_Code'] = simple_renames[e]

    # splits
    # pull out the relevant multiname rows, copy, rename, append
    for e in split_renames.keys():
        mask = (df.Experiment_Code == e)
        temp = df.loc[mask, :] 

        df = df.loc[~mask, :]
        for e2 in split_renames[e]:
            temp2 = temp.copy()
            temp2['Experiment_Code'] = e2
            df = df.merge(temp2, how = 'outer')

    return(df)

# %% ../02_FreshStart_2021.ipynb 30
import pandas as pd
# Make versions of `find_unconvertable_datetimes` for other datatype
# make a function to find the unexpected entries so it's easy to write the santization code
# in a column, report all the values causing errors OR an index of these values
def find_unconvertable_datetimes(df_col, pattern = '%m/%d/%y', index = False):
    datetime_errors = pd.to_datetime(pd.Series(df_col), format = pattern, errors='coerce').isna()
    if index == True:
        return(datetime_errors)
    else:
        # This is a interesting trick. Python's nan is not equal to itself.
        # missing values can't become datetimes so nan is returned if there's a missing value
        # This list comprehension removes nan (which is otherwise stubborn to remove) because nan != nan
        return([e for e in list(set(df_col[datetime_errors])) if e == e]) 

# %% ../02_FreshStart_2021.ipynb 31
import pandas as pd
def find_unconvertable_numerics(df_col, # Dataframe column (e.g. df['example']) to be used.
                                index = False # Return an index of unconveratbles or a list of unique values
                               ):
    "Find the values or positions of values that cannot be converted to a numeric."
    numeric_errors = pd.to_numeric(pd.Series(df_col), errors='coerce').isna()
    if index == True:
        return(numeric_errors) # a
    else:
        # This is a interesting trick. Python's nan is not equal to itself.
        # missing values can't become datetimes so nan is returned if there's a missing value
        # This list comprehension removes nan (which is otherwise stubborn to remove) because nan != nan
        return([e for e in list(set(df_col[numeric_errors])) if e == e]) # b  

# %% ../02_FreshStart_2021.ipynb 32
# generalized version of `sanitize_Experiment_Codes`
def sanitize_col(df, col, simple_renames= {}, split_renames= {}):
    # simple renames
    for e in simple_renames.keys():
        mask = (df[col] == e)
        df.loc[mask, col] = simple_renames[e]

    # splits
    # pull out the relevant multiname rows, copy, rename, append
    for e in split_renames.keys():
        mask = (df[col] == e)
        temp = df.loc[mask, :] 

        df = df.loc[~mask, :]
        for e2 in split_renames[e]:
            temp2 = temp.copy()
            temp2[col] = e2
            df = df.merge(temp2, how = 'outer')

    return(df)

# %% ../02_FreshStart_2021.ipynb 33
import numpy as np
# If the Imputation_Notes column doesnt exist, create it. So long as it wouldn't overwrite any imputation notes move each specified value and replace it with nan.
def relocate_to_Imputation_Notes(df, col, val_list):
    if not 'Imputation_Notes' in df.columns:
        df.loc[:, 'Imputation_Notes'] = np.nan

    for relocate in val_list:
        mask = (df.loc[:, col] == relocate)
        mask_Impute_Full = ((df.loc[:, 'Imputation_Notes'] == '') | (df.loc[:, 'Imputation_Notes'].isna()))
        # check if this contains anyting
        overwrite_danger = df.loc[(mask & ~mask_Impute_Full), 'Imputation_Notes']
        if overwrite_danger.shape[0] > 0:
            print("Warning! The following values will be overwritten. Skipping relocation.")
            print(overwrite_danger)
        else:
            df.loc[(mask), 'Imputation_Notes'] = df.loc[(mask), col]
            df.loc[(mask), col] = np.nan
    return(df)

# %% ../02_FreshStart_2021.ipynb 34
# helper function so we can ask for a new column don't have to worry about overwritting a if it already exists 
def safe_create_col(df, col_name):
    if not col_name in df.columns:
        df.loc[:, col_name] = np.nan
    return(df)

# %% ../02_FreshStart_2021.ipynb 35
# little helper function to make this easier. Make all the columns in a list into dtype string.
# require the column to exist to make this safe.
# to make things even easier, use a list comprehension to pull out the keys in the *_col_dtype dict 
# that have value of 'string'!
def cols_astype_string(df, col_list):
    for e in [ee for ee in col_list if ee in df.columns]:
        df[e] = df[e].astype('string')
    return(df)

# %% ../02_FreshStart_2021.ipynb 36
import pandas as pd
# Ignore columns that don't exist in the dataframe even if they're specified in the dict
# For testing that sanitization was successful
# a function to check the type of each column 
# shouldn't _change_ anything, just report what I need to fix
def check_df_dtype_expectations(df, dtype_dct):
    found = pd.DataFrame(zip(
        df.columns,
        [str(df[e].dtype) for e in df.columns]
    ), columns=['Column', 'dtype'])


    expected = pd.DataFrame(zip(dtype_dct.keys(), dtype_dct.values()),
                 columns=['Column', 'Expected_dtype']
                )
    mask = [True if e in df.columns else False for e in expected.Column]
    expected = expected.loc[mask, ]
    
    out = found.merge(expected, how = 'outer')
    out = out.assign(Pass = out.dtype == out.Expected_dtype)

    print(str(sum(out.Pass))+'/'+str(len(out.Pass))+' Columns pass.')
    return(out)

# each df should get individual treatment with these steps. Probably most readable

# %% ../02_FreshStart_2021.ipynb 38
def mk_dtype_dict(name # table sval, wthr, or mgmt
                ):
    'Easily share dictionaries of expected datatypes of the columns across scripts.'
    sval_col_dtypes = {
        'Year': 'string', 
        'Experiment_Code': 'string', 
        'State': 'string', 
        'City': 'string', 
        'Plot_Length_Unit_Feet': 'float64', 
        'Plot_Area_Unit_Feet2': 'float64', 
        'Alley_Length_Unit_Inches': 'float64', 
        'Row_Spacing_Unit_Inches': 'float64', 
        'Rows_Per_Plot': 'float64', 
        'Seeds_Per_Plot': 'float64', 
        'Experiment': 'string', 
        'Source': 'string', 
        'Pedigree': 'string', 
        'Family': 'string', 
        'Tester': 'string', 
        'Replicate': 'string', 
        'Block': 'string', 
        'Plot': 'string', 
        'Plot_ID': 'string', 
        'Range': 'string', 
        'Pass': 'string', 
        'Planted_Unit_Datetime': 'datetime64[ns]', 
        'Harvested_Unit_Datetime': 'datetime64[ns]', 
        'Anthesis_Unit_Datetime': 'datetime64[ns]', 
        'Silking_Unit_Datetime': 'datetime64[ns]', 
        'Anthesis_Unit_Days': 'float64', 
        'Silking_Unit_Days': 'float64', 
        'Plant_Height_Unit_cm': 'float64', 
        'Ear_Height_Unit_cm': 'float64', 
        'Stand_Count_Unit_Number': 'float64', 
        'Root_Lodging_Unit_Number': 'float64', 
        'Stalk_Lodging_Unit_Number': 'float64', 
        'Grain_Moisture_Unit_Percent': 'float64', 
        'Test_Weight_Unit_lbs': 'float64', 
        'Plot_Weight_Unit_lbs': 'float64', 
        'Grain_Yield_Unit_bu_Per_A': 'float64', 
        'Discarded': 'bool', 
        'Phenotype_Comments': 'string', 
        'Filler': 'string', 
        'Snap_Unit_Number': 'float64', 
    'phno': 'bool', 
        'Grower': 'string', 
        'Recieved_Date_Unit_Datetime': 'datetime64[ns]', 
        'Processed_Date_Unit_Datetime': 'datetime64[ns]', 
        'Depth_Unit_UNK': 'float64', 
        'Soil_1_to_1_Unit_pH': 'float64', 
        'WDRF_Buffer_Unit_pH': 'float64', 
        'Soluable_Salts_Unit_mmho_Per_cm': 'float64', 
        'Texture_Number': 'float64', 
        'Organic_Matter_Unit_Percent': 'float64', 
        'Nitrates_Unit_ppm': 'float64', 
        'N_per_Acre_Unit_lbs': 'float64', 
        'K_Unit_ppm': 'float64', 
        'Sulfate_Unit_ppm': 'float64', 
        'Ca_Unit_ppm': 'float64', 
        'Mg_Unit_ppm': 'float64', 
        'Na_Unit_ppm': 'float64', 
        'Cation_Exchange_Capacity': 'float64', 
        'H_Sat_Unit_Percent': 'float64', 
        'K_Sat_Unit_Percent': 'float64', 
        'Ca_Sat_Unit_Percent': 'float64', 
        'Mg_Sat_Unit_Percent': 'float64', 
        'Na_Sat_Unit_Percent': 'float64', 
        'Mehlich_PIII_P_Unit_ppm': 'float64', 
        'Sand_Unit_Percent': 'float64', 
        'Silt_Unit_Percent': 'float64', 
        'Clay_Unit_Percent': 'float64', 
        'Texture': 'string', 
        'Soil_Comments': 'string', 
    'soil': 'bool', 
        'Treatment': 'string', 
        'Farm': 'string', 
        'Field': 'string', 
        'Trial_ID': 'string', 
        'Soil_Taxonomic_ID': 'string', 
        'Weather_Station_Serial_Number': 'string', 
        'Weather_Station_Latitude_Unit_Decimal': 'float64', 
        'Weather_Station_Longitude_Unit_Decimal': 'float64', 
        'Weather_Station_Placed_Unit_Datetime': 'datetime64[ns]', 
        'Weather_Station_Removed_Unit_Datetime': 'datetime64[ns]', 
        'Weather_Station_In_Field_Serial_Number': 'string', 
        'Weather_Station_In_Field_Latitude_Unit_Decimal': 'float64', 
        'Weather_Station_In_Field_Longitude_Unit_Decimal': 'float64', 
        'Previous_Crop': 'string', 
        'Pre_Plant_Tillage': 'string', 
        'Post_Plant_Tillage': 'string', 
        'Planter_Type': 'string', 
        'Kernels_Per_Plot': 'float64', 
        'System_Determining_Moisture': 'string', 
        'Pounds_Needed_Soil_Moisture': 'float64', 
        'Field_Latitude_BL': 'float64', 
        'Field_Longitude_BL': 'float64', 
        'Field_Latitude_BR': 'float64', 
        'Field_Longitude_BR': 'float64', 
        'Field_Latitude_TR': 'float64', 
        'Field_Longitude_TR': 'float64', 
        'Field_Latitude_TL': 'float64', 
        'Field_Longitude_TL': 'float64', 
        'Cardinal_Heading': 'float64', 
        'Local_Check_Pedigree_1': 'string', 
        'Local_Check_Source_1': 'string', 
        'Local_Check_Pedigree_2': 'string', 
        'Local_Check_Source_2': 'string', 
        'Local_Check_Pedigree_3': 'string', 
        'Local_Check_Source_3': 'string', 
        'Local_Check_Pedigree_4': 'string', 
        'Local_Check_Source_4': 'string', 
        'Local_Check_Pedigree_5': 'string', 
        'Local_Check_Source_5': 'string', 
        'Comment_1': 'string', 
        'Comment_2': 'string', 
        'Comment_3': 'string', 
        'Comment_4': 'string', 
        'Comment_5': 'string', 
        'Comment_6': 'string', 
        'Comment_7': 'string', 
        'Comment_8': 'string', 
        'Comment_9': 'string', 
        'Comment_70': 'string', 
    'meta': 'bool',
        'Imputation_Notes': 'string'
    }

    wthr_col_dtypes = {
        'Experiment_Code': 'string', 
        'Weather_Station_ID': 'string', 
        'NWS_Network': 'string', 
        'NWS_Station': 'string', 
        'Datetime': 'datetime64[ns]', 
        'Month': 'string', 
        'Day': 'string', 
        'Year': 'string', 
        'Time': 'string', 
        'Temperature_Unit_C': 'float64', 
        'Dew_Point_Unit_C': 'float64', 
        'Relative_Humidity_Unit_Percent': 'float64', 
        'Solar_Radiation_Unit_W_per_m2': 'float64', 
        'Rainfall_Unit_mm': 'float64', 
        'Wind_Speed_Unit_m_per_s': 'float64', 
        'Wind_Direction_Unit_Degrees': 'float64', 
        'Wind_Gust_Unit_m_per_s': 'float64', 
        'Soil_Temperature_Unit_C': 'float64', 
        'Soil_Moisture_Unit_Percent_VWC': 'float64', 
        'Soil_EC_Unit_mS_per_cm': 'float64', 
        'UV_Light_Unit_uM_per_m2s': 'float64', 
        'PAR_Unit_uM_per_m2s': 'float64', 
    'wthr': 'bool',
        'Imputation_Notes': 'string',
        'CO2_Unit_ppm': 'float64'# 2020
    }

    mgmt_col_dtypes = {
        'Year': 'string',   
        'Experiment_Code': 'string', 
        'Range': 'string',
        'Pass': 'string',
        'Plot': 'string',
        'Application': 'string', 
        'Product': 'string', 
        'Date_Datetime': 'datetime64[ns]', 
        'Amount_Per_Acre': 'float64', 
        'Unit': 'string', 
    'mgmt': 'bool',
        'Imputation_Notes': 'string',
        'Ingredient': 'string'
    }
   
    if name == 'sval':
        return sval_col_dtypes
    elif name == 'wthr':
        return wthr_col_dtypes
    elif name == 'mgmt':
        return mgmt_col_dtypes
    else:
        print('Requested name is not defined')
    

# %% ../02_FreshStart_2021.ipynb 76
import pickle
def write_out_pkl(obj, path = './temp.pickle'):
    with open(path, 'wb') as handle:
        pickle.dump(obj, handle, protocol=pickle.HIGHEST_PROTOCOL)   
