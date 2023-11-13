# variables
#HTML Variable
wch_colour_box = (0,204,102)
wch_colour_font = (0,0,0)
fontsize = 18
valign = "left"
iconname = "fas fa-asterisk"
sline = "Observations"
lnk = '<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.12.1/css/all.css" crossorigin="anonymous">'
i = 123

htmlstr = f"""<p style='background-color: rgb({wch_colour_box[0]}, 
                                              {wch_colour_box[1]}, 
                                              {wch_colour_box[2]}, 0.75); 
                        color: rgb({wch_colour_font[0]}, 
                                   {wch_colour_font[1]}, 
                                   {wch_colour_font[2]}, 0.75); 
                        font-size: {fontsize}px; 
                        border-radius: 7px; 
                        padding-left: 12px; 
                        padding-top: 18px; 
                        padding-bottom: 18px; 
                        line-height:25px;'>
                        <i class='{iconname} fa-xs'></i> {i}
                        </style><BR><span style='font-size: 14px; 
                        margin-top: 0;'>{sline}</style></span></p>"""


              
#Pandas Variable
httpResponseCode = ('100', '101', '102', '103', '200', '201', '202', '203', '204', '205', '206', '207', '208', '226', '300', '301', '302', '303', '304', '305' , '306', '307', '308', '400', '401', '402', '403', '404', '405', '406', '407', '408', '409', '419', '500', '501', '502', '503', '504', '505', '506', '507', '508' , '509', '510', '511', 'Nan', ' ')
nonErrorResponseCode = ('100', '101', '102', '103', '200', '201', '202', '203', '204', '205', '206', '207', '208', '226', '300', '301', '302', '303', '304', '305' , '306', '307', '308')
ErrorResponseCode = ('400', '401', '402', '403', '404', '405', '406', '407', '408', '409', '419', '500', '501', '502', '503', '504', '505', '506', '507', '508' , '509', '510', '511')          
color_response_code={
        '200': 'rgb(0, 255, 153)',
    }

#Charts
color_response_code={
   '200': '#0f9758',
    }
color_success={
    'success': '#008000'
}

color_TPS={
    True : '#0f9758',
    False: '#ff5349'
}