from sklearn.preprocessing import LabelEncoder
import numpy as np

class Pipeline:

    def __init__(self, dataframe, verbose=False):
        self.dataframe = dataframe
        self.verbose = verbose          # set true for tests

    def preview(self, size):
        '''
        Returns the head of the dataframe.
        '''

        return self.dataframe.head(size)

    def encode(self, col_str):
        '''
        Takes the columns and shifts them to numerical values. 
        Converts missing values through and returns them. 
        Won\'t follow the organisation of a text file very well after though, introduces new labels.
        '''

        encoder = LabelEncoder()

        # The encoder can't handle missing numbers, but I don't want to deal with them just yet, 
        # instead I'll assign a dummy variable and shift it back to NaN after the transfer

        NaN_sum = self.dataframe[col_str].isna().sum()                             # formed here, as it changes otherwise
    
        if NaN_sum > 0:                                                            # replace nan values if the column has them
            self.dataframe[col_str].replace(np.nan, 'missing', inplace=True)       # converts any NaN to a usable value for labels
        
        col_labels = list(dict.fromkeys(self.dataframe[col_str].sort_values(ascending=True)))  # generates the refined list of labels
        encoder.fit(col_labels)
        
        if NaN_sum > 0:                                                            # replace nan values if the column has them
            inverse_transform = encoder.transform(['missing'])                     # translates the NaN back in right at the end
            
        encoded_arr = encoder.transform(self.dataframe[col_str].to_list())                     
        
        if NaN_sum > 0:
            self.dataframe[col_str] = np.where(encoded_arr==inverse_transform, np.nan, encoded_arr)   # translates the NaN back in right at the end
            if self.verbose:
                print('still missing values in', col_str)
        else:
            self.dataframe[col_str] = encoded_arr
            if self.verbose:
                print('All missing values cleaned in', col_str)

    def fill_missing_simple(self, col_str):
        '''
        Replaces mislabelled missing values with a new label.
        Use only on features that have simple behaviour.
        
        Breaks encoding.
        '''

        feature_max = self.dataframe[col_str].max()
        self.dataframe[col_str].fillna(feature_max+1, inplace=True)

    def fill_missing_complex(self, col_str, col_str_dep):
        '''
        Replaces mislabelled missing values with a new label.
        Use on features that have more complex behaviour (depending on other features).
        
        Breaks encoding.
        '''
        feature_max = self.dataframe[col_str].max()
        #feature_req = self.dataframe[col_str_dep]==0

        self.dataframe[col_str].fillna(feature_max+1, inplace=True)

    def cross_checker(self, core_cond, features):
        '''
        Checks if the core feature is present (e.g. has basement), then creates a new group for each
        feature that depends on this for finding the rows that all share missing values. If these are all missing together,
        they are likely just a poorly labelled set (e.g no basement, not NaN).
        
        Breaks encoding.
        '''

        init_lineup = self.dataframe[core_cond].isnull()

        for feat1 in features:
            combi_region = self.dataframe[feat1].isnull() & init_lineup
            self.dataframe.loc[combi_region, feat1] = self.dataframe[feat1].max()+1
