from scipy.io import loadmat
import matplotlib.pyplot as plt 
from scipy.signal import find_peaks

if __name__ == "__main__":
  
    #full directory of file
    dir = "/Users/Lab User 1/Desktop/Data Folder/Etched/dev25_etched.mat"  #sample directory

    #laser sweep paramaters
    lambda_min = 1510.1
    lambda_max = 1600


    def load_file(dir):  

        #loads the mat file into an cell array
        mat = loadmat(dir) 

        #converting from time to wavelenth and normalizing transmission
        time_max = max(mat['x'][0])
        voltage_max = max(mat['y'][0])
        x = mat['x'][0] * (lambda_max - lambda_min) / time_max + lambda_min
        y = mat['y'][0] * (1/voltage_max)

        #collecting the device number from the mat file for later reference
        start_index = dir.find("dev") + 3
        end_index = dir.find("_", start_index)
        dev_num = int(dir[start_index:end_index])

        #find the peaks in our transmission
        #tune prominence and distance along with other find_peaks parameters that 
        #best fit with your data

        prominence, distance = 0,0
        peaks, _ = find_peaks(-y, prominence=prominence , distance=distance)     

       
        return mat, time_max, voltage_max, x, y, peaks, dev_num
    
    #Plots the transmission spectra and has an option to plot the peaks 
    def plot_transmission(showPeaks):

        _, _, _, x, y, peaks, dev_num = load_file(dir)

        if showPeaks == True:
            plt.plot(x[peaks], y[peaks], "ob"); 
        
        plt.gca().yaxis.set_major_formatter(plt.matplotlib.ticker.StrMethodFormatter('{x:,.3f}'))
        plt.plot(x,y)
        plt.title(("Wavelength vs. Transmisson \n Device #{}").format(dev_num))
        plt.xlabel("Wavelength (nm)")
        plt.ylabel("Normalized Transmission")
        plt.show()
    
#finds the split peaks at single resonance 
def find_split_peaks(dir):
        _, time_max, _, x, _, peaks, _ = load_file(dir)
        splitting = []
        splitLoc= []
        ydiff = []
        xdiff = []   

        #this treshold value is extemely important and must be carefully chosen for each data set
        #it is the minimum treshold distance between peaks to classify as a split peak
        #in my research this value is still not well defined 

        threshold = #minimum distance in nm (between peaks) to be considered a split peak
        for i in range(len(peaks) - 1):

            if (x[peaks[i+1]] - x[peaks[i]] < threshold):

                splitLoc.append(peaks[i])

                splitting_value = ((((peaks[i] + peaks[i+1]) / 2) / (time_max * 10**5)) * (lambda_max - lambda_min)) + lambda_min

                splitting.append(splitting_value)

                ydiff.append((x[peaks[i+1]] - x[peaks[i]]))

                xdiff.append(peaks[i+1] - peaks[i])

        splitting = [round(value,2) for value in splitting]

        return splitLoc, splitting, ydiff, xdiff


#plots and saves the split peaks into your current directory, dev_type is a parameter that will be at the front 
#of the file name ex. "Etched_dev21_1510_1600.png" where dev_type = "Etched"

def save_split_peaks(dir, dev_type):
    mat, _, voltage_max, x, _, _, dev_num = load_file(dir)

    splitLoc, splitting, _, _ = find_split_peaks(dir)

    for i, center_index in enumerate(splitLoc):

       #change this to choose how many data points you want to capture in your images
        window_size = 5000 
        left_lim = center_index - window_size
        right_lim = center_index + window_size

        xwindow = x[left_lim:right_lim]
        ywindow = mat['y'][0][left_lim:right_lim] * (1/voltage_max)

        plt.title(f"{dev_type}, Device #{dev_num}, {splitting[i]} nm")
        plt.xlabel("Wavelength (nm)")
        plt.ylabel("Transmission")
        plt.plot(xwindow,ywindow)
        plt.savefig(f"{dev_type}_dev{dev_num}_{splitting[i]}.png")
        print("{dev_type}_dev{dev_num}_{splitting}.png has been successfully saved...".format\
              (dev_type = dev_type, dev_num = dev_num, splitting = splitting[i]))
        plt.close()

#plots and saves a plot of wavelenth vs the split peak distance
def save_diff_plots(dir, dev_type):
    _, _, _, _, _, _, dev_num = load_file(dir)
    _, splitting, ydiff, _ = find_split_peaks(dir)

    plt.title(f"{dev_type}, Device #{dev_num}, Threshold Difference Plot")
    plt.xlabel("Wavelength (nm)")
    plt.ylabel("Difference")
    plt.scatter(splitting,ydiff, marker = '^', color = 'r')
    plt.savefig(f"{dev_type}_dev{dev_num}_diff_plot.png")
    print("{dev_type}_dev{dev_num}_diff_plot.png has been successfully saved...".format(dev_type = dev_type,dev_num = dev_num))
   









   

    


