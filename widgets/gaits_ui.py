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
        "color": BUTTON_COLOR,        
    }

    return html.Button(button_name, id=button_id,style=BUTTON_STYLE)

def make_slider(slider_id, name, max_angle):

    handle_style = {
        "showCurrentValue": True,
        "color": SLIDER_HANDLE_COLOR,
        "label": name,
    }

    daq_slider = dash_daq.Slider(  # pylint: disable=not-callable
        id=slider_id,
        min=-max_angle,
        max=max_angle,
        value=7.5,
        step=SLIDER_ANGLE_RESOLUTION,
        size=300,
        updatemode=UPDATE_MODE,
        handleLabel=handle_style,
        color={"default": SLIDER_COLOR},
        theme=SLIDER_THEME,
    )
    testfont = dash.html.Font(name)
    
    return html.Div([testfont,daq_slider], style={"padding": "2%"})
    #return html.Div([testfont,daq_slider], style={"padding-top": "10%","padding-left": "5%"})

def make_radio(label_name,label_val):
    
    num_options = len(label_name)

    options_append = [{'label': label_name[0] , 'value': label_val[0]}]
    for i in range(num_options-1):
        options_append = options_append + [{'label': label_name[i+1] , 'value': label_val[i+1]}]

    return dcc.RadioItems(
        options = options_append,
        value ='MTL',
        labelStyle = {'display': 'inline-block'}, # display of flex to create a vertical list, or of inline-block for horizontal.
    )


# ................................
# COMPONENTS
# ................................

HEADER = html.Label(dcc.Markdown(f"**{GAITS_WIDGETS_HEADER}**"))

# 1 make sliders widgets
WIDGET_NAMES = ["hipSwing", "liftSwing", "hipStance","liftStance","stepCount","speed"]
GAITS_WIDGET_IDS = [f"widget-{name}" for name in WIDGET_NAMES]
GAITS_CALLBACK_INPUTS = [Input(i, "value") for i in GAITS_WIDGET_IDS]

max_angles = [ALPHA_MAX_ANGLE, BETA_MAX_ANGLE, GAMMA_MAX_ANGLE,GAMMA_MAX_ANGLE,GAMMA_MAX_ANGLE,GAMMA_MAX_ANGLE]
widgets = [
    make_slider(id, name, angle)
    for id, name, angle in zip(GAITS_WIDGET_IDS, WIDGET_NAMES, max_angles)
]

# 2. make button widgets
BUTTON_NAMES = ['Step by step','Keep moving']
BUTTON_IDS = [f"button-widget-{name}" for name in BUTTON_NAMES]
button_widgets = [
    make_button(id,name)
    for id,name in zip(BUTTON_IDS,BUTTON_NAMES)

]
GAITS_BUTTON_CALLBACK_INPUTS = [Input(i, 'n_clicks') for i in BUTTON_IDS]

# 3. make radio widgets
GAIT_TYPE_RADIO_OPTION_LABEL = ['tripod gaits','ripple gaits']
GAIT_TYPE_RADIO_OPTION_VAL = ['tripod','ripple']

MOVING_DIR_RADIO_OPTION_LABEL = ['moving forward','moving backward','rotate left','rotate right']
MOVING_DIR_RADIO_OPTION_VAL = ['forward','backward','rotate left','rotate right']

radio_widgets = [
    make_radio(option_label,option_val)
    for option_label,option_val in zip(
        [GAIT_TYPE_RADIO_OPTION_LABEL,MOVING_DIR_RADIO_OPTION_LABEL],
        [GAIT_TYPE_RADIO_OPTION_VAL,MOVING_DIR_RADIO_OPTION_VAL])
]

GAITS_WIDGETS_SECTION = html.Div([HEADER] +button_widgets + radio_widgets + widgets)
