from PIL import Image
import numpy as np

class CWA:
  def __init__(self, image_path
              , offset=1
              , top_row_val = 3.0
              , rows_range = 6.0
              , left_col_val = -3.0
              , cols_range = 6.0
              ):
    """
    Calculates the weighted average of the y-position for blue-dominant pixels in each column.

    Args:
        image_path (str): The file path to the image.
        offset (int): The minimum difference between the blue and red values (blue - red > offset).

    Returns:
        list: A list of weighted average y-positions for each column.
    """
    self.image_path = image_path
    (self.top_row_val,self.rows_range, self.left_col_val,self.cols_range
    ,) = map(float,(top_row_val, rows_range, left_col_val, cols_range,))
    try:
        with Image.open(image_path) as img:
            # Ensure the image is in RGB format
            img = img.convert("RGB")

            # Convert the image to a NumPy array for efficient processing
            data = np.array(img)
            self.height, self.width = data.shape[:2]

            weighted_averages = list()

            # Iterate through each column of the image
            for col in range(self.width):
                column_pixels = data[:, col]

                # Initialize variables for the weighted average calculation
                total_weighted_position, total_weight = 0,0

                # Iterate through each pixel in the current column
                for row in range(self.height):
                    r, g, b = column_pixels[row]

                    # Check if the blue value is greater than the red value by the specified offset
                    if b > (r + offset):
                        # Use the y-position (row) as the position data
                        # Use the blue value as the weight
                        total_weighted_position += row * (b - r)
                        total_weight += (b - r)

                # Calculate the weighted average for the column
                if total_weight > 0:
                    weighted_average = total_weighted_position / total_weight
                    weighted_averages.extend([col,weighted_average])

            assert weighted_averages, f"No blue data found in {self.image_path}"

            self.wanp =  np.array(weighted_averages,dtype=np.float64).reshape((-1,2,)).T

            ### Scale X column values to nominal 6x6 image (-3 left to +3 right )
            self.xs =  self.left_col_val
            self.xs += self.wanp[0] * self.cols_range / (self.width-1)

            ### Scale Y line values to nominal 6x6 image (+3 top down to -3 bottom)
            ### N.B. Y position of 0 is at top of image; Y position height is at bottom
            self.ys =  self.top_row_val
            self.ys -= self.wanp[1] * self.rows_range / (self.height - 1)

            self.poly = np.polyfit(self.xs,self.ys,8,full=False)

    except FileNotFoundError:
        raise FileNotFoundError("Error: Image file not found at the specified path.")
    except Exception as e:
        raise e

  def plot(self,extra_title=''):
    import matplotlib.pyplot as plt
    plt.plot(self.xs,np.polyval(self.poly,self.xs),'b',lw=5,label='Fit')
    plt.plot(self.xs,self.ys,'c.',label='Raw data')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title(self.image_path + f" ({extra_title})")
    plt.grid()
    plt.legend(loc='best')
    plt.show()

  def deriv_coeffs(self, nderiv, poly=None):
    if poly is None: return self.deriv_coeffs(nderiv, self.poly)
    if nderiv < 1: return poly
    L = len(poly)
    if L < 2: return np.array([0.0])
    pows = list(range(L))[1:]
    pows.reverse()
    return self.deriv_coeffs(nderiv-1, poly[:-1] * np.array(pows))

  def polyval(self, x_eval, nderiv=0):
    return np.polyval(self.deriv_coeffs(nderiv), x_eval)

# Example usage:
# Replace 'your_image.png' with the actual path to your image file
# The offset determines the sensitivity of the blue-red comparison
# offset=0 means blue > red
# offset=50 means blue > red + 50
import sys
if "__main__" == __name__ and 6 == len(sys.argv):

  ### Usage:

  ###   python cwa.py numerator.png <numer offset> denominator.png <denom offset> <x eval>

  ### E.g.

  ###   python cwa.py images/g.png 40 images/f.png 40 .5
  ###   python cwa.py images/f.png 40 images/g.png 40 -1

  ###   numerator.png:
  ###     Path to numerator RGB image file, plot with data in blue
  ###     from (x,y)=(-3,-3) at lower left of image
  ###     to (x,y)=(+3,+3) at upper right of image

  ###   <numer offset>:
  ###     Integer offset of minimum difference between red and blue
  ###     channels of a numerator image's pixel's color to choose that
  ###     pixel as plot data
  ###
  ###     Positions of plot data will be used to fit an
  ###     eighth-order polynomial to the data

  ###   denominator.png:
  ###   - Path to deonminator RGB image file, plot with data in blue
  ###     - from (x,y)=(-3,-3) at lower left of image
  ###       to (x,y)=(+3,+3) at upper right of image

  ###   <denom offset>:
  ###     Integer offset of minimum difference between red and blue
  ###     channels of a denominator image's pixel's color to choose that
  ###     pixel as plot data
  ###
  ###     Positions of plot data will be used to fit an
  ###     eighth-order polynomial to the data

  ###   <x eval>:
  ###     Numeric X value at which to evaluate d(Numer/Denom) / dx

  (numer_image_file_path, numer_blue_offset_arg
  ,denom_image_file_path, denom_blue_offset_arg
  ,x_eval_arg
  ,) = sys.argv[1:]

  numer_blue_offset = int(numer_blue_offset_arg)
  denom_blue_offset = int(denom_blue_offset_arg)
  x_eval = float(x_eval_arg)

  numer = CWA(numer_image_file_path, offset=numer_blue_offset)
  denom = CWA(denom_image_file_path, offset=denom_blue_offset)

  numer.plot('Numerator')
  denom.plot('Denominator')

  allfour = (numer0val, numer1val, denom0val, denom1val
  ,) = (numer.polyval(x_eval), numer.polyval(x_eval,1)
       ,denom.polyval(x_eval), denom.polyval(x_eval,1)
       ,)

  ### R(x) = numer(x) / denom(x)
  ### R' = (denom*numer' - numer*denom') / denom^2

  R1val = ((denom0val * numer1val) - (numer0val * denom1val)) / (denom0val * denom0val)
  print(allfour)
  print(f"R'({x_eval}) = {R1val}")
