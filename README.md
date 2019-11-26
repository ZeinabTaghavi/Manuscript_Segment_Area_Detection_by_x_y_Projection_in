## find_segment_area_by_x_y_projection_in_Manuscript
### WITH A VARIABLE THRESHOLD


This code will find text areas in a handwriting image.

__Algorithm based on__: Projection (x_y_Projection)

__Time__: 2.64s (per image)

__Process__:

1 - correct rotation to more accurately find lines
    
![first](https://github.com/ZeinabTaghavi/find_segment_area_by_x_y_projection_in_-handwriting_documents/blob/master/sample/7.jpg?raw=true)

2 - find the high compression vertical area
![first](https://github.com/ZeinabTaghavi/find_segment_area_by_x_y_projection_in_-handwriting_documents/blob/master/sample/7.jpg_find_segment_area_by_x_y_projection_1_vertical_line_detected.jpg?raw=true)
    
3 - in vertical high compression areas, find all horizontal high compression areas
![first](https://github.com/ZeinabTaghavi/find_segment_area_by_x_y_projection_in_-handwriting_documents/blob/master/sample/7.jpg_find_segment_area_by_x_y_projection_2_just_lines.jpg?raw=true)
