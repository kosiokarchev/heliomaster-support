import sys, csv, cv2, datetime
import numpy as np
import pandas as pd
from math import atan
from math import pi

METHODS = ['cv2.TM_CCOEFF',
           'cv2.TM_CCOEFF_NORMED',
           'cv2.TM_CCORR',
           'cv2.TM_CCORR_NORMED',
           'cv2.TM_SQDIFF',
           'cv2.TM_SQDIFF_NORMED']

wav_radpx = {"HALPHA" : 1.1260345355325731e-05,
              "VISIBLE" : 1.1794377267140912e-05}

def correlation(img, wavelength, date):
    METH_NUM = 1
    method = METHODS[METH_NUM]
    pad = 10
    sun_diameter = 0.00929826069

    # template is dynamically generated using the distance Sun - Earth
    df = pd.read_csv("Python/sun_distance.csv")
    df['Date'] = df['Date'].map(lambda a: a.split(" ")[0])
    date_distance = df.set_index("Date").T.to_dict('list')

    diameter = 2*atan(sun_diameter/(2*date_distance[date][0])) / wav_radpx[wavelength]

    side = int(diameter + pad)
    template = np.zeros((side,side),dtype=np.float32)
    I,J = np.ogrid[:side,:side]
    sq_dist = (I - side/2)**2 + (J - side/2)**2
    template[sq_dist < (diameter/2)**2] = 1.0

    # opencv doesnt accept float64
    img = img.astype(np.float32)

    # find correlation with template
    res = cv2.matchTemplate(img,template,eval(method))

    if res is None:
        return (-1,-1) -1

    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
    if eval(method) in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
        top_left = min_loc[::-1]
    else:
        top_left = max_loc[::-1]

    w,h = template.shape
    bottom_right = (top_left[0] + w, top_left[1] + h)

    center = tuple(map(sum, zip(top_left, (int(side/2),int(side/2)))))
    return center[::-1], int(diameter/2), max_val

if __name__ == "__main__":
    date = str(datetime.date.today()).replace("-","")

    params = sys.argv[1].split(" ")
    wavelength = params[0]
    filename = params[1]

    # read image from csv and find center
    img = cv2.imread(filename,0)
    center, radius, score = correlation(img, wavelength, date)

    cv2.circle(img, center, radius, 255, thickness=2)
    cv2.imwrite(filename.replace(".bmp","_center.bmp"), img)

    offset = tuple([len(img[0]) // 2 - center[0], len(img) // 2 - center[1]]) # (RA, DEC)
    offsetDeg = tuple([wav_radpx[wavelength] * (180 / pi) * offset[0],
                       wav_radpx[wavelength] * (180 / pi) * offset[1]])

    print("(", offsetDeg[0], ",", offsetDeg[1], ")", radius, score ,"(", str(offset[0]), ",", str(offset[1]), ")", "(", str(center[0]),",",str(center[1]), ")")
    # finish
