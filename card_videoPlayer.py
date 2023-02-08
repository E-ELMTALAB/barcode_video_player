###  main ### 

### main ###
import box_finder as box_finder
import cv2
import numpy as np
from pyzbar.pyzbar import decode
import barcode_reader as bar_reader


if __name__ == '__main__':

    cap = cv2.VideoCapture(0)
    # video = cv2.VideoCapture(r"C:\python\open_cv\opencv_practice\warp_bitwise_practice\card_videoPlayer\20170609_190435.mp4")
    video_1 = cv2.VideoCapture(r"F:\movie\Ted.2.2015.1080p.Farsi.Dubbed.mkv")
    video_2 = cv2.VideoCapture(r"F:\movie\No Time To Die (2021)\No  Time To Die (2021).mkv")
    


    while cv2.waitKey(1) != ord('q'):
        
    #### first operations on the image 
        _ , image = cap.read()
        image_copy = image.copy()
        image_gray = cv2.cvtColor(image , cv2.COLOR_BGR2GRAY)
        image_blur = cv2.GaussianBlur(image_gray ,(5 , 5) ,1 )
        image_threshold = cv2.adaptiveThreshold(image_blur, 255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,19, 8)
        image_canny = cv2.Canny(image_threshold , 10 , 50)
        image_dilate = cv2.dilate(image_canny , (5 , 5) , iterations=4)
        height, width, channels = image.shape

        # square_found , four_points , image = box_finder.find_four_points(image , image_dilate , True , True)

        four_points , found , bar_name , image = bar_reader.read_barcode(image)

        # intializing the pionts 
        if found:
            _ , ted_frame = video_1.read()
            _ , bond_frame = video_2.read()

            match bar_name:
                case "ted":
                    frame = ted_frame
                case "bond":
                    frame = bond_frame
                    
            overlay_h, overlay_w = frame.shape[:2]
            points1 = np.float32([[0, 0], [overlay_w, 0], [overlay_w, overlay_h],[0, overlay_h]])
            points2 = np.float32(four_points)

            # warping
            transformation_matrix = cv2.getPerspectiveTransform(points1, points2)
            warped_img = cv2.warpPerspective(frame, transformation_matrix, (width, height))

            # making the mask to put the image on it
            mask = np.zeros(image.shape, dtype=np.uint8)
            roi_corners = np.int32(four_points)
            mask = cv2.fillConvexPoly(mask, roi_corners, (255, 255, 255))
            mask = cv2.bitwise_not(mask)

            # bitwise_and with the base_image
            masked_base_img = cv2.bitwise_and(mask , image)

            # bitwise_or for the final result
            final_masked_base = cv2.bitwise_or(masked_base_img , warped_img)
            print(bar_name)

            # cv2.imshow("final" , final_masked_base)
            image = final_masked_base



            


        
        # if square_found:
        #     warped , points1 , points2 = box_finder.warp(image , four_points)
        #     boxes = box_finder.slice(warped)
        #     boxes = np.array(boxes)
        #     sod_solver.solve(board)
        #     # sod_solver.print_board(board , warped)
        #     predicted_number = (detector.classify_digit(boxes[0][5]))
        #     print("predicted : " + str(predicted_number))
        #     written_box = box_finder.write_on_box(warped , 0 , 6 , predicted_number )

            
        #     # boxes2 = np.reshape(boxes , (9 , 9))
        #     # written_box = box_finder.write_on_box(warped , 4 , 8 , 6)
        #     # written_box = box_finder.write_on_box(warped , 8 , 0 , 3)
        #     # written_box = box_finder.write_on_box(warped , 0 , 8 , 7)
        #     # written_box = box_finder.write_on_box(warped , 8 , 8 , 2)

        #     rewarped = box_finder.rewarp(image , points1 , points2 , warped)
        #     cv2.imshow("warped" , warped)
        #     cv2.imshow("slice[0]" , boxes[0][5])
        #     # cv2.imshow("written_box" , written_box)
        #     cv2.imshow("rewarped" , rewarped)
        #     # print(boxes)


    #### showing the processed image 
        
        cv2.imshow("final" , image)
        # cv2.imshow("video" , frame)