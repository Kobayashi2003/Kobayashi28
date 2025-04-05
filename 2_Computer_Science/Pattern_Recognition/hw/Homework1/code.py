import cv2
import numpy as np
from skimage.feature import hog


def harris_corner_detection(img_path):
    img = cv2.imread(img_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    Ix = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
    Iy = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)

    window_size = 3
    k = 0.04 # Harris parameter α

    Ix2 = cv2.GaussianBlur(Ix**2, (window_size, window_size), 0)
    Iy2 = cv2.GaussianBlur(Iy**2, (window_size, window_size), 0)
    Ixy = cv2.GaussianBlur(Ix * Iy, (window_size, window_size), 0)

    det = Ix2 * Iy2 - Ixy**2
    trace = Ix2 + Iy2
    R = det - k * trace**2

    threshold = 0.01 * R.max()
    R[R < threshold] = 0
    R = cv2.dilate(R, None)
    keypoints = np.argwhere(R > 0)
    return keypoints
    
def draw_keypoints(img_path, keypoints):
    img = cv2.imread(img_path)
    output = img.copy()
    for y, x in keypoints:
        cv2.circle(output, (x, y), 1, (0, 0, 255), -1)
    return output


def match_sift_features(img1_path, img2_path):
    img1 = cv2.imread(img1_path)
    img2 = cv2.imread(img2_path)
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    
    sift = cv2.SIFT_create()
    keypoints1, descriptors1 = sift.detectAndCompute(gray1, None)
    keypoints2, descriptors2 = sift.detectAndCompute(gray2, None)
    
    bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=True)
    matches = bf.match(descriptors1, descriptors2)
    
    matches = sorted(matches, key=lambda x: x.distance)
    
    match_img = cv2.drawMatches(img1, keypoints1, img2, keypoints2, matches[:50], None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
    
    return keypoints1, keypoints2, descriptors1, descriptors2, matches, match_img

def match_hog_features(img1_path, img2_path):
    img1 = cv2.imread(img1_path)
    img2 = cv2.imread(img2_path)
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    
    # detector = cv2.SIFT_create(nfeatures=100)
    detector = cv2.SIFT_create()
    keypoints1 = detector.detect(gray1, None)
    keypoints2 = detector.detect(gray2, None)
    
    hog_params = dict(orientations=8, pixels_per_cell=(4, 4), cells_per_block=(2, 2), visualize=False)
    
    def compute_hog_descriptors(image, keypoints, params):
        descriptors = []
        valid_kps = []
        for kp in keypoints:
            x, y = int(kp.pt[0]), int(kp.pt[1])
            if 8 <= x < image.shape[1]-8 and 8 <= y < image.shape[0]-8:
                window = image[y-8:y+8, x-8:x+8]
                desc = hog(window, **params)
                descriptors.append(desc)
                valid_kps.append(kp)
        return np.array(descriptors, dtype=np.float32), valid_kps
    
    descriptors1, valid_keypoints1 = compute_hog_descriptors(gray1, keypoints1, hog_params)
    descriptors2, valid_keypoints2 = compute_hog_descriptors(gray2, keypoints2, hog_params)
    
    bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=True)
    matches = bf.match(descriptors1, descriptors2)
    matches = sorted(matches, key=lambda x: x.distance)
    
    match_img = cv2.drawMatches(img1, valid_keypoints1, img2, valid_keypoints2, 
                               matches[:50], None, 
                               flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
    
    return valid_keypoints1, valid_keypoints2, descriptors1, descriptors2, matches, match_img

def stitch_images_with_ransac(img1, keypoints1, img2, keypoints2, matches):
    src_pts = np.float32([keypoints1[m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)
    dst_pts = np.float32([keypoints2[m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)
    
    M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
    
    h1, w1 = img1.shape[:2]
    h2, w2 = img2.shape[:2]
    
    pts = np.float32([[0, 0], [0, h1-1], [w1-1, h1-1], [w1-1, 0]]).reshape(-1, 1, 2)
    dst = cv2.perspectiveTransform(pts, M)
    
    min_x = min(0, dst[0][0][0], dst[1][0][0], dst[2][0][0], dst[3][0][0])
    min_y = min(0, dst[0][0][1], dst[1][0][1], dst[2][0][1], dst[3][0][1])
    max_x = max(w2, dst[0][0][0], dst[1][0][0], dst[2][0][0], dst[3][0][0])
    max_y = max(h2, dst[0][0][1], dst[1][0][1], dst[2][0][1], dst[3][0][1])
    
    translation_matrix = np.array([
        [1, 0, -min_x],
        [0, 1, -min_y],
        [0, 0, 1]
    ])
    M_translated = translation_matrix.dot(M)
    
    stitched_width = int(max_x - min_x)
    stitched_height = int(max_y - min_y)
    stitched_img = np.zeros((stitched_height, stitched_width, 3), dtype=np.uint8)
    
    cv2.warpPerspective(img1, M_translated, (stitched_width, stitched_height), stitched_img)
    
    stitched_img[-int(min_y):h2-int(min_y), -int(min_x):w2-int(min_x)] = img2
    
    return stitched_img

def stitch_multiple_images(image_paths):
    result = cv2.imread(image_paths[0])
    
    for i in range(1, len(image_paths)):
        img = cv2.imread(image_paths[i])
        
        sift = cv2.SIFT_create()
        
        gray_result = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        keypoints1, descriptors1 = sift.detectAndCompute(gray_result, None)
        keypoints2, descriptors2 = sift.detectAndCompute(gray_img, None)
        
        FLANN_INDEX_KDTREE = 1
        index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
        search_params = dict(checks=50)
        flann = cv2.FlannBasedMatcher(index_params, search_params)
        
        matches = flann.knnMatch(descriptors1, descriptors2, k=2)
        
        good_matches = []
        for m, n in matches:
            if m.distance < 0.7 * n.distance:
                good_matches.append(m)
        
        if len(good_matches) > 10:
            src_pts = np.float32([keypoints1[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
            dst_pts = np.float32([keypoints2[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)
            
            M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
            
            h1, w1 = result.shape[:2]
            h2, w2 = img.shape[:2]
            
            pts = np.float32([[0, 0], [0, h1-1], [w1-1, h1-1], [w1-1, 0]]).reshape(-1, 1, 2)
            dst = cv2.perspectiveTransform(pts, M)
            
            min_x = min(0, dst[0][0][0], dst[1][0][0], dst[2][0][0], dst[3][0][0])
            min_y = min(0, dst[0][0][1], dst[1][0][1], dst[2][0][1], dst[3][0][1])
            max_x = max(w2, dst[0][0][0], dst[1][0][0], dst[2][0][0], dst[3][0][0])
            max_y = max(h2, dst[0][0][1], dst[1][0][1], dst[2][0][1], dst[3][0][1])
            
            translation_matrix = np.array([
                [1, 0, -min_x],
                [0, 1, -min_y],
                [0, 0, 1]
            ])
            M_translated = translation_matrix.dot(M)
            
            stitched_width = int(max_x - min_x)
            stitched_height = int(max_y - min_y)
            stitched_img = np.zeros((stitched_height, stitched_width, 3), dtype=np.uint8)
            
            cv2.warpPerspective(result, M_translated, (stitched_width, stitched_height), stitched_img)
            
            stitched_img[-int(min_y):h2-int(min_y), -int(min_x):w2-int(min_x)] = img
            
            result = stitched_img
            
    return result


if __name__ == '__main__':
    import os
    import time

    os.makedirs('results', exist_ok=True)

    # 1. Harris corner detection
    suduku_img_path = 'images/sudoku.png'
    suduku_keypoints = harris_corner_detection(suduku_img_path)
    suduku_output = draw_keypoints(suduku_img_path, suduku_keypoints)
    cv2.imwrite('results/sudoku_keypoints.png', suduku_output)

    uttower1_img_path = 'images/uttower1.jpg'
    uttower1_keypoints = harris_corner_detection(uttower1_img_path)
    uttower1_output = draw_keypoints(uttower1_img_path, uttower1_keypoints)
    cv2.imwrite('results/uttower1_keypoints.png', uttower1_output)

    uttower2_img_path = 'images/uttower2.jpg'
    uttower2_keypoints = harris_corner_detection(uttower2_img_path)
    uttower2_output = draw_keypoints(uttower2_img_path, uttower2_keypoints)
    cv2.imwrite('results/uttower2_keypoints.png', uttower2_output)

    # 2. SIFT and HOG feature matching
    uttower1_path = 'images/uttower1.jpg'
    uttower2_path = 'images/uttower2.jpg'
    
    # SIFT feature matching
    start_time = time.time()
    kp1_sift, kp2_sift, desc1_sift, desc2_sift, matches_sift, match_img_sift = match_sift_features(uttower1_path, uttower2_path)
    end_time = time.time()
    print(f"SIFT feature matching time: {end_time - start_time} seconds")
    if match_img_sift is not None:
        cv2.imwrite('results/uttower_match_sift.png', match_img_sift)
    
    # HOG feature matching
    start_time = time.time()
    kp1_hog, kp2_hog, desc1_hog, desc2_hog, matches_hog, match_img_hog = match_hog_features(uttower1_path, uttower2_path)
    end_time = time.time()
    print(f"HOG feature matching time: {end_time - start_time} seconds")
    if match_img_hog is not None:
        cv2.imwrite('results/uttower_match_hog.png', match_img_hog)
    
    # 3. Image stitching
    img1 = cv2.imread(uttower1_path)
    img2 = cv2.imread(uttower2_path)
    
    # SIFT + RANSAC stitching
    start_time = time.time()
    if matches_sift and len(matches_sift) > 10:
        stitched_img_sift = stitch_images_with_ransac(img1, kp1_sift, img2, kp2_sift, matches_sift[:50])
        cv2.imwrite('results/uttower_stitching_sift.png', stitched_img_sift)
    end_time = time.time()
    print(f"SIFT + RANSAC stitching time: {end_time - start_time} seconds")

    # HOG + RANSAC stitching
    start_time = time.time()
    if matches_hog and len(matches_hog) > 10:
        stitched_img_hog = stitch_images_with_ransac(img1, kp1_hog, img2, kp2_hog, matches_hog[:50])
        cv2.imwrite('results/uttower_stitching_hog.png', stitched_img_hog)
    end_time = time.time()
    print(f"HOG + RANSAC stitching time: {end_time - start_time} seconds")

    # 4. Multi-image stitching (Yosemite images)
    yosemite_paths = [
        'images/yosemite1.jpg',
        'images/yosemite2.jpg',
        'images/yosemite3.jpg',
        'images/yosemite4.jpg'
    ]
    
    yosemite_stitched = stitch_multiple_images(yosemite_paths)
    cv2.imwrite('results/yosemite_stitched.png', yosemite_stitched)