'''
ResidencyMatch.py

This algorithm operates by reading an input file of the form

[residents | hospitals] preference 1, preference 2, preference 3, preference 4, ...

Any whitespace occurring in the input files is stripped off.

Usage:

    python ResidencyMatch.py [residents preference file] [hospitals preference file]

[Max Harper, 8/29/20]

'''

import sys
import csv

class ResidencyMatch:

    # behaves like a constructor
    def __init__(self):
        '''
        Think of
        
            unmatchedHospitals
            residentsMappings
            hospitalsMappings
            matches
            
        as being instance data for your class.
        
        Whenever you want to refer to instance data, you must
        prepend it with 'self.<instance data>'
        '''
        
        # list of unmatched hospitals
        self.unmatchedHospitals = [ ]

        # list of unmatched residents
        self.unmatchedResidents = [ ]
        
        # dictionaries representing preferences mappings
        
        self.residentsMappings = { }
        self.hospitalsMappings = { }
        
        # dictionary of matches where mapping is resident:hospital
        self.matches = { }
        
        # read in the preference files
        
        '''
        This constructs a dictionary mapping a resident to a list of hospitals in order of preference
        '''
        
        prefsReader = csv.reader(open (sys.argv[1],'r'), delimiter = ',')
        for row in prefsReader:
            resident = row[0].strip()

             # all hospitals are initially unmatched
            self.unmatchedResidents.append(resident)
            #print("Unmatched Residents: ", self.unmatchedResidents)

            # maps a resident to a list of preferences
            self.residentsMappings[resident] = [x.strip() for x in row[1:]] #preferences for residents
            #print("Resident Preferences: ",self.residentsMappings)
            
            # initially have each resident as unmatched
            self.matches[resident] = None
            #print("Matches: ", self.matches)
        
        '''
        This constructs a dictionary mapping a hospital to a list of residents in order of preference
        '''
        
        prefsReader = csv.reader(open (sys.argv[2],'r'), delimiter = ',')
        for row in prefsReader:
            
            hospital = row[0].strip()
            
            # all hospitals are initially unmatched
            self.unmatchedHospitals.append(hospital)
            #print(self.unmatchedHospitals)
            
            # maps a resident to a list of preferences
            self.hospitalsMappings[hospital] = [x.strip() for x in row[1:]] #preferences for hospitals
            #print(self.hospitalsMappings)
    

    def checkDuplicates(self):
        rev_muti = {}
        for key,value in self.matches.items():
            rev_muti.setdefault(value, set()).add(key)
        #print ([values for key, values in rev_muti.items() if len(values) > 1])

    def reportMatches(self):
        print(self.matches) # the final result of the algorithim
        return self.matches
            
    def runMatch(self):
        '''
        It is suggested you use the debugger or similar output statements
        to determine what the contents of the data structures are
        favorite = (lunch['fruits'])[0] to get 
        '''
        
        self.matchedResidents = []
        self.matchedHospitals = []
        keysInMatches = list(self.matches.keys())
        valuesInHospitals = list(self.hospitalsMappings.values())
        
        
        for x in self.matches:
            if self.matches[x] == None: #if values = None
                for x in self.residentsMappings: # looping through residents

                    preferedHospital = (self.residentsMappings[x])[0] #get resident's prefered hospital
                    

                    if preferedHospital in self.unmatchedHospitals: #if resident's prefered hospital is avaliable

                        #get the indexes of where the resident and hospital is in both lists
                        poppedHospitalindex =self.unmatchedHospitals.index(preferedHospital)
                        poppedResidentindex = self.unmatchedResidents.index(x)
                
                        #pop those two from both lists to eventually match
                        poppedHospital = self.unmatchedHospitals.pop(poppedHospitalindex)
                        poppedResident = self.unmatchedResidents.pop(poppedResidentindex)


                        #match the resident and the hospital in self.matches
                        self.matches[x] = poppedHospital
                        valuesInMatches = list(self.matches.values())
                        

                    elif preferedHospital not in self.unmatchedHospitals: #if y's prefered hospital has been taken

                        #put the prefered hospital BACK in unmatched due to a conflict
                        self.unmatchedHospitals.append(preferedHospital) 

                        i = 0 #using for incrementing

                        while preferedHospital in self.unmatchedHospitals:

                        
                            #this is the resident who has y's preferedHospital
                            currentResident=keysInMatches[valuesInMatches.index(preferedHospital)]

                            #get the preferedHospital's prefered resident's list
                            compare = self.hospitalsMappings.get(preferedHospital)

                            #find the indexes of who we are comparing, one wh0 has the hospital and the resident who wants it
                            compareXResident = compare.index(x)
                            compareCurrentResident = compare.index(currentResident)

                            

                            #get the index of y's prefered hospital
                            unmatchedHosIndex = self.unmatchedHospitals.index(preferedHospital) 

                            #if hospital prefers CurrentResident over X resident (Doris over Charlie for VT, Charlie over Alex for CA)
                            if compareXResident < compareCurrentResident:

                                #get the indexes of where the resident and hospital is in both lists
                                self.matches[currentResident] = None
                                poppedHospitalindex =self.unmatchedHospitals.index(preferedHospital)
                                poppedResidentindex = self.unmatchedResidents.index(x)
                
                                #pop those two from both lists to eventually match
                                poppedHospital = self.unmatchedHospitals.pop(poppedHospitalindex)
                                poppedResident = self.unmatchedResidents.pop(poppedResidentindex)


                                #match the resident and the hospital in self.matches
                                self.matches[x] = poppedHospital
                                valuesInMatches = list(self.matches.values())
                                x = currentResident
                                preferedHospital = (self.residentsMappings[x])[1]
                                self.unmatchedHospitals.append(preferedHospital)
                                self.unmatchedResidents.append(x)
                                


                            #if hospital prefers X Resident over current resident 
                            else:

                                #hospital stays matched with current resident
                                self.unmatchedHospitals.pop(unmatchedHosIndex)

                                #move on to the next hospital in y's preference
                                preferedHospital = (self.residentsMappings[x])[i+1]
                            
                                
                                if preferedHospital not in self.unmatchedHospitals:
                                    #go back through the while loop
                                    self.unmatchedHospitals.append(preferedHospital)
                                    i = i + 1
                                else:
                                    #Get the indexes of the resident(x) and their new prefered hospital
                                    poppedHospitalIndex =self.unmatchedHospitals.index(preferedHospital) 
                                    poppedResidentIndex = self.unmatchedResidents.index(x)

                                    #pop them from the list to show they have been matched
                                    poppedHospital = self.unmatchedHospitals.pop(poppedHospitalIndex)
                                    poppedResident = self.unmatchedResidents.pop(poppedResidentIndex)

                                    #add to matches
                                    self.matches[x] = preferedHospital
                                    valuesInMatches = list(self.matches.values())

                                    #reset i to 0
                                    i = 0
                                    

                            


                        
                        

                
        '''
        FINAL MATCHES:
        {'Alex', 'WA'}
        {'Barbara', 'NY'}
        {'Charlie', 'CA'}
        {'Doris', 'VT'}
        ''' 
        
            

if __name__ == "__main__":
   
    # some error checking
    if len(sys.argv) != 3:
        print('ERROR: Usage\n python ResidencyMatch.py [residents preferences] [hospitals preferences]')
        quit()

    # create an instance of ResidencyMatch 
    match = ResidencyMatch()

    # now call the runMatch() function
    match.runMatch()
    
    # report the matches
    match.reportMatches()

    match.checkDuplicates()



