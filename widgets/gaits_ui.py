# Widgets used to set the leg pose of all legs uniformly
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input
import dash
import dash_daq
from texts import GAITS_WIDGETS_HEADER
from settings import (
    ALPHA_MAX_ANGLE,
    BETA_MAX_ANGLE,
    GAMMA_MAX_ANGLE,
    UPDATE_MODE,
    SLIDER_ANGLE_RESOLUTION,
)
from style_settings import SLIDER_THEME, SLIDER_HANDLE_COLOR, SLIDER_COLOR,BUTTON_COLOR





def make_button(button_id, button_name):
    BUTTON_STYLE = {
        "margin": "0 0 0 0.5em"        
    }

    return html.Button(button_name, id=button_id,style=BUTTON_STYLE)

def make_slider(slider_id, name, max_val,min_val,default_val):

    handle_style = {
        "showCurrentValue": True,
        "color": SLIDER_HANDLE_COLOR,
        "label": name,
    }

    daq_slider = dash_daq.Slider(  # pylint: disable=not-callable
        id = slider_id,
        min = min_val,
        max = max_val,
        value = default_val,
        step = SLIDER_ANGLE_RESOLUTION,
        size = 500,
        updatemode = UPDATE_MODE,
        handleLabel = handle_style,
        color = {"default": SLIDER_COLOR},
        theme = SLIDER_THEME,
    )
    testfont = dash.html.Font(name)
    
    return html.Div([testfont,daq_slider], style={"padding": "2%"})
    #return html.Div([testfont,daq_slider], style={"padding-top": "10%","padding-left": "5%"})

def make_radio(label_id,label_name,label_val):
    
    num_options = len(label_name)

    options_append = [{'label': label_name[0] , 'value': label_val[0]}]
    for i in range(num_options-1):
        options_append = options_append + [{'label': label_name[i+1] , 'value': label_val[i+1]}]

    return dcc.RadioItems(
        id = label_id,
        options = options_append,
        value =label_val[0],
        labelStyle = {'display': 'inline-block'}, # display of flex to create a vertical list, or of inline-block for horizontal.
    )


# ................................
# COMPONENTS
# ................................

HEADER = html.Label(dcc.Markdown(f"**{GAITS_WIDGETS_HEADER}**"))

# 1 make sliders widgets
WIDGET_NAMES = ["hipSwing", "liftSwing", "hipStance","legStance","stepCount","speed"]
GAITS_WIDGET_IDS = [f"widget-{name}" for name in WIDGET_NAMES]
GAITS_CALLBACK_INPUTS = [Input(i, "value") for i in GAITS_WIDGET_IDS]

max_vals =      [35, 90, 35,10,6,400]
min_vals =      [15, 40, 15,-10,0,100]
default_vals =  [25, 60, 25,1,2,300]
widgets = [
    make_slider(id, name, max_val,min_val,default_val)
    for id, name, max_val,min_val,default_val in zip(GAITS_WIDGET_IDS, WIDGET_NAMES, max_vals,min_vals,default_vals)
]

# 2. make button widgets
BUTTON_NAMES = ['Step by step','Start keep moving']
BUTTON_IDS = [f"button-widget-{name}" for name in BUTTON_NAMES]
BUTTON_KEEPMOVING_ID = BUTTON_IDS[1]
button_widgets = [
    make_button(id,name)
    for id,name in zip(BUTTON_IDS,BUTTON_NAMES)

]
GAITS_BUTTON_CALLBACK_INPUTS = [Input(BUTTON_IDS[0], 'n_clicks')]
KEEPMOV_BUTTON_CALLBACK_INPUT = [Input(BUTTON_IDS[1], 'n_clicks')]
# 3. make radio widgets
GAIT_TYPE_NAME = 'gaittype'
GAIT_TYPE_RADIO_OPTION_LABEL = ['tripod gaits','ripple gaits']
GAIT_TYPE_RADIO_OPTION_VAL = ['tripod','ripple']

MOVING_DIR_NAME = 'movdir'
MOVING_DIR_RADIO_OPTION_LABEL = ['forward','backward','rotate left','rotate right']
MOVING_DIR_RADIO_OPTION_VAL = ['walkingforward','walkingbackward','rotatingleft','rotatingright']

#WALKROT_NAME = 'walkrot'
#WALKROT_RADIO_OPTION_LABEL = ['walking mode','rotating mode']
#WALKROT_RADIO_OPTION_VAL = ['walking','rotating']

RADIO_NAMES = [GAIT_TYPE_NAME,MOVING_DIR_NAME ]
RADIO_IDS = [f"radio-widget-{name}" for name in RADIO_NAMES]
RADIOS_CALLBACK_INPUTS = [Input(i, 'value') for i in RADIO_IDS]

radio_widgets = [
    make_radio(option_id,option_label,option_val)
    for option_id,option_label,option_val in zip(
        RADIO_IDS,
        [GAIT_TYPE_RADIO_OPTION_LABEL,MOVING_DIR_RADIO_OPTION_LABEL],
        [GAIT_TYPE_RADIO_OPTION_VAL,MOVING_DIR_RADIO_OPTION_VAL])
]

INTERVAL_ID = 'interval1'
interval_widget = dcc.Interval(id=INTERVAL_ID, interval=500, n_intervals=0,disabled = True)
INTERVAL_CALLBACK_INPUTS = Input(INTERVAL_ID, 'n_intervals')

GAITS_WIDGETS_SECTION = html.Div([HEADER] +button_widgets + radio_widgets + widgets+[interval_widget])
